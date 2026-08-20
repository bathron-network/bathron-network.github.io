#!/usr/bin/env bash
# BATHRON homepage i18n — MANDATORY fail-closed mutation test.
#
# Proves by execution, not by argument, that a French page which is incomplete,
# stale, fuzzy, duplicated or built from a malformed catalogue CANNOT be
# published.
#
# PORTABILITY. This runs on Bash 3.2 — the /bin/bash macOS ships — as well as
# Bash 5. No associative arrays (Bash 4+), no `mapfile`, no `${var^^}`, and no
# `sha256sum` (absent from a stock macOS). Hashing goes through Python, which
# is already a hard dependency. An earlier version used `declare -A`; on Bash
# 3.2 it failed, the guarded-file checks never ran, and the script still printed
# PASS and exited 0. That class of failure is now impossible: see "FAIL-CLOSED".
#
# FAIL-CLOSED. Any harness error — hashing, sandbox creation, copying, a missing
# anchor — calls die() and exits 3. On top of that the script counts the steps
# and assertions it actually executed and refuses to print PASS unless both
# reach their expected totals, so a silently truncated run cannot be mistaken
# for a successful one.
#
# The whole test runs inside a throwaway COPY of the source files. The calling
# worktree is never written to; that is asserted, not assumed.
#
#   bash i18n/mutation-test.sh
#     0 = the guarantee holds
#     1 = an assertion failed
#     3 = the harness itself could not run (never reported as PASS)
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)" || exit 3
cd "$ROOT" || exit 3

# Test-only fault injection, used by the regression tests in test_i18n.py to
# prove that a broken harness can never report success.
FAULT="${BATHRON_MUTATION_TEST_FAULT:-}"
fault_is() { [ "$FAULT" = "$1" ]; }

STEPS_EXPECTED=8
# Assertions that do not depend on how many files are guarded. The per-file
# "unchanged: <path>" assertions are added once GUARDED is known, so adding a
# guarded file cannot silently loosen the completeness check.
ASSERTIONS_FIXED=23

FAILED=0
STEP=0
ASSERTIONS=0
SANDBOX=""
SANDBOX_PREFIX=""
MARKER_NAME=".bathron-mutation-sandbox"

die() {
    printf '\n  FATAL  %s\n' "$1"
    printf '\nMUTATION TEST: FAIL (harness error — nothing was proven)\n'
    exit 3
}
say()  { STEP=$((STEP+1)); printf '\n=== STEP %d — %s ===\n' "$STEP" "$1"; }
ok()   { ASSERTIONS=$((ASSERTIONS+1)); printf '  PASS  %s\n' "$1"; }
bad()  { ASSERTIONS=$((ASSERTIONS+1)); printf '  FAIL  %s\n' "$1"; FAILED=1; }

