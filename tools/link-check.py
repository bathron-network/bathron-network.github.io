#!/usr/bin/env python3
"""Built-site links, fragments, direct redirects, images and pinned sources.

Never fetches anything. Source verification reads a supplied local git checkout
at exactly NSPEC_REF. CI prepares that checkout before calling the gates.
"""
import argparse
import html
import os
import posixpath
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit
from common import ROOT, SITE, LEGACY_PATHS, entries, parse_html, redirects, report, summary, tracked

PREFIX = 'https://github.com/bathron-network/n-spec/blob/'
APP = 'app/APP-SPEC-v1-draft.md'
APP_SECTIONS = {'04-vocabulaire-et-identifiants-gelés', 'id-identifiant-applicatif-application_spec_id',
                '13-règlement-btcm0-à-un-saut', 'r2p-r2-pivot--durée-de-vie-minimale-réelle-des-contrats-enfants',
                '03-catégories-et-verdicts', 'btc-faits-bitcoin-applicatifs',
                'scr1-socle-actif-au-genesis', 'scr2-échéances-absolues-en-créneaux-n-cltv',
                'scr3-délais-relatifs-en-liens-n-csv', 'scr4-limites-publiées-des-délais',
                'scr5-ctv', 'scr7-btcstate', 'obj3-anciens-types-refusés-et-numéros-réservés',
                '131-contrat', '132-création-objet-0004', '133-paiement', '134-résolution',
                '135-discipline-du-payeur-politique-client', '136-rollback',
                'pub-publications-obligatoires', 'imp1-source-unique', 'imp4-matérialisation',
                'obj2-transaction-applicative-application_transaction'}


def revision(root=ROOT):
    rows = [s.strip() for s in (root / 'docs/NSPEC_REF').read_text().splitlines() if s.strip() and not s.startswith('#')]
    if len(rows) != 1:
        raise ValueError('NSPEC_REF must have exactly one value')
    return rows[0]


def redirect_check(root=ROOT):
    errors = []
    expected = {'status.md', 'overview.md', 'trust.md', 'engine.md', 'producers.md',
                'depth.md', 'burns.md', 'roles.md', 'glossary.md',
                'bitcoin-facts.md', 'covenants.md', 'settlement.md',
                'between-providers.md', 'what-you-can-build.md'}
    names = summary(root)
    actual = {p.name for p in (root / 'docs/src').glob('*.md')}
    if len(names) != len(expected) or set(names) != expected or actual != expected | {'SUMMARY.md'}:
        errors.append('book scope: expected exactly thirteen pages, Status and SUMMARY')
    pages = {p.removesuffix('.md') + '.html' for p in names}
    table = redirects(root)
    for key, target in table.items():
        dest = posixpath.normpath(posixpath.join(posixpath.dirname(key), target)).lstrip('/')
        if dest not in pages or '#' in target or urlsplit(target).scheme:
            errors.append(f'redirect {key}: target must be a SUMMARY page, without a chain or fragment')
        if key.lstrip('/') in pages:
            errors.append(f'redirect {key}: collides with a rendered page')
    return errors


def site_files(root):
    result = {'/index.html': root / 'index.html'}
    for path in LEGACY_PATHS:
        result['/' + path + '/index.html'] = root / path / 'index.html'
    for path in (root / 'docs/book').rglob('*'):
        if path.is_file():
            result['/docs/' + path.relative_to(root / 'docs/book').as_posix()] = path
    for path in (root / 'img').rglob('*'):
        if path.is_file():
            result['/img/' + path.relative_to(root / 'img').as_posix()] = path
    return result


def links(root=ROOT):
    errors = []
    files = site_files(root)
    documents = {}
    for url, path in files.items():
        if not path.is_file():
            errors.append(f'{url}: missing generated page')
        elif path.suffix == '.html':
            documents[url] = parse_html(path.read_text())
    for name in summary(root):
        if '/docs/' + name.removesuffix('.md') + '.html' not in documents:
            errors.append(f'{name}: book has not been built')
    for url, doc in documents.items():
        for link in doc.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                if parsed.netloc != urlsplit(SITE).netloc:
                    continue
            dest = unquote(parsed.path)
            if not dest:
                dest = url
            elif not dest.startswith('/'):
                dest = posixpath.join(posixpath.dirname(url), dest)
            if dest.endswith('/'):
                dest += 'index.html'
            dest = posixpath.normpath(dest)
            if dest not in files or not files[dest].exists():
                errors.append(f'{url}: missing internal destination {link}')
            elif parsed.fragment and (dest not in documents or unquote(parsed.fragment) not in documents[dest].ids):
                errors.append(f'{url}: missing anchor {link}')
    # mdBook emits redirects as HTML; verify their actual refresh destinations.
    for key, target in redirects(root).items():
        path = root / 'docs/book' / key.lstrip('/')
        if not path.is_file() or f'url={target}'.lower() not in path.read_text().lower():
            errors.append(f'{key}: missing or stale built redirect')
    return errors


def images(root=ROOT):
    errors = []
    sources = [root / 'index.html'] + list((root / 'docs/src').glob('*.md'))
    content = '\n'.join(p.read_text() for p in sources)
    for directory in ('img', 'docs/src/img'):
        for path in (root / directory).rglob('*'):
            if path.is_file() and path.stem not in {'favicon', 'emblem', 'wordmark', 'og'}:
                if path.name not in content:
                    errors.append(f'{path.relative_to(root)}: unreferenced image')
    return errors


