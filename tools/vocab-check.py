#!/usr/bin/env python3
"""Sentence-context vocabulary gates V1–V12; URLs and code are not prose."""
import re
from common import ROOT, LEGACY_PATHS, entries, markdown_prose, parse_html, report, sentences, summary

NEG = re.compile(r'\b(?:no|not|never|without|nor|neither|cannot)\b', re.I)
PATTERNS = {
    'V1': r'\b(?:M1|masternodes?|DMM|Clearing Providers?|pivot|numéraire)\b',
    'V2': r'\boperators?\b',
    'V3': r'\b(?:votes?|voting|quorum|committee|slashing|stake|staking)\b',
    'V4': r'\b(?:final|finality|finalized)\b',
    'V5': r'\b(?:swaps?|exchange|trade|trading|DEX|DLP|order book|liquidity pool)\b',
    'V6': r'\b(?:currency|money|coin|token|peg|par|yield|APY|backed by)\b',
    'V7': r'\b(?:guaranteed?|safe|instant|real-time|atomic|unstoppable)\b',
    'V8': r'\boracle\b',
    'V9': r'\b(?:testnet|mainnet|launch|live|roadmap|coming soon|under construction|Q[1-4])\b|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',
}
HISTORICAL = ('N-SPEC v0.7 keeps a historical application wording that was never adopted for any network. '
              'APP-SPEC v1 makes M0 the only settlement asset; its §13 differs from N-SPEC v0.7 §13 only in the asset.')
REQUIRED = {
    'producers': ['A ticket is an entry right, never a guarantee.',
                  'Proven equivocation bans the identity permanently. There is no slashing: the ticket was spent at entry, not seized.'],
    'engine': ['One producer per slot, drawn from burned tickets with a Bitcoin-derived seed. No committee, no quorum, no vote, no finality gadget.'],
    'depth': ['There is no native finality. N offers inclusion and depth. Each participant chooses a depth from the published table, within the published domain. Outside it, N makes no quantitative claim.',
              'Wait or stop rather than be wrong. A settlement may wait hours; the network may pause to resolve a conflict.'],
    'overview': ['There is no native finality.'],
    'trust': ['There is no native finality.', 'BATHRON reads Bitcoin; it never commands it.',
              'Wait or stop rather than be wrong. A settlement may wait hours; the network may pause to resolve a conflict.'],
    'burns': ['New M0 comes only from eligible burns imported under the rules.',
              'Using M0 does not require burning BTC.', 'Every M0 unit comes from burned bitcoin. A burn creates no reserve and no claim on Bitcoin.'],
    'bitcoin-facts': ['BTCSTATE is a generic, non-consuming presence predicate.'],
    'covenants': ['recursive covenants and discreet log contracts (DLCs) are not capabilities offered by this documented baseline today.'],
    'settlement': ['A Bitcoin payment never resolves two §13 locks.',
                   'Without the scan, resolution waits for data instead of refunding by default.'],
    'between-providers': ['It does not establish an equal interval after the beneficiary discovers the child.'],
    'what-you-can-build': ['These are examples of third-party constructions, not services supplied by BATHRON.',
                           'Difficulty markets are therefore compatible by design, without an oracle.',
                           'BTC/USD price is not a Bitcoin fact.'],
    'roles': [HISTORICAL, 'Independent liquidity providers settle with each other on M0, without trusting one another. The specifications define no order book and no pool.'],
}


def corpus(root):
    paths = list((root / 'docs/src').glob('*.md')) + [root / 'README.md', root / 'index.html']
    paths += [root / path / 'index.html' for path in LEGACY_PATHS]
    paths += list((root / 'img').glob('*.svg')) + list((root / 'docs/src/img').glob('*.svg'))
    for path in paths:
        raw = path.read_text()
        text = parse_html(raw).prose if path.suffix in ('.html', '.svg') else markdown_prose(raw)
        yield path.relative_to(root).as_posix(), text