# --- the files this test must leave untouched -------------------------------
# Indexed array: available in Bash 3.2. An associative array is not.
GUARDED=(index.html i18n/homepage.fr.po i18n/i18n.py i18n/mutation-test.sh i18n/ci-check.sh)
ASSERTIONS_EXPECTED=$((ASSERTIONS_FIXED + ${#GUARDED[@]}))

# sha256 of each path, one "<hex>  <path>" line per file. Python, not
# sha256sum: macOS has `shasum`, Linux has `sha256sum`, and neither is
# guaranteed — Python 3 already is.
manifest() {
    if fault_is manifest; then
        echo 'injected fault: manifest' >&2
        return 1
    fi
    python3 - "$@" <<'MANIFEST_PY'
import hashlib, sys
for path in sys.argv[1:]:
    with open(path, 'rb') as fh:
        print(hashlib.sha256(fh.read()).hexdigest(), path)
MANIFEST_PY
}

count_lines() { printf '%s\n' "$1" | grep -c . ; }

BEFORE_MANIFEST="$(manifest "${GUARDED[@]}")" \
    || die "could not hash the guarded files"
[ -n "$BEFORE_MANIFEST" ] \
    || die "the guarded-file manifest is empty"
n_before="$(count_lines "$BEFORE_MANIFEST")"
[ "$n_before" -eq "${#GUARDED[@]}" ] \
    || die "manifest covers $n_before file(s), expected ${#GUARDED[@]}"

GIT_BEFORE="$(git status --porcelain 2>/dev/null || echo '(not a git worktree)')"

# --- sandbox, strictly bounded ----------------------------------------------
TMPROOT="${TMPDIR:-/tmp}"
TMPROOT="${TMPROOT%/}"
[ -d "$TMPROOT" ] || die "temporary directory $TMPROOT does not exist"
SANDBOX_PREFIX="$TMPROOT/bathron-i18n-mutation."
if fault_is sandbox; then
    SANDBOX_PREFIX="/proc/nonexistent-by-design/bathron-i18n-mutation."
fi
SANDBOX="$(mktemp -d "${SANDBOX_PREFIX}XXXXXX" 2>/dev/null)" \
    || die "could not create a sandbox under $TMPROOT"
[ -d "$SANDBOX" ] || die "mktemp returned $SANDBOX, which is not a directory"
case "$SANDBOX" in
    "$SANDBOX_PREFIX"??????) : ;;
    *) die "mktemp returned an unexpected path: $SANDBOX" ;;
esac
printf 'bathron i18n mutation sandbox\n' > "$SANDBOX/$MARKER_NAME" \
    || die "could not write the sandbox marker"

# Removes ONLY the exact directory mktemp returned, only if it still matches
# the expected prefix AND still carries the marker this script wrote.
cleanup() {
    [ -n "$SANDBOX" ] || return 0
    case "$SANDBOX" in
        "$SANDBOX_PREFIX"??????) : ;;
        *) printf '  refusing to remove %s: path does not match the sandbox template\n' "$SANDBOX"
           return 0 ;;
    esac
    if [ ! -d "$SANDBOX" ]; then return 0; fi
    if [ ! -f "$SANDBOX/$MARKER_NAME" ]; then
        printf '  refusing to remove %s: sandbox marker is missing\n' "$SANDBOX"
        return 0
    fi
    rm -rf -- "$SANDBOX"
}
trap cleanup EXIT

mkdir -p "$SANDBOX/i18n" || die "could not populate the sandbox"
if fault_is copy; then
    printf '  (injected fault: sources not copied)\n'
else
    cp index.html          "$SANDBOX/index.html"          || die "could not copy index.html"
    cp i18n/i18n.py        "$SANDBOX/i18n/i18n.py"        || die "could not copy i18n.py"
    cp i18n/homepage.fr.po "$SANDBOX/i18n/homepage.fr.po" || die "could not copy the catalogue"
fi
for f in index.html i18n/i18n.py i18n/homepage.fr.po; do
    [ -s "$SANDBOX/$f" ] || die "sandbox is missing $f — preparation failed"
done
printf '  sandbox: %s\n' "$SANDBOX"

PO="$SANDBOX/i18n/homepage.fr.po"
SRC="$SANDBOX/index.html"
OUT="$SANDBOX/fr/index.html"
PRISTINE_PO="$SANDBOX/pristine.po"
PRISTINE_SRC="$SANDBOX/pristine.html"
cp "$PO" "$PRISTINE_PO"   || die "could not snapshot the catalogue"
cp "$SRC" "$PRISTINE_SRC" || die "could not snapshot the source"

run() { ( cd "$SANDBOX" && python3 i18n/i18n.py "$@" ); }
reset_sandbox() {
    cp "$PRISTINE_PO" "$PO"   || die "could not restore the sandbox catalogue"
    cp "$PRISTINE_SRC" "$SRC" || die "could not restore the sandbox source"
    run extract >/dev/null    || die "extract failed while resetting the sandbox"
}

ORIG='Verify the chain yourself, from your own machine.'
MUT='Verify the chain yourself, from your own laptop.'
grep -qF "$ORIG" "$SRC" || die "anchor sentence not found in index.html"

expect_refusal() {
    label="$1"
    run build fr >/dev/null 2>&1
    rc=$?
    if [ "$rc" -eq 0 ]; then
        bad "$label: build succeeded, expected refusal"
    else
        ok "$label: build refused (exit $rc)"
    fi
    if [ -e "$OUT" ]; then
        bad "$label: fr/index.html survives a refused build"
    else
        ok "$label: no French page on disk"
    fi
}

