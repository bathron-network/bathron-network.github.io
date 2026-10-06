#!/usr/bin/env python3
"""Derive the sitemap from the book and language table, without timestamps."""
import argparse
from common import ROOT, i18n, summary, report


def render(root=ROOT):
    paths = [lang['path'] for lang in i18n.LANGUAGES]
    paths += ['/docs/' + name.removesuffix('.md') + '.html' for name in summary(root)]
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f'  <url><loc>{i18n.SITE}{path}</loc></url>\n' for path in paths) + '</urlset>\n'


def check(root=ROOT):
    return [] if (root / 'sitemap.xml').read_text() == render(root) else ['sitemap.xml: regenerate with tools/gen-sitemap.py']


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--check', action='store_true')
    args = p.parse_args()
    if args.check:
        raise SystemExit(report(check(), 'sitemap'))
    (ROOT / 'sitemap.xml').write_text(render())
