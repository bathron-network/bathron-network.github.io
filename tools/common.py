"""Shared, standard-library-only documentation checks; no network access."""
from pathlib import Path
from html.parser import HTMLParser
import html
import importlib.util
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'i18n'))
import i18n


def tracked(root=ROOT):
    result = subprocess.run(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'],
                            cwd=root, check=True, capture_output=True).stdout
    return sorted({p for name in result.decode().split('\0') if name
                   for p in [root / name] if p.is_file() and not p.is_symlink()})


def entries(name, root=ROOT):
    rows = []
    for line in (root / 'tools' / name).read_text().splitlines():
        if line.strip() and not line.startswith('#'):
            row = json.loads(line)
            if not row.get('reason', '').strip():
                raise ValueError(f'{name}: exception without reason')
            rows.append(row)
    return rows


def summary(root=ROOT):
    return re.findall(r'\]\(([^)#]+\.md)\)', (root / 'docs/src/SUMMARY.md').read_text())


def redirects(root=ROOT):
    # The redirect table is last; parse its deliberately narrow TOML subset.
    text = (root / 'docs/book.toml').read_text().split('[output.html.redirect]', 1)[1]
    pairs = re.findall(r'^"([^"]+)"\s*=\s*"([^"]+)"\s*$', text, re.M)
    if len(dict(pairs)) != len(pairs):
        raise ValueError('duplicate redirect key')
    return dict(pairs)


def markdown_prose(text):
    text = re.sub(r'^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$', '', text, flags=re.M | re.S)
    text = re.sub(r'`+[^`]*`+', '', text)
    text = re.sub(r'^\s*\[[^\]]+\]:.*$', '', text, flags=re.M)
    text = re.sub(r'\[([^\]]+)\](?:\([^)]*\)|\[[^\]]*\])', r'\1', text)
    text = re.sub(r'<https?://[^>]+>', '', text)
    text = re.sub(r'^#+\s*(?:\d+\s*·\s*)?', '', text, flags=re.M)
    text = re.sub(r'^- \d+ · ', '- ', text, flags=re.M)
    return re.sub(r'[*_>]', '', text)


class HTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.parts = []
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in ('style', 'script', 'code', 'pre'):
            self.skip += 1
        if d.get('id'):
            self.ids.add(d['id'])
        if tag == 'a' and d.get('name'):
            self.ids.add(d['name'])
        for key in ('href', 'src'):
            if d.get(key):
                self.links.append(d[key])
        if tag in ('p', 'h1', 'h2', 'h3', 'h4', 'li', 'td', 'br', 'article', 'nav'):
            self.parts.append('\n')
        if not self.skip:
            for key in ('alt', 'title', 'aria-label'):
                if d.get(key):
                    self.parts.extend(['\n', d[key], '\n'])
            if tag == 'meta' and (d.get('name') or d.get('property')) in i18n.META_PROSE:
                self.parts.extend(['\n', d.get('content', ''), '\n'])

    def handle_endtag(self, tag):
        if tag in ('style', 'script', 'code', 'pre'):
            self.skip = max(0, self.skip - 1)
        if tag in ('p', 'h1', 'h2', 'h3', 'h4', 'li', 'td', 'article', 'nav'):
            self.parts.append('\n')

    def handle_data(self, text):
        if not self.skip:
            self.parts.append(text)

    @property
    def prose(self):
        return ''.join(self.parts)


def parse_html(text):
    parser = HTML()
    parser.feed(text)
    parser.close()
    return parser


def sentences(text):
    for paragraph in text.splitlines():
        paragraph = ' '.join(paragraph.split())
        # A period inside a version/section number is not a sentence boundary.
        for sentence in re.split(r'(?<=[.!?])\s+(?=[A-Z§“])', paragraph):
            if sentence:
                yield sentence


def report(errors, label):
    for error in errors:
        print(error)
    print(f'{label}: {"FAIL" if errors else "PASS"} ({len(errors)} errors)')
    return bool(errors)
