#!/usr/bin/env python3
"""Generic public-tree checks. Private names require a separate private review."""
import argparse
import ipaddress
import os
import re
import subprocess
from common import ROOT, entries, report, tracked

EMAILS = {'security@bathron.org', 'dev@bathron.org', 'contact@bathron.org'}
# Split literal fragments so the detector does not report its own vocabulary.
AI = ['chat' + 'g' + 'pt', 'co' + 'dex', 'clau' + 'de', 'anthro' + 'pic',
      'open' + 'ai', 'gem' + 'ini', 'g' + 'pt' + r'(?:-?\d+(?:\.\d+)*)?',
      'so' + 'nnet', 'o' + 'pus', 'ha' + 'iku', 'as' + 'tra', 'lu' + 'na',
      'cop' + 'ilot', 'deep' + 'seek', 'll' + 'ama']
PATTERNS = {
    'home-path': r'(?:/ho[m]e/|/Us[e]rs/|~[/])[^\s\"\'<>`]+',
    'host': r'\b(?:vps\d+|local[h]ost)\b',
    'internal': r'\blot\s*[-#:]?\s*\d{4}\b|\bDIRECTI[O]N(?:\.md)?\b|\bQR-\d+\b|\bINCOMPL[E]T\b',
    'ai-name': r'(?<![\w-])(?:' + '|'.join(AI) + r')(?![\w-])',
}


def findings(line):
    result = []
    for rule, pattern in PATTERNS.items():
        result += [(rule, m.group()) for m in re.finditer(pattern, line, 0 if rule == 'internal' else re.I)]
    for m in re.finditer(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])', line):
        result.append(('ip', m.group()))
    for m in re.finditer(r'(?<![\w:])(?:[0-9a-fA-F]{0,4}:){2,}[0-9a-fA-F:.]*(?:%[\w]+)?(?![\w:])', line):
        try:
            ipaddress.IPv6Address(m.group().split('%')[0])
        except ValueError:
            continue
        result.append(('ip', m.group()))
    for m in re.finditer(r'[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}', line):
        if m.group() not in EMAILS:
            result.append(('email', m.group()))
    return result


def check(root=ROOT):
    allow = entries('confidentiality-allow.txt', root)
    errors = []
    for a in allow:
        target = root / a['file']
        if not target.is_file() or a['line'] not in target.read_text().splitlines():
            errors.append('confidentiality: stale exact-line exception')
    for path in tracked(root):
        try:
            raw = path.read_text()
        except UnicodeError:
            continue
        relative = path.relative_to(root).as_posix()
        generic_code = False
        for n, line in enumerate(raw.splitlines(), 1):
            if path.suffix == '.md' and re.match(r'^\s*```', line):
                generic_code = not generic_code
            for rule, match in findings(line):
                if relative == 'tools/confidentiality-allow.txt':
                    # Exception records necessarily repeat their permitted literals.
                    # A new literal still fails unless separately reviewed and scoped.
                    if any(a['rule'] == rule and a['match'] == match for a in allow):
                        continue
                if rule == 'home-path' and generic_code and match.startswith('~/'):
                    continue
                if rule == 'internal' and re.search(r'https://github\.com/bathron-network/n-spec/blob/[^\s]+', line) and line.lstrip().startswith(('>', '[')):
                    continue
                if any(a['file'] == relative and a['rule'] == rule and a['match'] == match and a['line'] == line for a in allow):
                    continue
                errors.append(f'{relative}:{n}: confidentiality/{rule}')
    return errors


def metadata(root=ROOT, base=None, head=None, branch=None):
    errors = []
    if not branch or not re.fullmatch(r'docs/[a-zA-Z0-9][a-zA-Z0-9._/-]*', branch):
        errors.append('metadata: pull-request branch must match docs/…')
    if not base or not head:
        return errors + ['metadata: explicit base and head commits are required']
    if not all(re.fullmatch(r'[0-9a-f]{40}', ref) for ref in (base, head)):
        return errors + ['metadata: base and head must be full commit hashes']
    result = subprocess.run(['git', 'log', '--format=%an%x00%ae%x00%cn%x00%ce', f'{base}..{head}'], cwd=root, text=True, capture_output=True)
    if result.returncode or not result.stdout.strip():
        return errors + ['metadata: commit range is absent or unreadable']
    for row in result.stdout.splitlines():
        if row.split('\0') != ['BATHRON', 'dev@bathron.org'] * 2:
            errors.append('metadata: unexpected author or committer identity')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--metadata', action='store_true')
    args = parser.parse_args()
    errors = metadata(base=os.getenv('DOCS_BASE'), head=os.getenv('DOCS_HEAD'), branch=os.getenv('DOCS_BRANCH')) if args.metadata else check()
    raise SystemExit(report(errors, 'PR metadata' if args.metadata else 'public confidentiality'))
