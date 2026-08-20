#!/usr/bin/env bash
# BATHRON homepage i18n — OPTIONAL compatibility check against real GNU gettext.
#
# The fail-closed guarantee is proven by i18n/mutation-test.sh, which needs
# Python only and is therefore safe on the deployment path. This script answers
# a narrower, separate question: does the strict PO reader still understand what
# a REAL `msgmerge --update` writes into the catalogue?
#
# It is deliberately NOT part of the deploy gates. A site publication must not
# depend on the Ubuntu archives being reachable.
#
#   bash i18n/msgmerge-compat.sh
#     0  = compatible
#     1  = incompatible (a real finding — investigate before trusting msgmerge)
#    77  = skipped, msgmerge is not installed (POSIX "skipped" convention)
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)" || exit 3
cd "$ROOT" || exit 3

if ! command -v msgmerge >/dev/null 2>&1; then
    printf 'SKIP — msgmerge not installed. Install "gettext" to run this check.\n'
    exit 77
fi
printf '  %s\n' "$(msgmerge --version | head -1)"

FAILED=0
ok()  { printf '  PASS  %s\n' "$1"; }
bad() { printf '  FAIL  %s\n' "$1"; FAILED=1; }

# Python, not sha256sum: a stock macOS has neither sha256sum nor a guaranteed
# shasum on PATH, and Python 3 is already required.
digest() {
    python3 -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$1"
}
BEFORE_SRC="$(digest index.html)"          || exit 3
BEFORE_PO="$(digest i18n/homepage.fr.po)"  || exit 3

TMPROOT="${TMPDIR:-/tmp}"; TMPROOT="${TMPROOT%/}"
SANDBOX_PREFIX="$TMPROOT/bathron-i18n-msgmerge."
SANDBOX="$(mktemp -d "${SANDBOX_PREFIX}XXXXXX")" || exit 3
MARKER_NAME=".bathron-msgmerge-sandbox"
printf 'bathron i18n msgmerge sandbox\n' > "$SANDBOX/$MARKER_NAME" || exit 3
cleanup() {
    [ -n "${SANDBOX:-}" ] || return 0
    case "$SANDBOX" in
        "$SANDBOX_PREFIX"??????) : ;;
        *) printf '  refusing to remove %s: path does not match the template\n' "$SANDBOX"; return 0 ;;
    esac
    [ -d "$SANDBOX" ] || return 0
    [ -f "$SANDBOX/$MARKER_NAME" ] || {
        printf '  refusing to remove %s: marker missing\n' "$SANDBOX"; return 0; }
    rm -rf -- "$SANDBOX"
}
trap cleanup EXIT

mkdir -p "$SANDBOX/i18n"
cp index.html          "$SANDBOX/index.html"
cp i18n/i18n.py        "$SANDBOX/i18n/i18n.py"
cp i18n/homepage.fr.po "$SANDBOX/i18n/homepage.fr.po"
printf '  sandbox: %s\n\n' "$SANDBOX"

run() { ( cd "$SANDBOX" && python3 i18n/i18n.py "$@" ); }

ORIG='Verify the chain yourself, from your own machine.'
MUT='Verify the chain yourself, from your own laptop.'

# 1. baseline
run extract >/dev/null
if run build fr >/dev/null; then ok 'baseline build succeeds'; else bad 'baseline build failed'; fi

# 2. change the English, then let REAL msgmerge update the catalogue
python3 - "$SANDBOX/index.html" "$ORIG" "$MUT" <<'EDITPY'
import sys
p, a, b = sys.argv[1:4]
s = open(p, encoding='utf-8').read()
assert s.count(a) == 1
open(p, 'w', encoding='utf-8').write(s.replace(a, b))
EDITPY
run extract >/dev/null
msgmerge --quiet --update --backup=none \
    "$SANDBOX/i18n/homepage.fr.po" "$SANDBOX/i18n/homepage.pot"
rc=$?
[ $rc -eq 0 ] && ok 'msgmerge --update exited 0' || bad "msgmerge exited $rc"

grep -q '^#, fuzzy' "$SANDBOX/i18n/homepage.fr.po" \
    && ok 'msgmerge flagged the changed entry fuzzy' \
    || bad 'msgmerge produced no fuzzy flag — the premise of the fuzzy gate is wrong'

# 3. the strict reader must REJECT what msgmerge just wrote
out="$(run build fr 2>&1)"; rc=$?
if [ $rc -ne 0 ]; then
    ok "build refused msgmerge output (exit $rc)"
    printf '        %s\n' "$(printf '%s\n' "$out" | grep -E 'FUZZY|CATALOGUE|REFUSED' | head -2)"
else
    bad 'build ACCEPTED a catalogue msgmerge had just flagged fuzzy'
fi
[ -e "$SANDBOX/fr/index.html" ] && bad 'a French page survived' || ok 'no French page on disk'

# 4. msgmerge emits extras (#| previous-msgid, #~ obsolete). The reader must
#    handle them deliberately rather than by accident.
if grep -q '^#|' "$SANDBOX/i18n/homepage.fr.po"; then
    ok 'msgmerge emitted "#|" previous-msgid comments (ignored as comments)'
fi
if grep -q '^#~' "$SANDBOX/i18n/homepage.fr.po"; then
    ok 'msgmerge emitted "#~" obsolete blocks (explicitly rejected)'
fi

# 5. the calling worktree must be untouched
[ "$(digest index.html)" = "$BEFORE_SRC" ] \
    && ok 'unchanged: index.html' || bad 'MODIFIED: index.html'
[ "$(digest i18n/homepage.fr.po)" = "$BEFORE_PO" ] \
    && ok 'unchanged: i18n/homepage.fr.po' || bad 'MODIFIED: i18n/homepage.fr.po'

printf '\n'
if [ $FAILED -eq 0 ]; then
    printf 'MSGMERGE COMPATIBILITY: PASS\n'; exit 0
fi
printf 'MSGMERGE COMPATIBILITY: FAIL\n'; exit 1
