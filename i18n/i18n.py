#!/usr/bin/env python3
"""BATHRON homepage i18n — single structural source, GNU gettext catalogues.

index.html is the canonical source: structure AND English text, and it is the
page served at /. Translatable segments are the text nodes and a whitelist of
attributes. <style> and <script> are never translatable.

  extract       -> i18n/homepage.pot   (generated, gitignored)
  check  <lang> -> fail-closed audit of a catalogue against the current source
  build  <lang> -> <lang>/index.html   (generated artifact, gitignored)
  verify <lang> -> structural facts of the page actually served for <lang>
  compare       -> EN/FR tag-skeleton equivalence
  static-overflow-check
                -> static scan for fixed widths wider than the smallest
                   viewport. NOT a rendering check: it does not lay the page
                   out. Browser verification stays a local editorial step.

Disambiguation: when one English string needs two different translations
depending on where it appears, wrap the element in data-i18n-context="<name>".
That becomes the gettext msgctxt.

  NOTE — the attribute is stripped from every GENERATED page (fr/index.html).
  The English page is served straight from index.html and therefore KEEPS the
  attribute. data-* is valid HTML5 and inert; see i18n/README.md, "Context
  metadata", for why that model was chosen over generating an English copy.

No framework, no runtime JS, no network, no AI. Deterministic.
"""
import sys, os, re, html, tempfile
from html.parser import HTMLParser

ROOT = os.path.realpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, 'index.html')
POT = os.path.join(ROOT, 'i18n', 'homepage.pot')

SKIP_TAGS = {'style', 'script'}
# attributes whose value is prose and must be translated
ATTRS = {('meta', 'content'), ('img', 'alt'), ('a', 'title'), ('html', 'lang')}
# only these meta names/properties carry prose. viewport, og:image, og:url,
# twitter:card and friends are structural and must never reach the catalogue.
META_PROSE = {'description', 'og:title', 'og:description', 'twitter:description', 'twitter:title'}
CTX_ATTR = 'data-i18n-context'
# Void elements have no end tag, so they must never push onto the context
# stack — otherwise the stack leaks and later strings inherit a stale context.
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta',
        'param', 'source', 'track', 'wbr',
        'path', 'circle', 'rect', 'line', 'polygon', 'use', 'stop'}

# Per-language values that are NOT prose: they are structural facts about the page.
LANG_CONF = {
    'en': {
        'lang': 'en',
        'canonical': 'https://bathron.org/',
        # The whole <nav> is a per-language structural fact, aria-label
        # included: it names a navigation control, not page prose, so it stays
        # out of the catalogue like the canonical URL does.
        'sel': ('<nav class="langsel" aria-label="Language selection">'
                '<span aria-current="page" lang="en">EN</span>'
                '<a href="/fr/" hreflang="fr" lang="fr">FR</a></nav>'),
    },
    'fr': {
        'lang': 'fr',
        'canonical': 'https://bathron.org/fr/',
        'sel': ('<nav class="langsel" aria-label="Sélection de la langue">'
                '<a href="/" hreflang="en" lang="en">EN</a>'
                '<span aria-current="page" lang="fr">FR</span></nav>'),
    },
}
# Where each language is served, used to check the other-language link target.
LANG_HREF = {'en': '/', 'fr': '/fr/'}
SELECTOR_RE = r'<nav class="langsel".*?</nav>'

# English is the source, not a generated artifact. Only these are built.
GENERATED_LANGS = {'fr'}
# Narrowest viewport the layout is expected to survive, in CSS pixels.
MIN_VIEWPORT_PX = 390


class I18nError(Exception):
    """Base class — every failure path raises, nothing fails silently."""


class LangError(I18nError): pass
class PathError(I18nError): pass
class PoError(I18nError): pass
class BuildError(I18nError): pass


# --------------------------------------------------------------------------
# Language and path bounding. Validated BEFORE any path is computed and before
# any file is read, created or removed.
# --------------------------------------------------------------------------

LANG_RE = re.compile(r'^[a-z]{2}$')