def source_paths(root):
    paths = [root / 'index.html', root / 'README.md', root / 'docs/STYLE.md']
    paths += list((root / 'docs/src').glob('*.md'))
    paths += [root / path / 'index.html' for path in LEGACY_PATHS]
    return [path for path in paths if path.is_file()]


def source_links(root):
    for path in source_paths(root):
        for match in re.finditer(r'https://github\.com/bathron-network/n-spec/(?:blob|tree)/[^\s<>"\)]+', path.read_text()):
            yield path.relative_to(root).as_posix(), match.group().rstrip('.,;')


def citation_labels(root):
    for path in source_paths(root):
        text = path.read_text()
        if path.suffix == '.md':
            definitions = dict(re.findall(r'^\[([^\]]+)\]:\s*(\S+)', text, re.M))
            links = []
            for match in re.finditer(r'\[([^\]]+)\](?:\(([^)]+)\)|\[([^\]]+)\])', text):
                label, inline, reference = match.groups()
                links.append((inline or definitions.get(reference, ''), label))
        else:
            links = [(url, html.unescape(re.sub(r'<[^>]+>', '', label)))
                     for url, label in re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', text, re.S)]
        for url, label in links:
            if url.startswith(PREFIX):
                yield path.relative_to(root).as_posix(), url, label


def citation_check(root):
    errors = []
    for page, url, label in citation_labels(root):
        anchor = unquote(urlsplit(url).fragment)
        for section in re.findall(r'§+\s*([0-9]+(?:\.[0-9]+)*|(?:ID|R2P|BTC|SCR|OBJ|PUB|IMP)(?:\.[0-9]+)*)', label):
            identifier = section.lower().replace('.', '')
            if not anchor.startswith(identifier + '-') and anchor != identifier:
                errors.append(f'{page}: section label §{section} disagrees with normative anchor')
    return errors


def slug(text):
    text = re.sub(r'<[^>]*>', '', text).lower()
    text = re.sub(r'[^\w\s-]', '', text, flags=re.UNICODE)
    return text.replace(' ', '-')


def sections(text):
    """GitHub heading anchors, including disambiguation and child subsections."""
    headings = []
    counts = {}
    fence = False
    for match in re.finditer(r'^.*$', text, re.M):
        line = match.group()
        if re.match(r'\s*(```|~~~)', line):
            fence = not fence
        heading = re.match(r'^(#{1,6})\s+(.+?)(?:\s+#+)?$', line)
        if heading and not fence:
            anchor = slug(heading[2])
            count = counts.get(anchor, 0)
            counts[anchor] = count + 1
            if count:
                anchor += '-' + str(count)
            headings.append((anchor, len(heading[1]), match.start()))
    result = {}
    for i, (anchor, level, start) in enumerate(headings):
        end = next((offset for _, depth, offset in headings[i+1:] if depth <= level), len(text))
        result[anchor] = text[start:end]
    return result


def sources(root=ROOT, checkout=None):
    errors = citation_check(root)
    ref = revision(root)
    if not re.fullmatch(r'[0-9a-f]{40}', ref):
        return errors + ['sources: TODO-REF — a full merge commit containing app/ is required']
    if not checkout or not Path(checkout).is_dir():
        return errors + ['sources: a local n-spec git checkout is required (NSPEC_DIR); nothing is fetched by this check']
    checkout = Path(checkout)
    def read(name):
        result = subprocess.run(['git', 'show', f'{ref}:{name}'], cwd=checkout, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else None
    if read(APP) is None:
        errors.append('sources: pinned revision does not contain the curated application specification')
    allow = entries('nspec-oldname-exceptions.txt', root)
    cache = {}
    for page, url in source_links(root):
        if not url.startswith(PREFIX + ref + '/'):
            errors.append(f'{page}: normative URL does not use NSPEC_REF')
            continue
        part = urlsplit(url[len(PREFIX + ref + '/'):])
        name, anchor = unquote(part.path), unquote(part.fragment)
        if name not in {'README.md', 'spec/N-SPEC-v0.7.md', 'docs/WHY-N.md', 'docs/ATTACKS.md', APP}:
            errors.append(f'{page}: source outside permitted public scope: {name}')
            continue
        if name == 'spec/N-SPEC-v0.7.md' and (not anchor or re.match(r'^13(?:-|\d)', anchor)):
            errors.append(f'{page}: engine settlement chapter or unscoped engine citation is forbidden')
            continue
        if name == APP and anchor not in APP_SECTIONS:
            errors.append(f'{page}: application section outside permitted scope')
            continue
        if name not in cache:
            cache[name] = read(name)
        text = cache[name]
        if text is None:
            errors.append(f'{page}: missing pinned source {name}')
            continue
        if anchor:
            text = sections(text).get(anchor)
            if text is None:
                errors.append(f'{page}: missing normative anchor {name}#{anchor}')
                continue
        if re.search(r'\bM1\b', text) and not any(a['page'] == page and a['section'] == name + ('#' + anchor if anchor else '') for a in allow):
            errors.append(f'{page}: historical wording needs a scoped exception for {name}#{anchor}')
    return errors


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--only', choices=['links', 'redirects', 'images', 'sources'])
    p.add_argument('--nspec-dir', default=os.getenv('NSPEC_DIR'))
    args = p.parse_args()
    checks = {'links': links, 'redirects': redirect_check, 'images': images, 'sources': lambda: sources(checkout=args.nspec_dir)}
    errors = []
    for label, check in checks.items():
        if args.only is None or args.only == label:
            errors += check()
    raise SystemExit(report(errors, args.only or 'links and sources'))