def check(root=ROOT):
    errors = []
    allow = entries('vocab-allow.txt', root)
    texts = dict(corpus(root))
    for path, text in texts.items():
        stem = path.rsplit('/', 1)[-1].split('.')[0]
        for sentence in sentences(text):
            neg = bool(NEG.search(sentence))
            for rule, pattern in PATTERNS.items():
                candidate = sentence
                if rule == 'V1' and path == 'docs/src/status.md':
                    candidate = re.sub(r'\bDMM\b', '', candidate)
                if rule == 'V2' and path == 'docs/src/glossary.md':
                    candidate = candidate.replace('formerly called Operator', '')
                if rule == 'V3' and neg and stem in {'engine', 'producers', 'overview', 'trust', 'glossary'}:
                    continue
                if rule in {'V4', 'V6', 'V7'} and neg:
                    continue
                if rule == 'V5':
                    candidate = re.sub(r'\b(?:message|key) exchange\b', '', candidate, flags=re.I)
                    if neg:
                        candidate = re.sub(r'\border book\b', '', candidate, flags=re.I)
                if rule == 'V8':
                    candidate = re.sub(r'\b(?:without an|no) oracle\b', '', candidate, flags=re.I)
                if rule == 'V9' and path == 'docs/src/status.md':
                    continue
                if re.search(pattern, candidate, re.I) and not any(a['rule'] == rule and a['page'] == path and a['sentence'] == sentence for a in allow):
                    errors.append(f'{path}: {rule}: {sentence}')
            # References/versions identify sources, not quantities. Citation labels
            # with invariant numbers remain explicit, reviewed exceptions.
            numeric = re.sub(r'§+\s*\d+(?:\.\d+)*(?:[–-]\d+(?:\.\d+)*)?|\bv\d+(?:\.\d+)*\b', '', sentence)
            numeric = re.sub(r'\b(?:GEN|OBJ|BTCSTATE|BTC|SCR|CTV|CLTV|CSV|R2P|PUB|IMP)-\d+\b', '', numeric)
            if re.search(r'\b\d+(?:\.\d+)?\s*(?:sats?|BTC|blocks?|slots?|s|ms|h|min|GB|%|confirmations?)(?!\w)|(?<![\w.])\d{2,}(?!\w|\.\d)', numeric, re.I):
                if not any(a['rule'] == 'V10' and a['page'] == path and a['sentence'] == sentence for a in allow):
                    errors.append(f'{path}: V10: {sentence}')
    glossary = texts.get('docs/src/glossary.md', '')
    if glossary.count('formerly called Operator') != 1:
        errors.append('docs/src/glossary.md: V2: exactly one historical role mention required')
    for name, phrases in REQUIRED.items():
        text = ' '.join(texts.get(f'docs/src/{name}.md', '').split())
        for phrase in phrases:
            if phrase not in text:
                errors.append(f'docs/src/{name}.md: V11: missing required wording: {phrase}')
    for name in summary(root):
        if name in {'limitations.md', 'how-this-project-is-built.md'}:
            raw = (root / 'docs/src' / name).read_text()
            if not re.match(r'^# [^\n]+\n\n> \*\*Sources:\*\*[^\n]+\n> ', raw):
                errors.append(f'docs/src/{name}: V12: missing transparency source block')
        elif name not in {'status.md', 'glossary.md'}:
            raw = (root / 'docs/src' / name).read_text()
            if not re.match(r'^# [^\n]+\n\n> \*\*Normative source:\*\*[^\n]+\n> This page explains; it does not restate rules or parameter values\.', raw):
                errors.append(f'docs/src/{name}: V12: missing opening source block')
    # The historical explanation belongs only on the roles page.
    for path, text in texts.items():
        if path != 'docs/src/roles.md' and 'historical application wording' in text:
            errors.append(f'{path}: V11: historical explanation belongs in roles')
    return errors


if __name__ == '__main__':
    raise SystemExit(report(check(), 'vocabulary V1–V12'))