def validate_lang(lang):
    """Accept only a language declared in LANG_CONF. Raises before any I/O."""
    if not isinstance(lang, str):
        raise LangError(f'language must be a string, got {type(lang).__name__}')
    if not LANG_RE.match(lang):
        raise LangError(f'invalid language code {lang!r}: expected two lowercase letters')
    if lang not in LANG_CONF:
        known = ', '.join(sorted(LANG_CONF))
        raise LangError(f'unknown language {lang!r}: known languages are {known}')
    return lang


def _bounded(path, must_be):
    """Resolve `path` and require it to be exactly `must_be`, inside ROOT."""
    real = os.path.realpath(path)
    expected = os.path.realpath(must_be)
    if real != expected:
        raise PathError(f'resolved path {real!r} is not the expected {expected!r}')
    if real != ROOT and os.path.commonpath([ROOT, real]) != ROOT:
        raise PathError(f'resolved path {real!r} escapes the repository root {ROOT!r}')
    return real


def lang_dir(lang):
    """Output directory for a generated language, strictly <repo>/<lang>/."""
    validate_lang(lang)
    if lang not in GENERATED_LANGS:
        raise LangError(f'{lang!r} is not a generated language '
                        f'(generated: {", ".join(sorted(GENERATED_LANGS))})')
    return _bounded(os.path.join(ROOT, lang), os.path.join(ROOT, lang))


def out_path(lang):
    """<repo>/<lang>/index.html for a generated language."""
    d = lang_dir(lang)
    p = os.path.join(d, 'index.html')
    if os.path.dirname(os.path.realpath(os.path.join(d, 'index.html'))) != d:
        raise PathError(f'output path escapes {d!r}')
    return p


def served_path(lang):
    """The file actually served for `lang`: index.html for English."""
    validate_lang(lang)
    return SRC if lang == 'en' else out_path(lang)


def po_path(lang):
    """<repo>/i18n/homepage.<lang>.po, bounded to the i18n directory."""
    validate_lang(lang)
    want = os.path.join(ROOT, 'i18n', f'homepage.{lang}.po')
    return _bounded(want, want)


# --------------------------------------------------------------------------
# HTML walking
# --------------------------------------------------------------------------

def norm(s):
    return ' '.join(s.split())


class Walker(HTMLParser):
    """Rebuilds the document, calling on_text/on_attr for translatable parts.

    Text is buffered ACROSS entity references so "Bitcoin&rsquo;s chain." is ONE
    translatable string, not three fragments. Each buffer item is
    (raw_source, plain_text): raw is re-emitted verbatim when the string comes
    back unchanged, which keeps the English round-trip byte-identical.
    """

    def __init__(self, on_text, on_attr, strip_ctx=True):
        super().__init__(convert_charrefs=False)
        self.out, self.skip = [], 0
        self.on_text, self.on_attr = on_text, on_attr
        self.strip_ctx = strip_ctx
        self.buf, self.ctx = [], ['']

    def _flush(self):
        if not self.buf: return
        raw = ''.join(r for r, _ in self.buf)
        plain = ''.join(p for _, p in self.buf)
        self.buf = []
        if self.skip or not norm(plain):
            self.out.append(raw); return
        new = self.on_text(plain, self.ctx[-1])
        self.out.append(raw if new == plain else html.escape(new, quote=False))

    def handle_starttag(self, tag, attrs, selfclosing=False):
        self._flush()
        if tag in SKIP_TAGS: self.skip += 1
        d = {k: v for k, v in attrs}
        mname = d.get('name') or d.get('property')
        own = d.get(CTX_ATTR)
        ctx = own if own else self.ctx[-1]
        parts = []
        for k, v in attrs:
            if k == CTX_ATTR and self.strip_ctx: continue
            if v is None: parts.append(f' {k}'); continue
            parts.append(f' {k}="{self.on_attr(tag, k, v, mname, ctx)}"')
        self.out.append(f'<{tag}{"".join(parts)}{" /" if selfclosing else ""}>')
        if not selfclosing and tag not in VOID:
            self.ctx.append(ctx)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs, selfclosing=True)

    def handle_endtag(self, tag):
        self._flush()
        if tag in SKIP_TAGS: self.skip = max(0, self.skip - 1)
        if tag not in VOID and len(self.ctx) > 1: self.ctx.pop()
        self.out.append(f'</{tag}>')

    def handle_data(self, d): self.buf.append((d, d))
    def handle_entityref(self, n): self.buf.append((f'&{n};', html.unescape(f'&{n};')))
    def handle_charref(self, n): self.buf.append((f'&#{n};', html.unescape(f'&#{n};')))
    def handle_comment(self, c): self._flush(); self.out.append(f'<!--{c}-->')
    def handle_decl(self, d): self._flush(); self.out.append(f'<!{d}>')
    def handle_pi(self, d): self._flush(); self.out.append(f'<?{d}>')
    def unknown_decl(self, d): self._flush(); self.out.append(f'<![{d}]>')
    def close(self): super().close(); self._flush()

    @property
    def document(self):
        return ''.join(self.out)


