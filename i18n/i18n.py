#!/usr/bin/env python3
"""BATHRON homepage i18n — single structural source, GNU gettext catalogues.

index.html is the canonical source: structure AND English text.
Translatable segments are the text nodes and a whitelist of attributes.
<style> and <script> are never translatable.

  extract     -> i18n/homepage.pot   (generated, never hand-edited)
  check <lg>  -> fail-closed audit of a catalogue against the current source
  build <lg>  -> <lg>/index.html     (generated artifact, not versioned)

Disambiguation: when one English string needs two different translations
depending on where it appears, wrap the element in data-i18n-context="<name>".
That becomes the gettext msgctxt. The attribute is build metadata and is
stripped from every generated page, English included.

No framework, no runtime JS, no network, no AI. Deterministic.
"""
import sys, os, re, html
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
    'en': {'lang': 'en', 'canonical': 'https://bathron.org/',
           'sel': '<b>EN</b> <span>/</span> <a href="/fr/">FR</a>'},
    'fr': {'lang': 'fr', 'canonical': 'https://bathron.org/fr/',
           'sel': '<a href="/">EN</a> <span>/</span> <b>FR</b>'},
}


def norm(s):
    return ' '.join(s.split())


class Walker(HTMLParser):
    """Rebuilds the document, calling on_text/on_attr for translatable parts.

    Text is buffered ACROSS entity references so "Bitcoin&rsquo;s chain." is ONE
    translatable string, not three fragments. Each buffer item is
    (raw_source, plain_text): raw is re-emitted verbatim when the string comes
    back unchanged, which keeps the English round-trip byte-identical.
    """
    def __init__(self, on_text, on_attr):
        super().__init__(convert_charrefs=False)
        self.out, self.skip = [], 0
        self.on_text, self.on_attr = on_text, on_attr
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
            if k == CTX_ATTR: continue          # build metadata, never emitted
            if v is None: parts.append(f' {k}'); continue
            parts.append(f' {k}="{self.on_attr(tag, k, v, mname, ctx)}"')
        self.out.append(f'<{tag}{"".join(parts)}{" /" if selfclosing else ""}>')
        if not selfclosing and tag not in VOID: self.ctx.append(ctx)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs, selfclosing=True)

    def handle_endtag(self, tag):
        self._flush()
        if tag in SKIP_TAGS: self.skip -= 1
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


def collect(src):
    """Ordered, de-duplicated list of (context, english) keys."""
    seen, order = set(), []
    def keep(s, ctx):
        k = (ctx, norm(s))
        if k[1] and k not in seen: seen.add(k); order.append(k)
    def text(d, ctx): keep(d, ctx); return d
    def attr(tag, k, v, name=None, ctx=''):
        if tag == 'meta':
            if k == 'content' and name in META_PROSE and norm(v): keep(v, ctx)
            return v
        if (tag, k) in ATTRS and (tag, k) != ('html', 'lang') and norm(v): keep(v, ctx)
        return v
    w = Walker(text, attr); w.feed(src); w.close()
    return order


