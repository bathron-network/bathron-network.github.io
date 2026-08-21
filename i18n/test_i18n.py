#!/usr/bin/env python3
"""Unit tests for the BATHRON homepage i18n generator.

Separate from the mutation test: this suite exercises the walker, the strict PO
reader, language/path bounding and the build gates. It asserts on the GENERATED
HTML, not only on Python data structures.

    python3 i18n/test_i18n.py            # or: python3 -m unittest discover i18n
"""
import builtins, importlib.util, os, re, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import i18n as M  # noqa: E402  (the real module, rooted at the real repo)

_UNIQ = [0]


# --------------------------------------------------------------------------
# A minimal but complete page, used to build throwaway repositories.
# --------------------------------------------------------------------------

FIXTURE_HTML = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="A short description.">
<meta property="og:url" content="https://bathron.org/">
<meta property="og:image" content="https://bathron.org/img/og.png">
<link rel="canonical" href="https://bathron.org/">
<link rel="alternate" hreflang="en" href="https://bathron.org/">
<link rel="alternate" hreflang="fr" href="https://bathron.org/fr/">
<link rel="alternate" hreflang="x-default" href="https://bathron.org/">
<title>Fixture</title>
<style>body{color:#fff;width:900px}</style>
</head>
<body>
<div class="topbar">
<nav class="langsel" aria-label="Language selection"><span aria-current="page" lang="en">EN</span><a href="/fr/" hreflang="fr" lang="fr">FR</a></nav>
</div>
<div class="hero">
<img src="/img/e.png" alt="An emblem">
<p data-i18n-context="hero">Settlement<br><b>anchored.</b></p>
</div>
<p>Settlement</p>
<p>Bitcoin&rsquo;s chain.</p>
<p>Read the docs &rarr;</p>
<script>var x = "Not translatable";</script>
</body>
</html>
'''

PO_HEADER = ('msgid ""\nmsgstr ""\n"Language: fr\\n"\n'
             '"Content-Type: text/plain; charset=UTF-8\\n"\n\n')


def po(entries, header=PO_HEADER):
    """entries: list of (ctx, msgid, msgstr, flags)"""
    out = [header]
    for ctx, mid, mstr, flags in entries:
        if flags: out.append(f'#, {", ".join(flags)}\n')
        if ctx: out.append(f'msgctxt "{M.po_escape(ctx)}"\n')
        out.append(f'msgid "{M.po_escape(mid)}"\nmsgstr "{M.po_escape(mstr)}"\n\n')
    return ''.join(out)


def full_fr_po(html=FIXTURE_HTML, override=None):
    """A complete French catalogue for `html`, translating each key as fr:<en>.

    `override` maps a (context, msgid) key to an explicit translation.
    """
    override = override or {}
    rows = []
    for ctx, s in M.collect(html):
        rows.append((ctx, s, override.get((ctx, s), f'fr:{s}'), []))
    return po(rows)


def make_repo(html=FIXTURE_HTML, po_text=None, write_po=True):
    """A throwaway repository whose i18n module is rooted inside it."""
    d = tempfile.mkdtemp(prefix='i18n-test-')
    os.makedirs(os.path.join(d, 'i18n'))
    shutil.copy(os.path.join(HERE, 'i18n.py'), os.path.join(d, 'i18n', 'i18n.py'))
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    if write_po:
        with open(os.path.join(d, 'i18n', 'homepage.fr.po'), 'w', encoding='utf-8') as f:
            f.write(po_text if po_text is not None else full_fr_po(html))
    _UNIQ[0] += 1
    name = f'i18n_sandbox_{_UNIQ[0]}'
    spec = importlib.util.spec_from_file_location(name, os.path.join(d, 'i18n', 'i18n.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.ROOT == os.path.realpath(d), (mod.ROOT, d)
    return d, mod


class RepoCase(unittest.TestCase):
    def repo(self, *a, **kw):
        d, mod = make_repo(*a, **kw)
        self.addCleanup(shutil.rmtree, d, True)
        return d, mod

    def built(self, d):
        with open(os.path.join(d, 'fr', 'index.html'), encoding='utf-8') as f:
            return f.read()


# --------------------------------------------------------------------------
# 1. The HTML walker
# --------------------------------------------------------------------------

class TestWalker(unittest.TestCase):
    def keys(self, html):
        return M.collect(html)

    def strings(self, html):
        return [s for _c, s in M.collect(html)]

    def roundtrip(self, html):
        w = M.Walker(lambda d, c: d, lambda t, k, v, n=None, c='': v)
        w.feed(html); w.close()
        return w.document

    def test_plain_text(self):
        self.assertEqual(self.strings('<p>Hello world</p>'), ['Hello world'])

    def test_whitespace_is_normalised_and_blank_ignored(self):
        self.assertEqual(self.strings('<p>  Hello\n  world  </p><p>   </p>'), ['Hello world'])

    def test_named_entity(self):
        self.assertEqual(self.strings('<p>Tom &amp; Jerry</p>'), ['Tom & Jerry'])

    def test_numeric_entity(self):
        self.assertEqual(self.strings('<p>caf&#233;</p>'), ['café'])

    def test_text_spanning_an_entity_is_one_string(self):
        self.assertEqual(self.strings('<p>Bitcoin&rsquo;s chain.</p>'), ['Bitcoin’s chain.'])

    def test_entity_roundtrip_is_byte_identical(self):
        src = '<p>Bitcoin&rsquo;s chain &amp; more &#8594;</p>'
        self.assertEqual(self.roundtrip(src), src)

    def test_void_tags_split_strings_but_do_not_leak_context(self):
        html = '<div data-i18n-context="c"><p>A<br>B</p></div><p>C</p>'
        self.assertEqual(M.collect(html), [('c', 'A'), ('c', 'B'), ('', 'C')])

    def test_nested_tags(self):
        self.assertEqual(self.strings('<div><p>Outer <b>inner</b> tail</p></div>'),
                         ['Outer', 'inner', 'tail'])

    def test_style_and_script_never_extracted(self):
        html = '<style>body{content:"nope"}</style><script>var s="nope";</script><p>Yes</p>'
        self.assertEqual(self.strings(html), ['Yes'])

    def test_style_content_survives_untouched(self):
        src = '<style>body{color:#fff}\n.a{width:900px}</style>'
        self.assertEqual(self.roundtrip(src), src)

    def test_translatable_attributes(self):
        html = ('<img src="/a.png" alt="An emblem">'
                '<a href="/x" title="A title">t</a>'
                '<meta name="description" content="A description.">')
        self.assertEqual(sorted(self.strings(html)),
                         ['A description.', 'A title', 'An emblem', 't'])

    def test_structural_attributes_excluded(self):
        html = ('<meta name="viewport" content="width=device-width,initial-scale=1">'
                '<meta property="og:image" content="https://x/og.png">'
                '<meta name="twitter:card" content="summary_large_image">'
                '<html lang="en">')
        self.assertEqual(self.strings(html), [])

    def test_msgctxt_captured(self):
        self.assertEqual(M.collect('<p data-i18n-context="hero">A</p>'), [('hero', 'A')])

    def test_same_string_two_contexts_are_two_keys(self):
        html = '<p data-i18n-context="hero">Settlement</p><p>Settlement</p>'
        self.assertEqual(M.collect(html), [('hero', 'Settlement'), ('', 'Settlement')])

    def test_context_attribute_stripped_from_output(self):
        out = self.roundtrip('<p data-i18n-context="hero">A</p>')
        self.assertNotIn('data-i18n-context', out)
        self.assertEqual(out, '<p>A</p>')

    def test_duplicate_string_same_context_collected_once(self):
        self.assertEqual(M.collect('<p>Same</p><p>Same</p>'), [('', 'Same')])

    def test_malformed_html_unbalanced_close(self):
        # a stray close tag must not crash the walker nor corrupt extraction
        self.assertEqual(self.strings('<p>A</p></div><p>B</p>'), ['A', 'B'])

    def test_malformed_html_unclosed_tag(self):
        self.assertEqual(self.strings('<div><p>A'), ['A'])

    def test_malformed_context_not_closed_does_not_crash(self):
        self.assertEqual(M.collect('<div data-i18n-context="x"><p>A'), [('x', 'A')])

    def test_comments_and_doctype_preserved(self):
        src = '<!doctype html><!-- keep me --><p>A</p>'
        self.assertEqual(self.roundtrip(src), src)

    def test_real_homepage_roundtrip_is_byte_identical(self):
        with open(os.path.join(REPO, 'index.html'), encoding='utf-8') as f:
            src = f.read()
        expected = src.replace(' data-i18n-context="hero"', '')
        self.assertEqual(self.roundtrip(src), expected)


# --------------------------------------------------------------------------
# 2. Language and path bounding
# --------------------------------------------------------------------------

class TestLanguageBounding(unittest.TestCase):
    BAD = ['../../x', '../fr', 'fr/../..', '/etc', '', 'FR', 'fr.', 'f', 'fra',
           'fr/', './fr', 'fr\x00', '..']

    def test_bad_languages_rejected(self):
        for bad in self.BAD:
            with self.subTest(lang=bad):
                with self.assertRaises(M.LangError):
                    M.validate_lang(bad)

    def test_unknown_but_wellformed_language_rejected(self):
        with self.assertRaises(M.LangError):
            M.validate_lang('de')

    def test_english_is_not_generated(self):
        with self.assertRaises(M.LangError):
            M.lang_dir('en')

    def test_paths_stay_inside_the_repository(self):
        self.assertEqual(M.out_path('fr'), os.path.join(M.ROOT, 'fr', 'index.html'))
        self.assertEqual(M.po_path('fr'), os.path.join(M.ROOT, 'i18n', 'homepage.fr.po'))
        for p in (M.out_path('fr'), M.po_path('fr')):
            self.assertEqual(os.path.commonpath([M.ROOT, os.path.realpath(p)]), M.ROOT)

    def test_non_string_language_rejected(self):
        for bad in (None, 3, ['fr'], {'fr': 1}):
            with self.subTest(lang=bad):
                with self.assertRaises(M.LangError):
                    M.validate_lang(bad)


class TestNoFilesystemAccessOnBadLanguage(unittest.TestCase):
    """Prove that a rejected language touches NOTHING on disk."""

    def run_spied(self, fn):
        calls = []
        real = {'open': builtins.open, 'remove': os.remove, 'unlink': os.unlink,
                'makedirs': os.makedirs, 'mkdir': os.mkdir, 'replace': os.replace,
                'rename': os.rename, 'rmtree': shutil.rmtree, 'mkstemp': tempfile.mkstemp}

        def spy(name, f):
            def wrapper(*a, **kw):
                calls.append((name, a[:1]))
                return f(*a, **kw)
            return wrapper

        builtins.open = spy('open', real['open'])
        for n in ('remove', 'unlink', 'makedirs', 'mkdir', 'replace', 'rename'):
            setattr(os, n, spy(n, real[n]))
        shutil.rmtree = spy('rmtree', real['rmtree'])
        tempfile.mkstemp = spy('mkstemp', real['mkstemp'])
        try:
            result = fn()
        finally:
            builtins.open = real['open']
            for n in ('remove', 'unlink', 'makedirs', 'mkdir', 'replace', 'rename'):
                setattr(os, n, real[n])
            shutil.rmtree = real['rmtree']
            tempfile.mkstemp = real['mkstemp']
        return result, calls

    def test_build_with_traversal_touches_no_file(self):
        for bad in ('../../x', '/etc', '..', 'fr/../..', 'de', 'en'):
            with self.subTest(lang=bad):
                rc, calls = self.run_spied(lambda: M.build(bad))
                self.assertEqual(rc, 2, f'{bad!r} should be refused')
                self.assertEqual(calls, [], f'{bad!r} touched the filesystem: {calls}')

    def test_check_with_traversal_touches_no_file(self):
        for bad in ('../../x', '/etc', 'de'):
            with self.subTest(lang=bad):
                def go():
                    try:
                        M.check(bad, verbose=False)
                    except M.I18nError as e:
                        return e
                    return None
                err, calls = self.run_spied(go)
                self.assertIsInstance(err, M.I18nError)
                self.assertEqual(calls, [], f'{bad!r} touched the filesystem: {calls}')

    def test_sentinel_outside_the_repository_is_untouched(self):
        d = tempfile.mkdtemp(prefix='i18n-sentinel-')
        self.addCleanup(shutil.rmtree, d, True)
        sentinel = os.path.join(d, 'index.html')
        with open(sentinel, 'w', encoding='utf-8') as f:
            f.write('SENTINEL')
        before = os.stat(sentinel)
        for bad in (os.path.join('..', os.path.basename(d)), '../../x', d):
            M.build(bad)
        after = os.stat(sentinel)
        with open(sentinel, encoding='utf-8') as f:
            self.assertEqual(f.read(), 'SENTINEL')
        self.assertEqual((before.st_size, before.st_mtime_ns),
                         (after.st_size, after.st_mtime_ns))
        self.assertEqual(sorted(os.listdir(d)), ['index.html'])


# --------------------------------------------------------------------------
# 3. The strict PO reader
# --------------------------------------------------------------------------

class TestPoReader(unittest.TestCase):
    def parse(self, text, expect_lang='fr'):
        d = tempfile.mkdtemp(prefix='i18n-po-')
        self.addCleanup(shutil.rmtree, d, True)
        p = os.path.join(d, 'c.po')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(text)
        return M.read_po(p, expect_lang=expect_lang)

    def bad(self, text, fragment=None, expect_lang='fr'):
        with self.assertRaises(M.PoError) as cm:
            self.parse(text, expect_lang)
        if fragment:
            self.assertIn(fragment, str(cm.exception))
        return str(cm.exception)

    # --- valid ---------------------------------------------------------
    def test_valid_catalogue(self):
        entries, flags = self.parse(po([('', 'A', 'fr:A', []), ('hero', 'A', 'fr:hero A', [])]))
        self.assertEqual(entries, {('', 'A'): 'fr:A', ('hero', 'A'): 'fr:hero A'})
        self.assertEqual(flags[('', 'A')], [])

    def test_valid_multiline_continuation(self):
        text = PO_HEADER + 'msgid ""\n"Long "\n"string"\nmsgstr ""\n"Longue "\n"chaine"\n\n'
        entries, _ = self.parse(text)
        self.assertEqual(entries, {('', 'Long string'): 'Longue chaine'})

    def test_valid_flags_preserved(self):
        _e, flags = self.parse(po([('', 'A', 'fr:A', ['fuzzy'])]))
        self.assertEqual(flags[('', 'A')], ['fuzzy'])

    def test_valid_escapes(self):
        text = PO_HEADER + 'msgid "a\\"b\\\\c\\nd"\nmsgstr "x"\n\n'
        entries, _ = self.parse(text)
        self.assertEqual(list(entries)[0][1], 'a"b\\c\nd')

    def test_comments_ignored(self):
        text = PO_HEADER + '# a comment\n#. extracted\n#: ref\nmsgid "A"\nmsgstr "B"\n\n'
        entries, _ = self.parse(text)
        self.assertEqual(entries, {('', 'A'): 'B'})

    # --- invalid -------------------------------------------------------
    def test_duplicate_entry_rejected(self):
        self.bad(po([('', 'A', 'one', []), ('', 'A', 'two', [])]), 'duplicate entry')

    def test_duplicate_entry_with_same_context_rejected(self):
        self.bad(po([('h', 'A', 'one', []), ('h', 'A', 'two', [])]), 'duplicate entry')

    def test_same_msgid_different_context_is_not_duplicate(self):
        entries, _ = self.parse(po([('h', 'A', 'one', []), ('', 'A', 'two', [])]))
        self.assertEqual(len(entries), 2)

    def test_repeated_msgid_in_one_entry_rejected(self):
        self.bad(PO_HEADER + 'msgid "A"\nmsgid "B"\nmsgstr "C"\n\n', 'repeated msgid')

    def test_repeated_msgstr_in_one_entry_rejected(self):
        self.bad(PO_HEADER + 'msgid "A"\nmsgstr "B"\nmsgstr "C"\n\n', 'repeated msgstr')

    def test_repeated_msgctxt_in_one_entry_rejected(self):
        self.bad(PO_HEADER + 'msgctxt "a"\nmsgctxt "b"\nmsgid "A"\nmsgstr "C"\n\n',
                 'repeated msgctxt')

    def test_msgctxt_after_msgid_rejected(self):
        self.bad(PO_HEADER + 'msgid "A"\nmsgctxt "a"\nmsgstr "C"\n\n', 'msgctxt must come first')

    def test_msgid_after_msgstr_rejected(self):
        self.bad(PO_HEADER + 'msgstr "C"\nmsgid "A"\n\n', 'msgid after msgstr')

    def test_continuation_without_mode_rejected(self):
        self.bad(PO_HEADER + '"orphan"\nmsgid "A"\nmsgstr "B"\n\n', 'continuation string')

    def test_unrecognised_line_rejected(self):
        self.bad(PO_HEADER + 'msgid "A"\ngarbage here\nmsgstr "B"\n\n', 'unrecognised line')

    def test_invalid_escape_rejected(self):
        self.bad(PO_HEADER + 'msgid "a\\qb"\nmsgstr "B"\n\n', 'invalid escape')

    def test_dangling_backslash_rejected(self):
        self.bad(PO_HEADER + 'msgid "ab\\"\nmsgstr "B"\n\n')

    def test_incomplete_entry_missing_msgstr_rejected(self):
        self.bad(PO_HEADER + 'msgid "A"\n\n', 'has no msgstr')

    def test_incomplete_entry_missing_msgid_rejected(self):
        self.bad(PO_HEADER + 'msgctxt "c"\nmsgstr "B"\n\n', 'has no msgid')

    def test_missing_header_rejected(self):
        self.bad('msgid "A"\nmsgstr "B"\n\n', 'before the header')

    def test_duplicate_header_rejected(self):
        self.bad(PO_HEADER + PO_HEADER, 'duplicate header')

    def test_empty_file_has_no_header(self):
        self.bad('', 'no header entry')

    def test_wrong_language_rejected(self):
        header = 'msgid ""\nmsgstr ""\n"Language: de\\n"\n\n'
        self.bad(po([('', 'A', 'B', [])], header=header), 'but \'fr\' was requested')

    def test_missing_language_field_rejected(self):
        header = 'msgid ""\nmsgstr ""\n"Content-Type: text/plain\\n"\n\n'
        self.bad(po([('', 'A', 'B', [])], header=header), 'no "Language:" field')

    def test_language_variant_accepted(self):
        header = 'msgid ""\nmsgstr ""\n"Language: fr_FR\\n"\n\n'
        entries, _ = self.parse(po([('', 'A', 'B', [])], header=header))
        self.assertEqual(entries, {('', 'A'): 'B'})

    def test_obsolete_block_rejected(self):
        self.bad(po([('', 'A', 'B', [])]) + '#~ msgid "old"\n#~ msgstr "vieux"\n',
                 'obsolete entry')

    def test_flags_attached_to_nothing_rejected(self):
        self.bad(PO_HEADER + '#, fuzzy\n\n', 'flags attached to no entry')

    def test_flag_line_inside_entry_rejected(self):
        self.bad(PO_HEADER + 'msgid "A"\n#, fuzzy\nmsgstr "B"\n\n', 'flag line inside an entry')

    def test_missing_file_rejected(self):
        with self.assertRaises(M.PoError):
            M.read_po('/nonexistent/nowhere.po', expect_lang='fr')

    def test_header_with_context_rejected(self):
        self.bad('msgctxt "x"\nmsgid ""\nmsgstr ""\n"Language: fr\\n"\n\n',
                 'must not carry a msgctxt')


# --------------------------------------------------------------------------
# 4. Build gates, on generated HTML
# --------------------------------------------------------------------------

class TestBuild(RepoCase):
    def test_complete_catalogue_builds(self):
        d, mod = self.repo()
        self.assertEqual(mod.build('fr'), 0)
        out = self.built(d)
        self.assertIn('<html lang="fr"', out)
        self.assertIn('fr:Settlement', out)
        self.assertNotIn('data-i18n-context', out)

    def test_context_gives_two_different_renderings(self):
        d, mod = self.repo(po_text=full_fr_po(override={('hero', 'Settlement'): 'HERO',
                                                        ('', 'Settlement'): 'PLAIN'}))
        self.assertEqual(mod.build('fr'), 0)
        out = self.built(d)
        self.assertIn('<p>HERO<br>', out)
        self.assertIn('<p>PLAIN</p>', out)

    def test_structural_facts_rewritten(self):
        d, mod = self.repo()
        mod.build('fr')
        out = self.built(d)
        self.assertIn('<link rel="canonical" href="https://bathron.org/fr/">', out)
        self.assertIn('<meta property="og:url" content="https://bathron.org/fr/">', out)
        self.assertIn(M.LANG_CONF['fr']['sel'], out)
        self.assertIn('aria-label="Sélection de la langue"', out)
        self.assertNotIn('aria-label="Language selection"', out)

    def test_style_block_untouched(self):
        d, mod = self.repo()
        mod.build('fr')
        self.assertIn('<style>body{color:#fff;width:900px}</style>', self.built(d))

    def test_structural_attributes_not_translated(self):
        d, mod = self.repo()
        mod.build('fr')
        out = self.built(d)
        self.assertIn('content="width=device-width,initial-scale=1"', out)
        self.assertIn('content="https://bathron.org/img/og.png"', out)

    # --- refusals ------------------------------------------------------
    def refuse(self, po_text=None, html=FIXTURE_HTML, write_po=True):
        d, mod = self.repo(html=html, po_text=po_text, write_po=write_po)
        rc = mod.build('fr')
        self.assertNotEqual(rc, 0)
        self.assertFalse(os.path.exists(os.path.join(d, 'fr', 'index.html')))
        return d, mod

    def test_missing_entry_refused(self):
        rows = [(c, s, f'fr:{s}', []) for c, s in M.collect(FIXTURE_HTML)][:-1]
        self.refuse(po(rows))

    def test_empty_translation_refused(self):
        rows = [(c, s, '' if s == 'Settlement' else f'fr:{s}', [])
                for c, s in M.collect(FIXTURE_HTML)]
        self.refuse(po(rows))

    def test_fuzzy_entry_refused(self):
        rows = [(c, s, f'fr:{s}', ['fuzzy'] if s == 'Settlement' else [])
                for c, s in M.collect(FIXTURE_HTML)]
        self.refuse(po(rows))

    def test_obsolete_entry_refused(self):
        rows = [(c, s, f'fr:{s}', []) for c, s in M.collect(FIXTURE_HTML)]
        rows.append(('', 'A string no longer in the page', 'obsolete', []))
        self.refuse(po(rows))

    def test_duplicate_entry_refused(self):
        rows = [(c, s, f'fr:{s}', []) for c, s in M.collect(FIXTURE_HTML)]
        rows.append(('', 'Settlement', 'duplicate', []))
        self.refuse(po(rows))

    def test_malformed_catalogue_refused(self):
        self.refuse(PO_HEADER + 'msgid "A"\ngarbage\nmsgstr "B"\n\n')

    def test_empty_catalogue_refused(self):
        self.refuse('')

    def test_absent_catalogue_refused(self):
        self.refuse(write_po=False)

    def test_wrong_language_catalogue_refused(self):
        rows = [(c, s, f'fr:{s}', []) for c, s in M.collect(FIXTURE_HTML)]
        self.refuse(po(rows, header='msgid ""\nmsgstr ""\n"Language: de\\n"\n\n'))

    # --- structural facts absent or duplicated -------------------------
    def test_missing_selector_refused(self):
        html = FIXTURE_HTML.replace(M.LANG_CONF['en']['sel'], '')
        self.refuse(html=html, po_text=full_fr_po(html))

    def test_duplicate_selector_refused(self):
        sel = M.LANG_CONF['en']['sel']
        html = FIXTURE_HTML.replace(sel, sel + '\n' + sel)
        self.refuse(html=html, po_text=full_fr_po(html))

    def test_missing_canonical_refused(self):
        html = FIXTURE_HTML.replace('<link rel="canonical" href="https://bathron.org/">', '')
        self.refuse(html=html, po_text=full_fr_po(html))

    def test_duplicate_canonical_refused(self):
        link = '<link rel="canonical" href="https://bathron.org/">'
        html = FIXTURE_HTML.replace(link, link + '\n' + link)
        self.refuse(html=html, po_text=full_fr_po(html))

    def test_missing_ogurl_refused(self):
        html = FIXTURE_HTML.replace('<meta property="og:url" content="https://bathron.org/">', '')
        self.refuse(html=html, po_text=full_fr_po(html))

    def test_duplicate_ogurl_refused(self):
        og = '<meta property="og:url" content="https://bathron.org/">'
        html = FIXTURE_HTML.replace(og, og + '\n' + og)
        self.refuse(html=html, po_text=full_fr_po(html))

    # --- artifact lifecycle --------------------------------------------
    def test_stale_artifact_removed_before_validation(self):
        d, mod = self.repo()
        self.assertEqual(mod.build('fr'), 0)
        first = self.built(d)
        self.assertIn('fr:Settlement', first)
        # break the catalogue, rebuild: the old page must be gone
        with open(os.path.join(d, 'i18n', 'homepage.fr.po'), 'w', encoding='utf-8') as f:
            f.write(PO_HEADER)
        self.assertNotEqual(mod.build('fr'), 0)
        self.assertFalse(os.path.exists(os.path.join(d, 'fr', 'index.html')))

    def test_no_temporary_file_left_behind(self):
        d, mod = self.repo()
        self.assertEqual(mod.build('fr'), 0)
        leftovers = [f for f in os.listdir(os.path.join(d, 'fr')) if f != 'index.html']
        self.assertEqual(leftovers, [])

    def test_unknown_language_build_returns_two(self):
        _d, mod = self.repo()
        self.assertEqual(mod.build('de'), 2)
        self.assertEqual(mod.build('../../x'), 2)


# --------------------------------------------------------------------------
# 4b. The language selector
# --------------------------------------------------------------------------

class TestLanguageSelector(RepoCase):
    """The selector is a per-language structural fact, checked explicitly."""

    def page(self, d, lang):
        path = os.path.join(d, 'index.html') if lang == 'en' else os.path.join(d, 'fr', 'index.html')
        with open(path, encoding='utf-8') as f:
            return f.read()

    def build_both(self):
        d, mod = self.repo()
        self.assertEqual(mod.build('fr'), 0)
        return d, mod

    def test_exactly_one_selector_per_page(self):
        d, _mod = self.build_both()
        for lang in ('en', 'fr'):
            with self.subTest(lang=lang):
                doc = self.page(d, lang)
                self.assertEqual(doc.count('class="langsel"'), 1)
                self.assertEqual(len(re.findall(r'<nav class="langsel".*?</nav>', doc, re.S)), 1)

    def test_active_language_is_correct_and_not_a_link(self):
        d, _mod = self.build_both()
        for lang in ('en', 'fr'):
            with self.subTest(lang=lang):
                nav = re.search(r'<nav class="langsel".*?</nav>', self.page(d, lang), re.S).group(0)
                m = re.search(r'<(\w+)[^>]*aria-current="page"[^>]*>([^<]*)</\1>', nav)
                self.assertIsNotNone(m)
                self.assertNotEqual(m.group(1), 'a', 'the active language must not be a link')
                self.assertEqual(m.group(2), lang.upper())

    def test_other_language_target_is_correct(self):
        d, _mod = self.build_both()
        for lang, other, href in (('en', 'fr', '/fr/'), ('fr', 'en', '/')):
            with self.subTest(lang=lang):
                nav = re.search(r'<nav class="langsel".*?</nav>', self.page(d, lang), re.S).group(0)
                links = re.findall(r'<a href="([^"]*)" hreflang="([^"]*)" lang="([^"]*)">([^<]*)</a>', nav)
                self.assertEqual(len(links), 1)
                self.assertEqual(links[0], (href, other, other, other.upper()))

    def test_aria_current_appears_exactly_once(self):
        d, _mod = self.build_both()
        for lang in ('en', 'fr'):
            with self.subTest(lang=lang):
                doc = self.page(d, lang)
                self.assertEqual(len(re.findall(r'<[a-zA-Z][^>]*\baria-current=', doc)), 1)

    def test_selector_is_above_the_hero(self):
        d, _mod = self.build_both()
        for lang in ('en', 'fr'):
            with self.subTest(lang=lang):
                doc = self.page(d, lang)
                self.assertIn('class="topbar"', doc)
                self.assertLess(doc.index('class="langsel"'), doc.index('<div class="hero">'),
                                'the selector must sit in the top bar, above the hero')

    def test_no_nested_interactive_element(self):
        d, _mod = self.build_both()
        for lang in ('en', 'fr'):
            with self.subTest(lang=lang):
                nav = re.search(r'<nav class="langsel".*?</nav>', self.page(d, lang), re.S).group(0)
                self.assertIsNone(re.search(r'<a\b[^>]*>(?:(?!</a>).)*<(?:a|button|select|input)\b',
                                            nav, re.S))

    # --- negative: the checks must actually fail on a wrong selector --------
    def corrupt_and_verify(self, transform):
        """Build, corrupt the French page, and return verify()'s problems."""
        d, mod = self.build_both()
        path = os.path.join(d, 'fr', 'index.html')
        with open(path, encoding='utf-8') as f:
            doc = f.read()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(transform(doc, mod))
        return mod.verify('fr', verbose=False)

    def kinds(self, problems):
        return {k for k, _ in problems}

    def test_verify_rejects_a_missing_aria_current(self):
        p = self.corrupt_and_verify(lambda d, m: d.replace(' aria-current="page"', '', 1))
        self.assertIn('ARIA-CURRENT', self.kinds(p))

    def test_verify_rejects_a_duplicated_aria_current(self):
        p = self.corrupt_and_verify(
            lambda d, m: d.replace('<a href="/" hreflang="en" lang="en">',
                                   '<a href="/" hreflang="en" lang="en" aria-current="page">', 1))
        self.assertIn('ARIA-CURRENT', self.kinds(p))

    def test_verify_rejects_an_active_language_that_is_a_link(self):
        p = self.corrupt_and_verify(
            lambda d, m: d.replace('<span aria-current="page" lang="fr">FR</span>',
                                   '<a aria-current="page" lang="fr" href="/fr/">FR</a>', 1))
        self.assertIn('SELECTOR', self.kinds(p))

    def test_verify_rejects_a_wrong_other_language_target(self):
        p = self.corrupt_and_verify(
            lambda d, m: d.replace('<a href="/" hreflang="en" lang="en">',
                                   '<a href="/en/" hreflang="en" lang="en">', 1))
        self.assertIn('SELECTOR', self.kinds(p))

    def test_verify_rejects_a_duplicated_selector(self):
        def dup(doc, mod):
            nav = mod.LANG_CONF['fr']['sel']
            return doc.replace(nav, nav + nav, 1)
        self.assertIn('COUNT', self.kinds(self.corrupt_and_verify(dup)))

    def test_verify_rejects_a_selector_left_in_the_hero(self):
        def move(doc, mod):
            nav = mod.LANG_CONF['fr']['sel']
            return doc.replace(nav, '', 1).replace('<div class="hero">',
                                                   '<div class="hero">' + nav, 1)
        self.assertIn('SELECTOR', self.kinds(self.corrupt_and_verify(move)))

    def test_verify_accepts_the_untouched_page(self):
        d, mod = self.build_both()
        self.assertEqual(mod.verify('fr', verbose=False), [])
        self.assertEqual(mod.verify('en', verbose=False), [])

    def test_selector_carries_no_prose_into_the_catalogue(self):
        """aria-label is a structural fact, not a translatable string."""
        keys = [k[1] for k in M.collect(FIXTURE_HTML)]
        self.assertNotIn('Language selection', keys)
        self.assertNotIn('Sélection de la langue', keys)


# --------------------------------------------------------------------------
# 5. verify / compare / static-overflow-check on the REAL pages
# --------------------------------------------------------------------------

class TestRealPages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.built = M.build('fr') == 0

    def test_english_page_verifies(self):
        self.assertEqual(M.verify('en', verbose=False), [])

    def test_french_page_verifies(self):
        self.assertTrue(self.built)
        self.assertEqual(M.verify('fr', verbose=False), [])

    def test_skeletons_match(self):
        self.assertTrue(self.built)
        self.assertEqual(M.compare(verbose=False), [])

    def test_no_static_overflow_hazard(self):
        self.assertTrue(self.built)
        self.assertEqual(M.static_overflow_check(verbose=False), [])

    def test_catalogue_is_complete(self):
        self.assertEqual(M.check('fr', verbose=False), [])


# --------------------------------------------------------------------------
# 6. The mutation-test harness itself
#
# A harness that cannot run must never report success. An earlier version used
# `declare -A`, which Bash 3.2 (the /bin/bash macOS ships) rejects; the guarded
# file checks then silently did not run and the script still printed PASS and
# exited 0. These tests make that class of failure a hard error.
# --------------------------------------------------------------------------

MUTATION = os.path.join(HERE, 'mutation-test.sh')
SHELL_SCRIPTS = ['mutation-test.sh', 'ci-check.sh', 'msgmerge-compat.sh']


def run_mutation(fault=None, tmpdir=None, timeout=300):
    env = dict(os.environ)
    if fault: env['BATHRON_MUTATION_TEST_FAULT'] = fault
    if tmpdir: env['TMPDIR'] = tmpdir
    return subprocess.run(['bash', MUTATION], cwd=REPO, env=env, timeout=timeout,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          universal_newlines=True)


class TestMutationHarness(unittest.TestCase):
    FAULTS = ['manifest', 'sandbox', 'copy', 'guard', 'skipguard']

    def test_nominal_run_passes(self):
        r = run_mutation()
        self.assertEqual(r.returncode, 0, r.stdout[-2000:])
        self.assertIn('MUTATION TEST: PASS', r.stdout)

    def test_every_injected_fault_fails_and_never_prints_pass(self):
        for fault in self.FAULTS:
            with self.subTest(fault=fault):
                r = run_mutation(fault=fault)
                self.assertNotEqual(r.returncode, 0,
                                    f'fault {fault!r} still exited 0:\n{r.stdout[-2000:]}')
                self.assertNotIn('MUTATION TEST: PASS', r.stdout,
                                 f'fault {fault!r} reported PASS:\n{r.stdout[-2000:]}')

    def test_skipped_checks_are_caught_by_the_assertion_counter(self):
        """The original defect: guarded-file checks silently do not run."""
        r = run_mutation(fault='skipguard')
        self.assertEqual(r.returncode, 3)
        self.assertIn('assertions ran, expected', r.stdout)

    def test_sandbox_lives_under_tmpdir_and_is_removed(self):
        d = tempfile.mkdtemp(prefix='i18n-tmpdir-')
        self.addCleanup(shutil.rmtree, d, True)
        r = run_mutation(tmpdir=d)
        self.assertEqual(r.returncode, 0, r.stdout[-2000:])
        self.assertIn(d, r.stdout, 'the sandbox did not honour TMPDIR')
        self.assertEqual(os.listdir(d), [], 'the sandbox was not cleaned up')

    def test_cleanup_removes_only_its_own_sandbox(self):
        """A decoy matching the prefix but lacking the marker must survive."""
        d = tempfile.mkdtemp(prefix='i18n-tmpdir-')
        self.addCleanup(shutil.rmtree, d, True)
        decoy = os.path.join(d, 'bathron-i18n-mutation.DECOY')
        os.makedirs(decoy)
        with open(os.path.join(decoy, 'precious.txt'), 'w') as f:
            f.write('do not delete me')
        r = run_mutation(tmpdir=d)
        self.assertEqual(r.returncode, 0, r.stdout[-2000:])
        self.assertTrue(os.path.isdir(decoy), 'the decoy directory was removed')
        with open(os.path.join(decoy, 'precious.txt')) as f:
            self.assertEqual(f.read(), 'do not delete me')
        self.assertEqual(os.listdir(d), ['bathron-i18n-mutation.DECOY'])


class TestShellPortability(unittest.TestCase):
    """No Bash 4+ construct, and no tool a stock macOS lacks."""

    BASH4_ONLY = [
        (r'declare\s+-A', 'associative array (Bash 4+)'),
        (r'local\s+-A', 'associative array (Bash 4+)'),
        (r'\bmapfile\b', 'mapfile (Bash 4+)'),
        (r'\breadarray\b', 'readarray (Bash 4+)'),
        (r'\$\{[A-Za-z_][A-Za-z0-9_]*\^\^', 'uppercase expansion (Bash 4+)'),
        (r'\$\{[A-Za-z_][A-Za-z0-9_]*,,', 'lowercase expansion (Bash 4+)'),
        (r';;&', 'fallthrough case (Bash 4+)'),
    ]
    MISSING_ON_MACOS = [(r'\bsha256sum\b', 'sha256sum is not on a stock macOS')]

    def code_lines(self, name):
        """Lines that are not comments — comments may name a construct."""
        path = os.path.join(HERE, name)
        out = []
        with open(path, encoding='utf-8') as fh:
            for i, line in enumerate(fh, 1):
                stripped = line.lstrip()
                if stripped.startswith('#'): continue
                out.append((i, line))
        return out

    def test_no_bash4_only_constructs(self):
        import re as _re
        for name in SHELL_SCRIPTS:
            for lineno, line in self.code_lines(name):
                for pattern, why in self.BASH4_ONLY:
                    with self.subTest(script=name, line=lineno, why=why):
                        self.assertIsNone(_re.search(pattern, line),
                                          f'{name}:{lineno} uses {why}: {line.strip()!r}')

    def test_no_tools_absent_from_macos(self):
        import re as _re
        for name in SHELL_SCRIPTS:
            for lineno, line in self.code_lines(name):
                for pattern, why in self.MISSING_ON_MACOS:
                    with self.subTest(script=name, line=lineno):
                        self.assertIsNone(_re.search(pattern, line),
                                          f'{name}:{lineno}: {why}: {line.strip()!r}')

    def test_scripts_are_executable_and_have_a_shebang(self):
        for name in SHELL_SCRIPTS:
            path = os.path.join(HERE, name)
            with self.subTest(script=name):
                with open(path, encoding='utf-8') as f:
                    self.assertEqual(f.readline().rstrip(), '#!/usr/bin/env bash')
                self.assertTrue(os.access(path, os.X_OK), f'{name} is not executable')


if __name__ == '__main__':
    unittest.main(verbosity=2)