def collect(src):
    """Ordered, de-duplicated list of (context, english) keys."""
    seen, order = set(), []

    def keep(s, ctx):
        k = (ctx, norm(s))
        if k[1] and k not in seen:
            seen.add(k); order.append(k)

    def text(d, ctx): keep(d, ctx); return d

    def attr(tag, k, v, name=None, ctx=''):
        if tag == 'meta':
            if k == 'content' and name in META_PROSE and norm(v): keep(v, ctx)
            return v
        if (tag, k) in ATTRS and (tag, k) != ('html', 'lang') and norm(v): keep(v, ctx)
        return v

    w = Walker(text, attr); w.feed(src); w.close()
    return order


# --------------------------------------------------------------------------
# Strict PO reader — fail-closed. An ambiguous catalogue is a rejected
# catalogue: a silently overwritten entry is a silently wrong page.
# --------------------------------------------------------------------------

VALID_ESCAPES = set('\\"nrtabf/')


def po_unescape(s, lineno):
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c != '\\':
            if c == '"':
                raise PoError(f'line {lineno}: unescaped quote inside a string')
            out.append(c); i += 1; continue
        if i + 1 >= len(s):
            raise PoError(f'line {lineno}: string ends with a dangling backslash')
        nxt = s[i + 1]
        if nxt not in VALID_ESCAPES:
            raise PoError(f'line {lineno}: invalid escape \\{nxt}')
        out.append({'n': '\n', 'r': '\r', 't': '\t', 'a': '\a', 'b': '\b',
                    'f': '\f'}.get(nxt, nxt))
        i += 2
    return ''.join(out)