def po_escape(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def unesc(s):
    return s.replace('\\"', '"').replace('\\n', '\n').replace('\\\\', '\\')


def write_pot(keys, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('# BATHRON homepage — GENERATED, DO NOT EDIT BY HAND.\n'
                '# Regenerate with: python3 i18n/i18n.py extract\n'
                'msgid ""\nmsgstr ""\n'
                '"Content-Type: text/plain; charset=UTF-8\\n"\n'
                '"Content-Transfer-Encoding: 8bit\\n"\n\n')
        for ctx, s in keys:
            if ctx: f.write(f'msgctxt "{po_escape(ctx)}"\n')
            f.write(f'msgid "{po_escape(s)}"\nmsgstr ""\n\n')


def read_po(path):
    """Minimal .po reader. Returns (entries, flags, obsolete_line_count).

    Keys are (msgctxt, msgid) tuples; msgctxt is '' when absent.
    """
    entries, flags, obsolete = {}, {}, 0
    if not os.path.exists(path): return entries, flags, obsolete
    cur_flags, ctx, key, val, mode = [], None, None, None, None

    def flush():
        nonlocal ctx, key, val, cur_flags
        if key is not None:
            k = (ctx or '', key)
            entries[k] = val or ''
            flags[k] = list(cur_flags)
        ctx, key, val, cur_flags = None, None, None, []

    for raw in open(path, encoding='utf-8'):
        line = raw.rstrip('\n')
        if line.startswith('#~'): obsolete += 1; continue
        if line.startswith('#,'):
            cur_flags = [x.strip() for x in line[2:].split(',')]; continue
        if line.startswith('#'): continue
        if not line.strip(): flush(); continue
        m = re.match(r'^(msgctxt|msgid|msgstr)\s+"(.*)"$', line)
        if m:
            kind, v = m.group(1), unesc(m.group(2))
            if kind == 'msgctxt': flush(); ctx = v; mode = 'ctx'
            elif kind == 'msgid': key = v; mode = 'id'
            else: val = v; mode = 'str'
            continue
        m = re.match(r'^"(.*)"$', line)
        if m:
            v = unesc(m.group(1))
            if mode == 'ctx': ctx = (ctx or '') + v
            elif mode == 'id': key = (key or '') + v
            elif mode == 'str': val = (val or '') + v
    flush()
    entries.pop(('', ''), None); flags.pop(('', ''), None)
    return entries, flags, obsolete


def po_path(lang):
    return os.path.join(ROOT, 'i18n', f'homepage.{lang}.po')


def check(lang, verbose=True):
    """Fail-closed audit. Returns a list of (kind, description) problems."""
    need = collect(open(SRC, encoding='utf-8').read())
    entries, flags, obsolete = read_po(po_path(lang))
    problems = []
    for k in need:
        if k not in entries: problems.append(('MISSING', fmt(k)))
        elif not entries[k].strip(): problems.append(('EMPTY', fmt(k)))
        elif 'fuzzy' in flags.get(k, []): problems.append(('FUZZY', fmt(k)))
    need_set = set(need)
    for k in entries:
        if k not in need_set: problems.append(('OBSOLETE', fmt(k)))
    if obsolete:
        problems.append(('OBSOLETE-BLOCK',
                         f'{obsolete} commented-out line(s) — catalogue not synchronised'))
    if verbose:
        print(f'  source strings   : {len(need)}')
        print(f'  catalogue        : {po_path(lang)}')
        print(f'  entries          : {len(entries)}')
        print(f'  problems         : {len(problems)}')
        for kind, s in problems[:20]:
            print(f'    {kind:15} {s[:88]}')
    return problems


def fmt(k):
    return f'[{k[0]}] {k[1]}' if k[0] else k[1]


def build(lang):
    """Generate the translated page. Never writes on an incomplete catalogue."""
    out_dir = ROOT if lang == 'en' else os.path.join(ROOT, lang)
    out = os.path.join(out_dir, 'index.html')
    if lang == 'en':
        print('  refusing to overwrite the source index.html'); return 1
    # 1. remove any previous artifact BEFORE validating, so a failed build
    #    can never leave a stale translated page behind.
    if os.path.exists(out):
        os.remove(out); print(f'  removed stale artifact {lang}/index.html')
    # 2. fail-closed
    problems = check(lang, verbose=False)
    if problems:
        print(f'  BUILD REFUSED for {lang}: {len(problems)} problem(s)')
        for kind, s in problems[:20]: print(f'    {kind:15} {s[:88]}')
        return 1
    src = open(SRC, encoding='utf-8').read()
    entries, _, _ = read_po(po_path(lang))
    conf, en = LANG_CONF[lang], LANG_CONF['en']

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
    doc = ''.join(w.out)
    # 3. language-dependent structural facts, applied explicitly
    def sub1(pattern, repl, text, what):
        text, n = re.subn(pattern, repl.replace('\\', '\\\\'), text, flags=re.S)
        if n != 1:
            raise SystemExit(f'  BUILD FAILED: expected exactly 1 {what}, found {n}')
        return text
    doc = sub1(r'<meta property="og:url" content="[^"]*">',
               f'<meta property="og:url" content="{conf["canonical"]}">', doc, 'og:url')
    doc = sub1(r'<link rel="canonical"[^>]*>',
               f'<link rel="canonical" href="{conf["canonical"]}">', doc, 'canonical link')
    doc = sub1(r'<p class="langsel">.*?</p>',
               f'<p class="langsel">{conf["sel"]}</p>', doc, 'language selector')
    os.makedirs(out_dir, exist_ok=True)
    open(out, 'w', encoding='utf-8').write(doc)
    if not os.path.exists(out):
        print(f'  BUILD FAILED: {out} was not created'); return 1
    print(f'  built {lang}/index.html ({os.path.getsize(out)} bytes)')
    return 0


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    lang = sys.argv[2] if len(sys.argv) > 2 else 'fr'
    if cmd == 'extract':
        keys = collect(open(SRC, encoding='utf-8').read())
        write_pot(keys, POT); print(f'  {len(keys)} strings -> i18n/homepage.pot')
    elif cmd == 'check':
        sys.exit(1 if check(lang) else 0)
    elif cmd == 'build':
        sys.exit(build(lang))
    else:
        print(__doc__); sys.exit(2)