# ---------------------------------------------------------------- 1
say 'clean build succeeds'
run extract >/dev/null || die "extract failed on a pristine sandbox"
if run build fr >/dev/null; then ok 'build exited 0'; else bad 'clean build failed'; fi
if [ -f "$OUT" ]; then
    SIZE="$(wc -c < "$OUT" | tr -d ' ')"
    ok "fr/index.html built ($SIZE bytes)"
else
    bad 'fr/index.html not produced'; SIZE=0
fi
if grep -q '<html lang="fr"' "$OUT" 2>/dev/null; then
    ok 'page declares lang="fr"'
else
    bad 'page does not declare lang="fr"'
fi

# ---------------------------------------------------------------- 2
say 'English changed, catalogue untouched'
python3 - "$SRC" "$ORIG" "$MUT" <<'EDIT_PY' || die "could not mutate the English source"
import sys
p, a, b = sys.argv[1:4]
s = open(p, encoding='utf-8').read()
assert s.count(a) == 1, 'anchor appears %d times' % s.count(a)
open(p, 'w', encoding='utf-8').write(s.replace(a, b))
EDIT_PY
if cmp -s "$PO" "$PRISTINE_PO"; then ok 'catalogue untouched'; else bad 'catalogue changed'; fi
run extract >/dev/null || die "extract failed after mutating the source"
expect_refusal 'missing translation'
ok "the ${SIZE}-byte page from step 1 was removed, not served stale"
reset_sandbox

# ---------------------------------------------------------------- 3
say 'catalogue absent'
mv "$PO" "$SANDBOX/parked.po" || die "could not park the catalogue"
expect_refusal 'absent catalogue'
mv "$SANDBOX/parked.po" "$PO" || die "could not restore the parked catalogue"
reset_sandbox

# ---------------------------------------------------------------- 4
say 'fuzzy entry'
# The property under test is that the GENERATOR refuses a "#, fuzzy" entry. The
# flag is injected deterministically, reproducing what msgmerge writes: the
# msgid is updated to the new English, the old translation is kept, and the
# entry is flagged. Python only, so neither this test nor the deploy that runs
# it depends on the Ubuntu archives. Compatibility with the REAL msgmerge
# output is covered separately, and optionally, by i18n/msgmerge-compat.sh.
python3 - "$SRC" "$ORIG" "$MUT" <<'EDIT2_PY' || die "could not mutate the English source"
import sys
p, a, b = sys.argv[1:4]
s = open(p, encoding='utf-8').read()
open(p, 'w', encoding='utf-8').write(s.replace(a, b))
EDIT2_PY
run extract >/dev/null || die "extract failed before the fuzzy case"
python3 - "$PO" "$ORIG" "$MUT" <<'FUZZ_PY' || die "could not inject the fuzzy flag"
import sys
p, old, new = sys.argv[1:4]
lines = open(p, encoding='utf-8').read().split('\n')
out, done = [], False
for ln in lines:
    if ln == 'msgid "%s"' % old:
        out.append('#, fuzzy')                 # exactly what msgmerge emits
        out.append('msgid "%s"' % new)         # msgid updated, translation stale
        done = True
        continue
    out.append(ln)
assert done, 'anchor msgid not found in the catalogue'
open(p, 'w', encoding='utf-8').write('\n'.join(out))
FUZZ_PY
if grep -q '^#, fuzzy' "$PO"; then ok 'entry carries a fuzzy flag'
else bad 'no fuzzy flag was injected'; fi
expect_refusal 'fuzzy entry'

# ---------------------------------------------------------------- 5
say 'fuzzy cleared and translated — build succeeds again'
python3 - "$PO" "$MUT" <<'CLEAR_PY' || die "could not clear the fuzzy flag"
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
    if ln == 'msgid "%s"' % mut:
        out.append(ln)
        out.append('msgstr "Verifiez la chaine depuis votre propre ordinateur."')
        i += 2; continue
    out.append(ln); i += 1
open(p, 'w', encoding='utf-8').write('\n'.join(out))
CLEAR_PY
if grep -q '^#, fuzzy' "$PO"; then bad 'a fuzzy flag remains'; else ok 'no fuzzy flag left'; fi
if run build fr >/dev/null; then ok 'build exited 0'; else bad 'build failed after translating'; fi
if grep -qF 'Verifiez la chaine depuis votre propre ordinateur.' "$OUT" 2>/dev/null; then
    ok 'the new translation is in the page'
