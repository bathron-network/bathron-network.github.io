#!/usr/bin/env python3
"""Mutation tests run only in disposable repositories; no network calls."""
from contextlib import contextmanager
import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from common import ROOT, tracked


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V = load('vocab-check')
L = load('link-check')
C = load('confidentiality-check')
S = load('gen-sitemap')


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root, text=True, stderr=subprocess.DEVNULL).strip()


def init(root):
    git(root, 'init', '-q')
    git(root, 'config', 'user.name', 'BATHRON')
    git(root, 'config', 'user.email', 'dev@bathron.org')


@contextmanager
def changed(path, text):
    old = path.read_bytes() if path.exists() else None
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    try:
        yield
    finally:
        if old is None:
            path.unlink()
        else:
            path.write_bytes(old)


class Gates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='docs-gates-')
        cls.root = Path(cls.temp.name) / 'site'
        cls.root.mkdir()
        for p in tracked():
            dest = cls.root / p.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, dest)
        init(cls.root)
        # Construct a small built site from its declared pages and redirects.
        # It tests links without depending on an installed renderer.
        for page in L.summary(cls.root):
            target = cls.root / 'docs/book' / page.replace('.md', '.html')
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text('<h1 id="known">Page</h1>')
        (cls.root / 'docs/book/index.html').write_text('<a href="status.html">Status</a>')
        for key, target in L.redirects(cls.root).items():
            path = cls.root / 'docs/book' / key.lstrip('/')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f'<meta http-equiv="refresh" content="0; URL={target}"><a href="{target}">Page</a>')
        for lang in L.i18n.LANGUAGES:
            if lang['out']:
                path = cls.root / lang['out'] / 'index.html'
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('<a href="/docs/overview.html">Page</a>')
        # Local source fixture: exact anchors cited by the pages, no fetched data.
        cls.spec = Path(cls.temp.name) / 'spec'
        cls.spec.mkdir()
        init(cls.spec)
        files = {L.APP: set()}
        source_prefix = L.PREFIX + L.revision(cls.root) + '/'
        for _, url in L.source_links(cls.root):
            if not url.startswith(source_prefix):
                raise ValueError('source fixture URL does not use NSPEC_REF: ' + url)
            value = url[len(source_prefix):]
            name, _, anchor = value.partition('#')
            files.setdefault(name, set())
            if anchor:
                files[name].add(anchor)
        for name, anchors in files.items():
            path = cls.spec / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('# Public source\n\n' + ''.join('## ' + anchor + '\n\nConceptual content.\n\n' for anchor in sorted(anchors)))
        git(cls.spec, 'add', '.')
        git(cls.spec, 'commit', '-qm', 'Source fixture')
        cls.ref = git(cls.spec, 'rev-parse', 'HEAD')
        # All mutations start from a passing nominal fixture.
        cls.pinned = {}
        for page, _ in L.source_links(cls.root):
            cls.pinned[page] = (cls.root / page).read_text().replace(source_prefix, L.PREFIX + cls.ref + '/')

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def reject(self, check, path, text, marker):
        self.assertEqual(check(self.root), [], 'nominal fixture must pass')
        with changed(self.root / path, text):
            errors = check(self.root)
            self.assertTrue(any(marker in e for e in errors), errors)

    def test_vocabulary_each_gate(self):
        bad = {
            'V1': 'M1 is an asset.', 'V2': 'An operator produces.',
            'V3': 'A quorum chooses the chain.', 'V4': 'The payment is final.',
            'V5': 'The exchange handles trading.', 'V6': 'M0 is money.',
            'V7': 'Settlement is guaranteed.', 'V8': 'An oracle supplies the facts.',
            'V9': 'The mainnet is live.', 'V10': 'A slot takes 20 seconds and 30 s.',
        }
        for rule, sentence in bad.items():
            with self.subTest(rule=rule):
                self.reject(V.check, 'docs/src/mutation.md', '# Mutation\n\n' + sentence, rule + ':')
        path = self.root / 'docs/src/producers.md'
        self.reject(V.check, 'docs/src/producers.md', path.read_text().replace('A ticket is an entry right, never a guarantee.', 'Tickets allow entry.'), 'V11:')
        path = self.root / 'docs/src/engine.md'
        self.reject(V.check, 'docs/src/engine.md', path.read_text().replace('**Normative source:**', '**Source:**'), 'V12:')

    def test_role_mention_missing_or_duplicated(self):
        path = self.root / 'docs/src/glossary.md'
        for replacement in ('', 'formerly called Operator formerly called Operator'):
            with self.subTest(replacement=replacement):
                self.reject(V.check, 'docs/src/glossary.md', path.read_text().replace('formerly called Operator', replacement), 'V2:')

    def test_negation_only_in_designated_pages(self):
        self.reject(V.check, 'docs/src/mutation.md', 'There is no vote.', 'V3:')

    def test_homepage_exception_is_exact(self):
        path = self.root / 'index.html'
        self.reject(V.check, 'index.html', path.read_text().replace('without a vote.', 'without voting.'), 'V3:')

    def test_html_inline_tags_cannot_hide_word(self):
        path = self.root / 'index.html'
        self.reject(V.check, 'index.html', path.read_text().replace('</main>', '<p>M0 is a cur<strong>ren</strong>cy.</p></main>'), 'V6:')

    def test_code_and_urls_are_not_prose(self):
        with changed(self.root / 'docs/src/mutation.md', '# Example\n\n```text\nM1 vote\n```\n\n`M1`\n\n[Reference](https://bathron.org/swap)\n'):
            self.assertEqual(V.check(self.root), [])

    def test_metadata_and_svg_and_alt(self):
        self.reject(V.check, 'img/mutation.svg', '<svg><text>M0 is money.</text></svg>', 'V6:')
        for injected in ('<meta name="description" content="M0 is money.">', '<img alt="M0 is money.">'):
            path = self.root / 'index.html'
            self.reject(V.check, 'index.html', path.read_text() + injected, 'V6:')

    def test_catalogue_english_key(self):
        path = self.root / 'i18n/homepage.fr.po'
        self.reject(V.check, 'i18n/homepage.fr.po', path.read_text() + '\nmsgid "M0 is money."\nmsgstr "M0."\n', 'V6:')

    def test_contextual_negations_still_pass(self):
        path = self.root / 'docs/src/engine.md'
        with changed(path, path.read_text() + '\nThere is no committee. There is no finality. M0 is not money. There is no guarantee.\n'):
            self.assertEqual(V.check(self.root), [])

    def test_confidentiality_patterns(self):
        probes = {
            'ip': ['.'.join(map(str, [192, 0, 2, 44])), ':'.join(['2001', 'db8', '', '4'])],
            'email': ['fixture' + '@' + 'example.invalid'],
            'home-path': ['/' + 'home' + '/fixture/file', '/' + 'Users' + '/fixture/file', '~' + '/fixture/file'],
            'host': ['vps' + str(42)],
            'ai-name': ['co' + 'dex', 'clau' + 'de'],
            'internal': ['lot ' + str(1234), 'DIRECTI' + 'ON', 'QR-' + str(4), 'INCOMPL' + 'ET'],
        }
        for rule, values in probes.items():
            for value in values:
                with self.subTest(rule=rule, value=value):
                    self.reject(C.check, 'docs/src/mutation.md', '# Mutation\n' + value, 'confidentiality/' + rule)

    def test_confidentiality_reads_translation_and_svg(self):
        value = '.'.join(map(str, [192, 0, 2, 44]))
        self.reject(C.check, 'img/mutation.svg', '<svg><text>' + value + '</text></svg>', 'confidentiality/ip')
        path = self.root / 'i18n/homepage.fr.po'
        self.reject(C.check, 'i18n/homepage.fr.po', path.read_text() + '\n# ' + value, 'confidentiality/ip')

    def test_confidentiality_deleted_file_is_ignored(self):
        path = self.root / 'deleted.txt'
        path.write_text('vps' + str(42))
        git(self.root, 'add', 'deleted.txt')
        path.unlink()
        try:
            self.assertEqual(C.check(self.root), [])
        finally:
            git(self.root, 'rm', '--cached', '-q', 'deleted.txt')

    def test_confidentiality_exact_line_exception(self):
        path = self.root / 'docs/theme/index.hbs'
        value = '.'.join(map(str, [127, 0, 0, 1]))
        self.reject(C.check, 'docs/theme/index.hbs', path.read_text() + '\n' + value, 'confidentiality/ip')

    def test_links_and_fragments(self):
        self.reject(L.links, 'docs/book/overview.html', '<a href="absent.html">Broken</a>', 'missing internal')
        self.reject(L.links, 'docs/book/overview.html', '<a href="engine.html#absent">Broken</a>', 'missing anchor')
        self.reject(L.links, 'ar/index.html', '<a href="/docs/absent.html">Broken</a>', 'missing internal')
        self.reject(L.links, 'index.html', (self.root / 'index.html').read_text() + '<a href="#absent">Broken</a>', 'missing anchor')

    def test_built_redirect(self):
        self.reject(L.links, 'docs/book/m1.html', '<p>No redirect.</p>', 'stale built redirect')

    def test_redirect_chain_missing_and_collision(self):
        path = self.root / 'docs/book.toml'
        for line in ('"/mutation.html" = "m1.html"', '"/mutation.html" = "absent.html"', '"/overview.html" = "roles.html"'):
            self.reject(L.redirect_check, 'docs/book.toml', path.read_text() + '\n' + line + '\n', 'redirect')

    def test_book_scope(self):
        self.reject(L.redirect_check, 'docs/src/mutation.md', '# Unexpected page', 'book scope:')

    def test_numeric_sentence_end(self):
        for text in ('The parameter is 100.', 'The rate is 1%.'):
            self.reject(V.check, 'docs/src/mutation.md', text, 'V10:')

    def test_sitemap(self):
        self.reject(S.check, 'sitemap.xml', '<urlset/>', 'sitemap.xml:')

    def test_orphan_image(self):
        self.reject(L.images, 'img/mutation.svg', '<svg/>', 'unreferenced image')

    def test_sources_fail_closed(self):
        with self.pinned_context():
            check = lambda root: L.sources(root, self.spec)
            self.assertEqual(check(self.root), [])
            self.reject(check, 'docs/NSPEC_REF', 'REF\n', 'TODO-REF')
            path = self.root / 'index.html'
            original = path.read_text()
            for replacement, message in (
                ('/blob/' + '0' * 40 + '/', 'does not use NSPEC_REF'),
            ):
                self.reject(check, 'index.html', original.replace('/blob/' + self.ref + '/', replacement), message)
            base = L.PREFIX + self.ref + '/'
            for target, message in [
                ('spec/N-SPEC-v0.7.md#absent', 'missing normative anchor'),
                ('spec/N-SPEC-v0.7.md#13-settlement', 'settlement chapter'),
                (L.APP + '#other-section', 'application section'),
                ('qualification/fixture.md', 'outside permitted public scope')]:
                self.reject(check, 'index.html', original + '<a href="' + base + target + '">Source</a>', message)
            self.assertTrue(L.sources(self.root, self.root))

    @contextmanager
    def pinned_context(self):
        from contextlib import ExitStack
        with ExitStack() as stack:
            stack.enter_context(changed(self.root / 'docs/NSPEC_REF', self.ref + '\n'))
            for page, text in self.__class__.pinned.items():
                stack.enter_context(changed(self.root / page, text))
            yield

    def test_source_citation_label_matches_anchor(self):
        self.assertEqual(L.citation_check(self.root), [])
        path = self.root / 'docs/src/burns.md'
        self.reject(L.citation_check, 'docs/src/burns.md', path.read_text().replace('[§4.9][n49]', '[§4.8][n49]'), 'section label')

    def test_sources_require_curated_app(self):
        with self.pinned_context():
            self.assertEqual(L.sources(self.root, self.spec), [])
            git(self.spec, 'rm', '-q', L.APP)
            git(self.spec, 'commit', '-qm', 'Remove application fixture')
            missing = git(self.spec, 'rev-parse', 'HEAD')
            try:
                with changed(self.root / 'docs/NSPEC_REF', missing + '\n'):
                    self.assertTrue(any('curated application' in e for e in L.sources(self.root, self.spec)))
            finally:
                git(self.spec, 'reset', '--hard', self.ref)

    def test_historical_source_exception_required(self):
        with self.pinned_context():
            self.assertEqual(L.sources(self.root, self.spec), [])
            path = self.spec / 'spec/N-SPEC-v0.7.md'
            original = path.read_text()
            self.assertIn('## 49-burn-m0-v3\n', original)
            path.write_text(original.replace('## 49-burn-m0-v3', '## 49-burn-m0-v3\n\nM1'))
            git(self.spec, 'add', '.')
            git(self.spec, 'commit', '-qm', 'Historical wording fixture')
            historic = git(self.spec, 'rev-parse', 'HEAD')
            from contextlib import ExitStack
            try:
                with ExitStack() as stack:
                    stack.enter_context(changed(self.root / 'docs/NSPEC_REF', historic + '\n'))
                    for page, text in self.__class__.pinned.items():
                        stack.enter_context(changed(self.root / page, text.replace(self.ref, historic)))
                    self.assertTrue(any('historical wording needs' in e for e in L.sources(self.root, self.spec)))
            finally:
                git(self.spec, 'reset', '--hard', self.ref)

    def test_metadata_author_committer_and_branch(self):
        repo = Path(self.temp.name) / 'metadata'
        repo.mkdir(exist_ok=True)
        init(repo)
        git(repo, 'commit', '--allow-empty', '-qm', 'Base fixture')
        base = git(repo, 'rev-parse', 'HEAD')
        git(repo, 'commit', '--allow-empty', '-qm', 'Valid fixture')
        head = git(repo, 'rev-parse', 'HEAD')
        self.assertEqual(C.metadata(repo, base, head, 'docs/fixture'), [])
        self.assertTrue(C.metadata(repo, base, head, 'fixture'))
        git(repo, '-c', 'user.email=security@bathron.org', 'commit', '--allow-empty', '-qm', 'Invalid identity fixture')
        self.assertTrue(C.metadata(repo, base, git(repo, 'rev-parse', 'HEAD'), 'docs/fixture'))
        self.assertTrue(C.metadata(repo, None, None, 'docs/fixture'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
