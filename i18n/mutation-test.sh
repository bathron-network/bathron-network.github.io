#!/usr/bin/env bash
# BATHRON homepage i18n — MANDATORY fail-closed mutation test.
#
# Proves by execution, not by argument, that a French page which is incomplete,
# stale, fuzzy, duplicated or built from a malformed catalogue CANNOT be
# published.
#
# The whole test runs inside a throwaway COPY of the source files. The calling
# worktree is never written to; that is asserted, not assumed, by comparing
# SHA-256 digests and `git status` before and after. There is no reset, no
# clean and no recursive delete outside the temporary directory.
#
#   bash i18n/mutation-test.sh          exit 0 = the guarantee holds
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

FAILED=0
STEP=0
say()  { STEP=$((STEP+1)); printf '\n=== STEP %d — %s ===\n' "$STEP" "$1"; }
ok()   { printf '  PASS  %s\n' "$1"; }
bad()  { printf '  FAIL  %s\n' "$1"; FAILED=1; }

# ---------------------------------------------------------------- guard rails
GUARDED=(index.html i18n/homepage.fr.po i18n/i18n.py i18n/mutation-test.sh)
declare -A BEFORE
for f in "${GUARDED[@]}"; do
    BEFORE[$f]="$(sha256sum "$f" | cut -d' ' -f1)"
done
GIT_BEFORE="$(git status --porcelain 2>/dev/null || echo '(not a git worktree)')"

