#!/usr/bin/env bash
# BATHRON homepage i18n — MANDATORY mutation test.
#
# Proves, by execution rather than by argument, that an English change which is
# not reflected in the French catalogue CANNOT produce a published French page.
#
# Run from the repository root:  bash i18n/mutation-test.sh
# Exit 0 = the fail-closed guarantee holds. Any other exit = it does not.
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
SRC=index.html
PO=i18n/homepage.fr.po
OUT=fr/index.html
BAK="$(mktemp -d)"
STEP=0
FAILED=0

cp "$SRC" "$BAK/index.html"
cp "$PO"  "$BAK/homepage.fr.po"

restore() {
    cp "$BAK/index.html" "$SRC"
    cp "$BAK/homepage.fr.po" "$PO"
    python3 i18n/i18n.py extract >/dev/null
    rm -rf "$BAK"
}
trap restore EXIT

say() { STEP=$((STEP+1)); printf '\n=== STEP %d — %s ===\n' "$STEP" "$1"; }
ok()  { printf '  PASS  %s\n' "$1"; }
bad() { printf '  FAIL  %s\n' "$1"; FAILED=1; }

ORIG='Verify the chain yourself, from your own machine.'
MUT='Verify the chain yourself, from your own laptop.'

# ---------------------------------------------------------------- 1
say 'clean build succeeds'
python3 i18n/i18n.py extract >/dev/null
python3 i18n/i18n.py build fr
rc=$?
[ $rc -eq 0 ] && ok "build exited 0" || bad "build exited $rc, expected 0"
[ -f "$OUT" ] && ok "$OUT exists" || bad "$OUT missing"
BUILT_SIZE=$(wc -c < "$OUT" 2>/dev/null || echo 0)

# ---------------------------------------------------------------- 2
say 'mutate one English sentence, leave the catalogue untouched'
grep -qF "$ORIG" "$SRC" || { bad "anchor sentence not found in $SRC"; exit 1; }
python3 - "$SRC" "$ORIG" "$MUT" <<'PY'
import sys
p, a, b = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(p, encoding='utf-8').read()
assert s.count(a) == 1, f'anchor appears {s.count(a)} times'
open(p, 'w', encoding='utf-8').write(s.replace(a, b))
PY
grep -qF "$MUT" "$SRC" && ok "English source mutated" || bad "mutation did not apply"
cmp -s "$PO" "$BAK/homepage.fr.po" && ok "French catalogue untouched" || bad "catalogue changed"

# ---------------------------------------------------------------- 3
say 'rebuild must FAIL (missing translation)'
python3 i18n/i18n.py extract >/dev/null
python3 i18n/i18n.py build fr
rc=$?
[ $rc -ne 0 ] && ok "build exited $rc (non-zero)" || bad "build exited 0 — fail-closed BROKEN"

# ---------------------------------------------------------------- 4
say 'no stale French page may survive a failed build'
if [ -e "$OUT" ]; then
    bad "$OUT still present after a failed build ($(wc -c < "$OUT") bytes)"
else
    ok "$OUT absent — the previous ${BUILT_SIZE}-byte page was removed, not served stale"
fi

# ---------------------------------------------------------------- 5
say 'msgmerge marks the entry fuzzy — a fuzzy entry must ALSO block the build'
msgmerge --quiet --update --backup=none "$PO" i18n/homepage.pot
if grep -q '^#, fuzzy' "$PO"; then
    ok "entry flagged fuzzy by msgmerge"
else
    bad "msgmerge produced no fuzzy flag"
fi
python3 i18n/i18n.py build fr
rc=$?
[ $rc -ne 0 ] && ok "build exited $rc — fuzzy is not publishable" || bad "fuzzy entry was published"
[ -e "$OUT" ] && bad "$OUT present after fuzzy-refused build" || ok "$OUT still absent"

# ---------------------------------------------------------------- 6
say 'translate the mutation and clear fuzzy — build must succeed again'
python3 - "$PO" "$MUT" <<'PY'
import sys, re
p, mut = sys.argv[1], sys.argv[2]
lines = open(p, encoding='utf-8').read().split('\n')
out, i = [], 0
while i < len(lines):
    ln = lines[i]
    if ln.startswith('#, ') and 'fuzzy' in ln:
        rest = [f.strip() for f in ln[3:].split(',') if f.strip() != 'fuzzy']
        if rest: out.append('#, ' + ', '.join(rest))
        i += 1; continue
    if ln.startswith('#| '):          # msgmerge's previous-msgid comment
        i += 1; continue
    if ln == f'msgid "{mut}"':
        out.append(ln)
        out.append('msgstr "Vérifier la chaîne vous-même, depuis votre ordinateur portable."')
        i += 2                        # skip the stale msgstr line
        continue
    out.append(ln); i += 1
open(p, 'w', encoding='utf-8').write('\n'.join(out))
PY
grep -q '^#, fuzzy' "$PO" && bad "fuzzy flags remain" || ok "no fuzzy flag left"
python3 i18n/i18n.py build fr
rc=$?
[ $rc -eq 0 ] && ok "build exited 0" || bad "build exited $rc, expected 0"
[ -f "$OUT" ] && ok "$OUT rebuilt" || bad "$OUT missing"
grep -qF 'ordinateur portable' "$OUT" && ok "new translation present in the page" \
    || bad "new translation absent from the page"

# ---------------------------------------------------------------- 7
say 'restore the clean tree'
restore
trap - EXIT
python3 i18n/i18n.py build fr >/dev/null
if cmp -s "$SRC" <(git show HEAD:index.html 2>/dev/null) || true; then :; fi
python3 i18n/i18n.py check fr >/dev/null && ok "catalogue clean again" || bad "catalogue not clean"
grep -qF "$ORIG" "$SRC" && ok "English source restored" || bad "source not restored"
grep -qF 'ordinateur portable' "$PO" && bad "test translation leaked into the catalogue" \
    || ok "catalogue restored"

printf '\n================================\n'
if [ $FAILED -eq 0 ]; then
    printf 'MUTATION TEST: PASS — a stale or partial French page cannot be published.\n'
    exit 0
else
    printf 'MUTATION TEST: FAIL\n'
    exit 1
fi