else
    bad 'new translation absent from the page'
fi
reset_sandbox

# ---------------------------------------------------------------- 6
say 'duplicate entry in the catalogue'
python3 - "$PO" <<'DUP_PY' || die "could not duplicate an entry"
import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
i = s.index('msgid "', s.index('msgstr ""') + 8)      # first real entry
j = s.index('\n\n', i) + 2
open(p, 'w', encoding='utf-8').write(s[:j] + s[i:j] + s[j:])
DUP_PY
expect_refusal 'duplicate entry'
reset_sandbox

# ---------------------------------------------------------------- 7
say 'malformed catalogue entry'
printf 'this line is not valid PO syntax\n' >> "$PO" || die "could not corrupt the catalogue"
expect_refusal 'malformed catalogue'
reset_sandbox

# ---------------------------------------------------------------- 8
say 'sandbox recovered, and the calling worktree was never touched'
if run build fr >/dev/null; then ok 'sandbox builds again after every mutation'
else bad 'sandbox does not build after restoration'; fi
if cmp -s "$SRC" "$PRISTINE_SRC"; then ok 'sandbox index.html byte-identical to pristine'
else bad 'sandbox index.html diverged'; fi
if cmp -s "$PO" "$PRISTINE_PO"; then ok 'sandbox catalogue byte-identical to pristine'
else bad 'sandbox catalogue diverged'; fi

# Injected fault "skipguard" reproduces the ORIGINAL defect: the guarded-file
# checks silently do not run. die() cannot catch that — only the assertion
# counter below can, which is exactly what it is there for.
if fault_is skipguard; then
    printf '  (injected fault: guarded-file checks skipped)\n'
else
    AFTER_MANIFEST="$(manifest "${GUARDED[@]}")" || die "could not re-hash the guarded files"
    if fault_is guard; then
        AFTER_MANIFEST="${AFTER_MANIFEST}
    deadbeef  injected-fault"
    fi
    n_after="$(count_lines "$AFTER_MANIFEST")"
    [ "$n_after" -eq "${#GUARDED[@]}" ] || die "post-run manifest covers $n_after file(s), expected ${#GUARDED[@]}"
    if [ "$AFTER_MANIFEST" = "$BEFORE_MANIFEST" ]; then
        i=0
        while [ $i -lt ${#GUARDED[@]} ]; do
            ok "unchanged: ${GUARDED[$i]}"
            i=$((i+1))
        done
    else
        bad 'a guarded file changed during the test'
        printf '%s\n' "$BEFORE_MANIFEST" > "$SANDBOX/before.txt"
        printf '%s\n' "$AFTER_MANIFEST"  > "$SANDBOX/after.txt"
        diff "$SANDBOX/before.txt" "$SANDBOX/after.txt" | sed 's/^/    /'
    fi

    GIT_AFTER="$(git status --porcelain 2>/dev/null || echo '(not a git worktree)')"
    if [ "$GIT_BEFORE" = "$GIT_AFTER" ]; then ok 'git status identical before and after'
    else
        bad 'git status changed'
        printf '    before: %s\n    after : %s\n' "$GIT_BEFORE" "$GIT_AFTER"
    fi
fi

# --- completeness: a truncated run must never look like a successful one -----
printf '\n================================\n'
if [ "$STEP" -ne "$STEPS_EXPECTED" ]; then
    printf 'MUTATION TEST: FAIL — %d of %d steps ran; the test did not complete.\n' \
        "$STEP" "$STEPS_EXPECTED"
    exit 3
fi
if [ "$ASSERTIONS" -ne "$ASSERTIONS_EXPECTED" ]; then
    printf 'MUTATION TEST: FAIL — %d assertions ran, expected %d.\n' \
        "$ASSERTIONS" "$ASSERTIONS_EXPECTED"
    exit 3
fi
if [ $FAILED -eq 0 ]; then
    printf 'MUTATION TEST: PASS (%d steps, %d assertions) — no incomplete, stale,\n' \
        "$STEP" "$ASSERTIONS"
    printf 'fuzzy, duplicated or malformed French catalogue can produce a page.\n'
    exit 0
fi
printf 'MUTATION TEST: FAIL\n'
exit 1