def po_escape(s):
    return (s.replace('\\', '\\\\').replace('"', '\\"')
             .replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r'))


_PO_KV = re.compile(r'^(msgctxt|msgid|msgstr)[ \t]+"(.*)"[ \t]*$')
_PO_CONT = re.compile(r'^"(.*)"[ \t]*$')


def read_po(path, expect_lang=None):
    """Parse a .po file strictly. Returns (entries, flags).

    Keys are (msgctxt, msgid) tuples, msgctxt is '' when absent. Raises PoError
    on anything ambiguous, duplicated, incomplete or unrecognised.
    """
    if not os.path.exists(path):
        raise PoError(f'catalogue not found: {path}')
    entries, flags = {}, {}
    header_seen = 0
    cur = {'ctx': None, 'id': None, 'str': None, 'flags': [], 'start': 0}
    mode = None

    def finish(lineno):
        nonlocal cur, mode, header_seen
        if cur['id'] is None and cur['str'] is None and cur['ctx'] is None:
            if cur['flags']:
                raise PoError(f'line {lineno}: flags attached to no entry')
            cur = {'ctx': None, 'id': None, 'str': None, 'flags': [], 'start': 0}
            mode = None
            return
        if cur['id'] is None:
            raise PoError(f'line {cur["start"]}: entry has no msgid')
        if cur['str'] is None:
            raise PoError(f'line {cur["start"]}: entry for msgid {cur["id"][:40]!r} has no msgstr')
        if cur['ctx'] is not None and cur['id'] == '':
            raise PoError(f'line {cur["start"]}: header entry must not carry a msgctxt')
        key = (cur['ctx'] or '', cur['id'])
        if key == ('', ''):
            header_seen += 1
            if header_seen > 1:
                raise PoError(f'line {cur["start"]}: duplicate header entry')
            if expect_lang is not None:
                m = re.search(r'^Language:[ \t]*([A-Za-z_-]+)', cur['str'] or '', re.M)
                if not m:
                    raise PoError('header declares no "Language:" field')
                declared = m.group(1).split('_')[0].split('-')[0].lower()
                if declared != expect_lang:
                    raise PoError(f'catalogue declares Language: {m.group(1)!r} '
                                  f'but {expect_lang!r} was requested')
        else:
            if header_seen == 0:
                raise PoError(f'line {cur["start"]}: entry appears before the header entry')
            if key in entries:
                ctx = f'msgctxt {key[0]!r} + ' if key[0] else ''
                raise PoError(f'line {cur["start"]}: duplicate entry for {ctx}msgid {key[1][:60]!r}')
            entries[key] = cur['str']
            flags[key] = list(cur['flags'])
        cur = {'ctx': None, 'id': None, 'str': None, 'flags': [], 'start': 0}
        mode = None

    with open(path, encoding='utf-8') as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.rstrip('\n').rstrip('\r')
            if not line.strip():
                finish(lineno); continue
            if line.startswith('#~'):
                raise PoError(f'line {lineno}: obsolete entry (#~) — catalogue not synchronised')
            if line.startswith('#'):
                if line.startswith('#,'):
                    if cur['id'] is not None or cur['str'] is not None:
                        raise PoError(f'line {lineno}: flag line inside an entry')
                    cur['flags'] = [x.strip() for x in line[2:].split(',') if x.strip()]
                continue
            m = _PO_KV.match(line)
            if m:
                kind, val = m.group(1), po_unescape(m.group(2), lineno)
                if cur[{'msgctxt': 'ctx', 'msgid': 'id', 'msgstr': 'str'}[kind]] is not None:
                    raise PoError(f'line {lineno}: repeated {kind} in a single entry')
                if kind == 'msgctxt' and (cur['id'] is not None or cur['str'] is not None):
                    raise PoError(f'line {lineno}: msgctxt must come first in an entry')
                if kind == 'msgid' and cur['str'] is not None:
                    raise PoError(f'line {lineno}: msgid after msgstr')
                if not cur['start']: cur['start'] = lineno
                cur[{'msgctxt': 'ctx', 'msgid': 'id', 'msgstr': 'str'}[kind]] = val
                mode = {'msgctxt': 'ctx', 'msgid': 'id', 'msgstr': 'str'}[kind]
                continue
            m = _PO_CONT.match(line)
            if m:
                if mode is None:
                    raise PoError(f'line {lineno}: continuation string with no msgid/msgstr/msgctxt above it')
                cur[mode] += po_unescape(m.group(1), lineno)
                continue
            raise PoError(f'line {lineno}: unrecognised line {line[:60]!r}')
    finish(lineno + 1 if 'lineno' in dir() else 1)
    if header_seen == 0:
        raise PoError('catalogue has no header entry (msgid "" / msgstr "")')
    return entries, flags


def write_pot(keys, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('# BATHRON homepage — GENERATED, DO NOT EDIT BY HAND, NOT VERSIONED.\n'
                '# Regenerate with: python3 i18n/i18n.py extract\n'
                'msgid ""\nmsgstr ""\n'
                '"Content-Type: text/plain; charset=UTF-8\\n"\n'
                '"Content-Transfer-Encoding: 8bit\\n"\n\n')
        for ctx, s in keys:
            if ctx: f.write(f'msgctxt "{po_escape(ctx)}"\n')
            f.write(f'msgid "{po_escape(s)}"\nmsgstr ""\n\n')


# --------------------------------------------------------------------------
# check / build
# --------------------------------------------------------------------------

def fmt(k):
    return f'[{k[0]}] {k[1]}' if k[0] else k[1]


def check(lang, verbose=True):
    """Fail-closed audit. Returns a list of (kind, description) problems."""
    validate_lang(lang)
    if lang not in GENERATED_LANGS:
        raise LangError(f'{lang!r} is the source language and has no catalogue')
    po = po_path(lang)
    with open(SRC, encoding='utf-8') as fh:
        need = collect(fh.read())
    try:
        entries, flags = read_po(po, expect_lang=lang)
    except PoError as e:
        problems = [('CATALOGUE', str(e))]
        if verbose:
            print(f'  catalogue        : {po}')
            print(f'  problems         : 1')
            print(f'    CATALOGUE       {e}')
        return problems
    problems = []
    for k in need:
        if k not in entries: problems.append(('MISSING', fmt(k)))
        elif not entries[k].strip(): problems.append(('EMPTY', fmt(k)))
        elif 'fuzzy' in flags.get(k, []): problems.append(('FUZZY', fmt(k)))
    need_set = set(need)
    for k in entries:
        if k not in need_set: problems.append(('OBSOLETE', fmt(k)))
    if verbose:
        print(f'  source strings   : {len(need)}')
        print(f'  catalogue        : {po}')
        print(f'  entries          : {len(entries)}')
        print(f'  problems         : {len(problems)}')
        for kind, s in problems[:20]:
            print(f'    {kind:15} {s[:88]}')
    return problems


def _sub_once(pattern, repl, text, what):
    text, n = re.subn(pattern, lambda _m: repl, text, flags=re.S)
    if n != 1:
        raise BuildError(f'expected exactly 1 {what} in the source, found {n}')
    return text


def render(lang, src=None, entries=None):
    """Produce the translated document as a string. Raises on any anomaly."""
    validate_lang(lang)
    if src is None:
        with open(SRC, encoding='utf-8') as fh:
            src = fh.read()
    if entries is None:
        entries, _ = read_po(po_path(lang), expect_lang=lang)
    conf = LANG_CONF[lang]

    def text(d, ctx):
        n = norm(d)
        if (ctx, n) in entries:
            lead = d[:len(d) - len(d.lstrip())]
            trail = d[len(d.rstrip()):]
            return lead + entries[(ctx, n)] + trail
        return d

    def attr(tag, k, v, name=None, ctx=''):
        if (tag, k) == ('html', 'lang'): return conf['lang']
        if tag == 'meta':
            if k == 'content' and name in META_PROSE and (ctx, norm(v)) in entries:
                return entries[(ctx, norm(v))]
            return v
        if (tag, k) in ATTRS and (ctx, norm(v)) in entries: return entries[(ctx, norm(v))]
        return v

    w = Walker(text, attr); w.feed(src); w.close()
    doc = w.document
    # language-dependent structural facts, each applied exactly once
    doc = _sub_once(r'<meta property="og:url" content="[^"]*">',
                    f'<meta property="og:url" content="{conf["canonical"]}">', doc, 'og:url meta')
    doc = _sub_once(r'<link rel="canonical"[^>]*>',
                    f'<link rel="canonical" href="{conf["canonical"]}">', doc, 'canonical link')
    doc = _sub_once(SELECTOR_RE, conf['sel'], doc, 'language selector')
    return doc


def build(lang):
    """Generate <lang>/index.html atomically. Never writes on an incomplete
    catalogue, and never leaves a stale or partial artifact behind."""
    try:
        validate_lang(lang)
        if lang not in GENERATED_LANGS:
            raise LangError(f'{lang!r} is served directly from index.html and is not generated')
        out = out_path(lang)
    except I18nError as e:
        print(f'  REFUSED: {e}')
        return 2
    # 1. remove any previous artifact BEFORE validating, so a failed build can
    #    never leave yesterday's page in place.
    if os.path.exists(out):
        os.remove(out); print(f'  removed stale artifact {lang}/index.html')
    problems = check(lang, verbose=False)
    if problems:
        print(f'  BUILD REFUSED for {lang}: {len(problems)} problem(s)')
        for kind, s in problems[:20]: print(f'    {kind:15} {s[:88]}')
        return 1
    try:
        doc = render(lang)
    except I18nError as e:
        print(f'  BUILD REFUSED for {lang}: {e}')
        return 1
    # 2. atomic publish: write to a temporary file in the SAME directory, fsync,
    #    then rename over the target. A killed process leaves either the old
    #    file or no file — never a half-written page.
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = None
    try:
        fd, tmp = tempfile.mkstemp(dir=os.path.dirname(out), prefix='.index.html.',
                                   suffix='.tmp')
        with os.fdopen(fd, 'w', encoding='utf-8') as fh:
            fh.write(doc); fh.flush(); os.fsync(fh.fileno())
        os.replace(tmp, out)
        tmp = None
    finally:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)
    if not os.path.exists(out):
        print(f'  BUILD FAILED: {out} was not created'); return 1
    print(f'  built {lang}/index.html ({os.path.getsize(out)} bytes)')
    return 0


# --------------------------------------------------------------------------
# Structural verification — the same checks the deploy workflow runs.
# --------------------------------------------------------------------------

class Skeleton(HTMLParser):
    """Tag skeleton, balance, duplicate ids, and structural attributes."""
    KEEP = ('class', 'href', 'src', 'rel', 'property', 'name', 'target')

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags, self.stack, self.ids, self.errors = [], [], [], []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if 'id' in d: self.ids.append(d['id'])
        keep = tuple(sorted((k, v) for k, v in d.items() if k in self.KEEP))
        self.tags.append((tag, keep))
        if tag not in VOID: self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in VOID: return
        if not self.stack:
            self.errors.append(f'</{tag}> at {self.getpos()} closes nothing'); return
        opened, pos = self.stack.pop()
        if opened != tag:
            self.errors.append(f'</{tag}> at {self.getpos()} closes <{opened}> opened at {pos}')


def parse_skeleton(path):
    with open(path, encoding='utf-8') as fh:
        s = Skeleton(); s.feed(fh.read()); s.close()
    for tag, pos in s.stack:
        s.errors.append(f'<{tag}> opened at {pos} is never closed')
    dups = sorted({i for i in s.ids if s.ids.count(i) > 1})
    for i in dups: s.errors.append(f'duplicate id {i!r}')
    return s


def _check_selector(doc, lang, problems):
    """The language selector must be present exactly once, in the top bar,
    with the right language active and the right target for the other one."""
    conf = LANG_CONF[lang]
    other = 'fr' if lang == 'en' else 'en'

    navs = re.findall(SELECTOR_RE, doc, flags=re.S)
    if len(navs) != 1:
        problems.append(('COUNT', f'language selector: expected exactly 1, found {len(navs)}'))
        return
    nav = navs[0]
    if doc.count('class="langsel"') != 1:
        problems.append(('COUNT', 'the langsel class appears more than once'))
    if nav != conf['sel']:
        problems.append(('SELECTOR', f'selector markup differs from LANG_CONF[{lang!r}]:\n'
                                     f'      got      {nav}\n      expected {conf["sel"]}'))

    # only real attributes on tags — the CSS rule .langsel [aria-current="page"]
    # is not an occurrence, and counting it would be a false alarm.
    n = len(re.findall(r'<[a-zA-Z][^>]*\baria-current=', doc))
    if n != 1:
        problems.append(('ARIA-CURRENT', f'aria-current appears {n} time(s), expected exactly 1'))

    m = re.search(r'<(\w+)([^>]*)aria-current="page"([^>]*)>([^<]*)</\1>', nav)
    if not m:
        problems.append(('ARIA-CURRENT', 'no element in the selector carries aria-current="page"'))
    else:
        tag, text = m.group(1), m.group(4).strip()
        if tag == 'a':
            problems.append(('SELECTOR', 'the active language must not be a link'))
        if text != lang.upper():
            problems.append(('SELECTOR', f'active language reads {text!r}, expected {lang.upper()!r}'))

    links = re.findall(r'<a href="([^"]*)" hreflang="([^"]*)" lang="([^"]*)">([^<]*)</a>', nav)
    if len(links) != 1:
        problems.append(('SELECTOR', f'expected exactly 1 link in the selector, found {len(links)}'))
    else:
        href, hl, lg, txt = links[0]
        if href != LANG_HREF[other]:
            problems.append(('SELECTOR', f'other-language link points to {href!r}, '
                                         f'expected {LANG_HREF[other]!r}'))
        if hl != other or lg != other:
            problems.append(('SELECTOR', f'link declares hreflang={hl!r} lang={lg!r}, expected {other!r}'))
        if txt.strip() != other.upper():
            problems.append(('SELECTOR', f'link reads {txt!r}, expected {other.upper()!r}'))

    if re.search(r'<a\b[^>]*>(?:(?!</a>).)*<(?:a|button|select|input)\b', nav, flags=re.S):
        problems.append(('SELECTOR', 'nested interactive element inside the selector'))

    if 'class="topbar"' not in doc:
        problems.append(('SELECTOR', 'no top bar container found'))
    hero = re.search(r'<div class="hero">', doc)
    if hero and doc.index(nav) > hero.start():
        problems.append(('SELECTOR', 'the selector sits inside or after the hero; '
                                     'it belongs to the top bar above it'))


def verify(lang, verbose=True):
    """Check the structural facts of the page actually served for `lang`."""
    validate_lang(lang)
    path = served_path(lang)
    problems = []
    if not os.path.exists(path):
        return [('MISSING-PAGE', f'{path} does not exist')]
    with open(path, encoding='utf-8') as fh:
        doc = fh.read()
    conf = LANG_CONF[lang]

    def one(pattern, what):
        found = re.findall(pattern, doc, flags=re.S)
        if len(found) != 1:
            problems.append(('COUNT', f'{what}: expected exactly 1, found {len(found)}'))
            return None
        return found[0]

    got = one(r'<html lang="([^"]*)"', 'html lang')
    if got is not None and got != conf['lang']:
        problems.append(('LANG', f'html lang is {got!r}, expected {conf["lang"]!r}'))
    got = one(r'<link rel="canonical" href="([^"]*)">', 'canonical link')
    if got is not None and got != conf['canonical']:
        problems.append(('CANONICAL', f'canonical is {got!r}, expected {conf["canonical"]!r}'))
    got = one(r'<meta property="og:url" content="([^"]*)">', 'og:url')
    if got is not None and got != conf['canonical']:
        problems.append(('OG-URL', f'og:url is {got!r}, expected {conf["canonical"]!r}'))
    _check_selector(doc, lang, problems)
    alts = dict(re.findall(r'<link rel="alternate" hreflang="([^"]*)" href="([^"]*)">', doc))
    want = {'en': LANG_CONF['en']['canonical'], 'fr': LANG_CONF['fr']['canonical'],
            'x-default': LANG_CONF['en']['canonical']}
    if alts != want:
        problems.append(('HREFLANG', f'hreflang set is {alts}, expected {want}'))
    skel = parse_skeleton(path)
    for e in skel.errors: problems.append(('HTML', e))
    if lang in GENERATED_LANGS and CTX_ATTR in doc:
        problems.append(('CONTEXT-ATTR', f'{CTX_ATTR} must be stripped from generated pages'))
    if verbose:
        print(f'  {lang}: {path}')
        print(f'    tags {len(skel.tags)}, problems {len(problems)}')
        for kind, s in problems: print(f'      {kind:14} {s[:88]}')
    return problems


def compare(verbose=True):
    """EN and FR must have the SAME tag skeleton, bar the intended differences."""
    a = parse_skeleton(served_path('en'))
    b = parse_skeleton(served_path('fr'))
    problems = []
    if len(a.tags) != len(b.tags):
        problems.append(('SHAPE', f'EN has {len(a.tags)} tags, FR has {len(b.tags)}'))
    else:
        diffs = [(i, x, y) for i, (x, y) in enumerate(zip(a.tags, b.tags)) if x != y]
        # EXACTLY three differences are legitimate, and no others:
        #   1. the canonical <link>
        #   2. and 3. the two selector items swapping <span> and <a>
        # Requiring an exact count, not a ceiling, means a new per-language
        # divergence fails here instead of slipping through under the limit.
        allowed_tags = {'link', 'a', 'span'}
        if len(diffs) != 3:
            problems.append(('SHAPE', f'{len(diffs)} structural differences, exactly 3 expected'))
        for i, x, y in diffs:
            if x[0] not in allowed_tags or y[0] not in allowed_tags:
                problems.append(('SHAPE', f'#{i} unexpected difference {x} vs {y}'))
    if verbose:
        print(f'  EN {len(a.tags)} tags | FR {len(b.tags)} tags | problems {len(problems)}')
        for kind, s in problems: print(f'    {kind:14} {s[:88]}')
    return problems


_FIXED_W = re.compile(r'(?<![-a-z])width:\s*(\d+(?:\.\d+)?)px', re.I)


def static_overflow_check(verbose=True):
    """Static scan for horizontal-overflow HAZARDS. Not a rendering check.

    A `max-width` in px cannot cause overflow; a FIXED `width:Npx` wider than
    the narrowest supported viewport can. This reads the markup — it does not
    lay the page out, does not resolve the cascade, and cannot see a long word,
    a wide flex item or an oversized image. A clean result means "no fixed
    width that is certain to overflow was found", never "the page renders
    correctly". Browser measurement stays a local editorial step (see README).
    """
    problems = []
    for lang in ('en', 'fr'):
        path = served_path(lang)
        if not os.path.exists(path):
            problems.append(('MISSING-PAGE', f'{path}')); continue
        with open(path, encoding='utf-8') as fh:
            doc = fh.read()
        for m in _FIXED_W.finditer(doc):
            start = doc.rfind('\n', 0, m.start()) + 1
            frag = doc[start:m.start()]
            if 'max-width' in frag[-12:] or 'min(' in doc[m.start():m.start() + 60]:
                continue
            px = float(m.group(1))
            if px > MIN_VIEWPORT_PX:
                line = doc[:m.start()].count('\n') + 1
                problems.append(('FIXED-WIDTH',
                                 f'{lang} line {line}: width:{m.group(1)}px exceeds '
                                 f'the {MIN_VIEWPORT_PX}px viewport'))
        for tag in re.findall(r'<(?:pre|table)\b[^>]*>', doc):
            if 'overflow' not in tag:
                problems.append(('SCROLLABLE',
                                 f'{lang}: {tag[:40]} has no overflow handling'))
    if verbose:
        print(f'  static-overflow-check: {len(problems)} hazard(s) '
              f'(static markup scan — NOT a rendering check)')
        for kind, s in problems: print(f'    {kind:14} {s[:88]}')
    return problems


# --------------------------------------------------------------------------

USAGE = ('usage: i18n.py {extract | check <lang> | build <lang> | verify <lang>'
         ' | compare | static-overflow-check}')


def main(argv):
    cmd = argv[1] if len(argv) > 1 else None
    arg = argv[2] if len(argv) > 2 else None
    try:
        if cmd == 'extract':
            with open(SRC, encoding='utf-8') as fh:
                keys = collect(fh.read())
            write_pot(keys, POT)
            print(f'  {len(keys)} strings -> i18n/homepage.pot')
            return 0
        if cmd == 'check':
            if arg is None: raise LangError('check requires a language')
            return 1 if check(arg) else 0
        if cmd == 'build':
            if arg is None: raise LangError('build requires a language')
            return build(arg)
        if cmd == 'verify':
            if arg is None: raise LangError('verify requires a language')
            return 1 if verify(arg) else 0
        if cmd == 'compare':
            return 1 if compare() else 0
        if cmd == 'static-overflow-check':
            return 1 if static_overflow_check() else 0
    except I18nError as e:
        print(f'  REFUSED: {e}')
        return 2
    print(USAGE)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv))