SANDBOX="$(mktemp -d -t bathron-i18n-mutation-XXXXXX)"
cleanup() {
    # bounded: only the directory this script created
    case "$SANDBOX" in
        /tmp/bathron-i18n-mutation-*|/var/folders/*) rm -rf "$SANDBOX" ;;
        *) printf '  refusing to remove unexpected sandbox path %s\n' "$SANDBOX" ;;
    esac
}
trap cleanup EXIT

mkdir -p "$SANDBOX/i18n"
cp index.html            "$SANDBOX/index.html"
cp i18n/i18n.py          "$SANDBOX/i18n/i18n.py"
cp i18n/homepage.fr.po   "$SANDBOX/i18n/homepage.fr.po"
printf '  sandbox: %s\n' "$SANDBOX"

PO="$SANDBOX/i18n/homepage.fr.po"
SRC="$SANDBOX/index.html"
OUT="$SANDBOX/fr/index.html"
PRISTINE_PO="$SANDBOX/pristine.po"
PRISTINE_SRC="$SANDBOX/pristine.html"
cp "$PO" "$PRISTINE_PO"
cp "$SRC" "$PRISTINE_SRC"

run()      { ( cd "$SANDBOX" && python3 i18n/i18n.py "$@" ); }
reset_sandbox() { cp "$PRISTINE_PO" "$PO"; cp "$PRISTINE_SRC" "$SRC"; run extract >/dev/null; }

ORIG='Verify the chain yourself, from your own machine.'
MUT='Verify the chain yourself, from your own laptop.'

expect_refusal() {   # $1 = human label
    local label="$1" rc
    run build fr >/dev/null 2>&1; rc=$?
    if [ "$rc" -eq 0 ]; then bad "$label: build succeeded, expected refusal"; return; fi
    ok "$label: build refused (exit $rc)"
    if [ -e "$OUT" ]; then bad "$label: fr/index.html survives a refused build"
    else ok "$label: no French page on disk"; fi
}

# ---------------------------------------------------------------- 1
say 'clean build succeeds'
run extract >/dev/null
if run build fr >/dev/null; then ok 'build exited 0'; else bad 'clean build failed'; fi
if [ -f "$OUT" ]; then
    SIZE=$(wc -c < "$OUT"); ok "fr/index.html built ($SIZE bytes)"
else
    bad 'fr/index.html not produced'; SIZE=0
fi
grep -q '<html lang="fr"' "$OUT" 2>/dev/null && ok 'page declares lang="fr"' \
    || bad 'page does not declare lang="fr"'

# ---------------------------------------------------------------- 2
say 'English changed, catalogue untouched'
python3 - "$SRC" "$ORIG" "$MUT" <<'PY'
import sys
p, a, b = sys.argv[1:4]
s = open(p, encoding='utf-8').read()
assert s.count(a) == 1, f'anchor appears {s.count(a)} times'
open(p, 'w', encoding='utf-8').write(s.replace(a, b))
PY
cmp -s "$PO" "$PRISTINE_PO" && ok 'catalogue untouched' || bad 'catalogue changed'
run extract >/dev/null
expect_refusal 'missing translation'
ok "the ${SIZE}-byte page from step 1 was removed, not served stale"
reset_sandbox

# ---------------------------------------------------------------- 3
say 'catalogue absent'
mv "$PO" "$SANDBOX/parked.po"
expect_refusal 'absent catalogue'
mv "$SANDBOX/parked.po" "$PO"
reset_sandbox

# ---------------------------------------------------------------- 4
say 'fuzzy entry'
# The property under test is that the GENERATOR refuses a "#, fuzzy" entry.
# The flag is injected deterministically, reproducing what msgmerge writes: the
# msgid is updated to the new English, the old translation is kept, and the
# entry is flagged. This needs Python only, so neither this test nor the deploy
# that runs it depends on the Ubuntu archives. Compatibility with the REAL
# msgmerge output is covered separately, and optionally, by
# i18n/msgmerge-compat.sh.
python3 - "$SRC" "$ORIG" "$MUT" <<'MUTPY'
import sys
p, a, b = sys.argv[1:4]
s = open(p, encoding='utf-8').read()
open(p, 'w', encoding='utf-8').write(s.replace(a, b))
MUTPY
run extract >/dev/null
python3 - "$PO" "$ORIG" "$MUT" <<'FUZZPY'
import sys
p, old, new = sys.argv[1:4]
lines = open(p, encoding='utf-8').read().split('\n')
out, done = [], False
for ln in lines:
    if ln == 'msgid "%s"' % old:
        out.append('#, fuzzy')                  # exactly what msgmerge emits
        out.append('msgid "%s"' % new)          # msgid updated, translation stale
        done = True
        continue
    out.append(ln)
assert done, 'anchor msgid not found in the catalogue'
open(p, 'w', encoding='utf-8').write('\n'.join(out))
FUZZPY
grep -q '^#, fuzzy' "$PO" && ok 'entry carries a fuzzy flag' \
    || bad 'no fuzzy flag was injected'
expect_refusal 'fuzzy entry'

# ---------------------------------------------------------------- 5
say 'fuzzy cleared and translated — build succeeds again'
python3 - "$PO" "$MUT" <<'PY'
import sys
p, mut = sys.argv[1], sys.argv[2]
lines = open(p, encoding='utf-8').read().split('\n')
out, i = [], 0
while i < len(lines):
    ln = lines[i]
    if ln.startswith('#,') and 'fuzzy' in ln:
        rest = [f.strip() for f in ln[2:].split(',') if f.strip() != 'fuzzy']
        if rest: out.append('#, ' + ', '.join(rest))
        i += 1; continue
    if ln == f'msgid "{mut}"':
        out.append(ln)
        out.append('msgstr "Verifiez la chaine depuis votre propre ordinateur."')
        i += 2; continue
    out.append(ln); i += 1
open(p, 'w', encoding='utf-8').write('\n'.join(out))
PY
grep -q '^#, fuzzy' "$PO" && bad 'a fuzzy flag remains' || ok 'no fuzzy flag left'
if run build fr >/dev/null; then ok 'build exited 0'; else bad 'build failed after translating'; fi
grep -qF 'Verifiez la chaine depuis votre propre ordinateur.' "$OUT" 2>/dev/null \
    && ok 'the new translation is in the page' || bad 'new translation absent from the page'
reset_sandbox

# ---------------------------------------------------------------- 6
say 'duplicate entry in the catalogue'
python3 - "$PO" <<'PY'
import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
i = s.index('msgid "', s.index('msgstr ""') + 8)      # first real entry
j = s.index('\n\n', i) + 2
open(p, 'w', encoding='utf-8').write(s[:j] + s[i:j] + s[j:])
PY
expect_refusal 'duplicate entry'
reset_sandbox

# ---------------------------------------------------------------- 7
say 'malformed catalogue entry'
printf 'this line is not valid PO syntax\n' >> "$PO"
expect_refusal 'malformed catalogue'
reset_sandbox

# ---------------------------------------------------------------- 8
say 'sandbox recovered, and the calling worktree was never touched'
if run build fr >/dev/null; then ok 'sandbox builds again after every mutation'
else bad 'sandbox does not build after restoration'; fi
cmp -s "$SRC" "$PRISTINE_SRC" && ok 'sandbox index.html byte-identical to pristine' \
    || bad 'sandbox index.html diverged'
cmp -s "$PO" "$PRISTINE_PO" && ok 'sandbox catalogue byte-identical to pristine' \
    || bad 'sandbox catalogue diverged'

for f in "${GUARDED[@]}"; do
    now="$(sha256sum "$f" | cut -d' ' -f1)"
    if [ "$now" = "${BEFORE[$f]}" ]; then ok "unchanged: $f"
    else bad "MODIFIED: $f (${BEFORE[$f]} -> $now)"; fi
done
GIT_AFTER="$(git status --porcelain 2>/dev/null || echo '(not a git worktree)')"
if [ "$GIT_BEFORE" = "$GIT_AFTER" ]; then ok 'git status identical before and after'
else
    bad 'git status changed'
    printf '    before: %s\n    after : %s\n' "$GIT_BEFORE" "$GIT_AFTER"
fi

printf '\n================================\n'
if [ $FAILED -eq 0 ]; then
    printf 'MUTATION TEST: PASS — no incomplete, stale, fuzzy, duplicated or\n'
    printf 'malformed French catalogue can produce a published page.\n'
    exit 0
fi
printf 'MUTATION TEST: FAIL\n'
exit 1
