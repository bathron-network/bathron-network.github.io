#!/usr/bin/env python3
"""English-only publication policy and direct legacy homepage redirects."""
from html.parser import HTMLParser
import re
from common import ROOT, SITE, LEGACY_PATHS, tracked, report


def redirect_html():
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>BATHRON</title>\n<meta http-equiv="refresh" content="0; url=/">\n'
            f'<link rel="canonical" href="{SITE}/">\n'
            '<meta name="robots" content="noindex">\n</head>\n'
            '<body><a href="/">BATHRON home</a></body>\n</html>\n')


class Policy(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
        self.english = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.english = attrs.get('lang') == 'en'
        if ('hreflang' in attrs or 'data-i18n-context' in attrs
                or set(attrs.get('class', '').split()) & {'langsel', 'langmenu'}):
            self.errors.append('translation selector or metadata')
        if attrs.get('translate') == 'no' or 'notranslate' in attrs.get('class', '').split():
            self.errors.append('browser translation disabled')
        if tag == 'meta' and attrs.get('name') == 'google' and attrs.get('content') == 'notranslate':
            self.errors.append('browser translation disabled')


def check(root=ROOT):
    errors = []
    for path in tracked(root):
        if path.suffix in {'.po', '.pot'}:
            errors.append(f'{path.relative_to(root)}: maintained translation catalogue')
    for name in LEGACY_PATHS:
        path = root / name / 'index.html'
        if not path.is_file() or path.read_text() != redirect_html():
            errors.append(f'{name}/index.html: expected direct homepage redirect')
    home = (root / 'index.html').read_text()
    policy = Policy()
    policy.feed(home)
    if not policy.english:
        errors.append('index.html: expected English document')
    errors.extend('index.html: ' + error for error in policy.errors)
    if re.search(r'N-SPEC|WHY-N|APP-SPEC|\b(?:French|English|Français|language|langue)\b',
                 re.sub(r'<style>.*?</style>', '', home, flags=re.S), re.I):
        errors.append('index.html: source citation or language mention')
    return errors


if __name__ == '__main__':
    raise SystemExit(report(check(), 'English-only site'))
