#!/usr/bin/env bash
# BATHRON homepage i18n — the single set of checks.
#
# This script is the ONLY definition of "the i18n gates". The pull-request
# workflow and the Pages deploy workflow both call it, so the checks that guard
# a PR and the checks that guard a publication cannot drift apart.
#
# Dependencies: Python 3, git, and a POSIX shell. Everything here runs on the
# Bash 3.2 that macOS ships as well as on Bash 5 — no associative arrays, and
# no `sha256sum`, which a stock macOS does not have. Nothing is installed,
# nothing is downloaded, no secret is read: a site publication must not depend
# on a package archive.
#
#   bash i18n/ci-check.sh
#     0 = every gate passed
#     1 = at least one gate failed (details above the summary)
#
# Not included on purpose: i18n/msgmerge-compat.sh, which needs GNU gettext.
# It is an optional, separate check — see i18n/README.md.
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)" || exit 3
cd "$ROOT" || exit 3

FAILED=0
GATES=()

# Snapshot the tree BEFORE any gate runs. The property to enforce is that the
# checks themselves leave the tree exactly as they found it — not that the
# developer's tree happened to be clean when they ran the script.
GIT_BEFORE="$(git status --porcelain 2>/dev/null || echo '(no git)')"

gate() {                       # gate <name> <command...>
    local name="$1"; shift
    printf '\n\033[1m── %s\033[0m\n' "$name"
    if "$@"; then
        GATES+=("PASS  $name")
    else
        local rc=$?
        printf '  gate failed with exit %d\n' "$rc"
        GATES+=("FAIL  $name")
        FAILED=1
    fi
}

# --- the environment this actually ran in, printed for the record ------------
printf '\033[1m── environment\033[0m\n'
printf '  python   : %s\n' "$(python3 -VV | tr '\n' ' ')"
printf '  executable: %s\n' "$(command -v python3)"
printf '  git      : %s\n' "$(git --version)"
printf '  commit   : %s\n' "$(git rev-parse HEAD 2>/dev/null || echo '(no git)')"

# --- 1. unit tests -----------------------------------------------------------
gate 'unit tests' python3 i18n/test_i18n.py

# --- 2. fail-closed mutation test, in an isolated sandbox --------------------
# Python-only since the fuzzy flag is injected deterministically; the deploy
# path therefore stays free of apt and gettext.
gate 'fail-closed mutation test' bash i18n/mutation-test.sh

# --- 3. catalogue ------------------------------------------------------------
gate 'extract template' python3 i18n/i18n.py extract
gate 'catalogue audit (every language)' python3 i18n/i18n.py check all

# --- 4. build ----------------------------------------------------------------
gate 'build every language' python3 i18n/i18n.py build all

# --- 5. structural validation of both served pages ---------------------------
gate 'verify every page' python3 i18n/i18n.py verify all
gate 'skeleton comparison' python3 i18n/i18n.py compare

# --- 6. static overflow scan -------------------------------------------------
# Reads the markup for fixed widths wider than the smallest supported viewport.
# It does NOT lay the page out and is not a substitute for looking at it in a
# browser; that remains a local editorial step.
gate 'static-overflow-check' python3 i18n/i18n.py static-overflow-check

# --- 7. the generated page must exist and be well-formed ---------------------
artifact_present() {
    local rc=0
    # The list comes from the language table, so adding a language cannot leave
    # this gate silently checking the old set.
    python3 i18n/i18n.py languages | awk '$NF != "(source)" {print $1, $NF}' |
    while read -r code out; do
        f="$out/index.html"
        if [ ! -s "$f" ]; then echo "  $f is missing or empty"; exit 1; fi
        if ! grep -q "<html lang=\"$code\"" "$f"; then
            echo "  $f does not declare lang=\"$code\""; exit 1
        fi
        if grep -q 'data-i18n-context' "$f"; then
            echo "  build metadata leaked into $f"; exit 1
        fi
        if grep -q '<script' "$f"; then echo "  $f contains a script"; exit 1; fi
        printf '  %-20s %7s bytes  lang=%s\n' "$f" "$(wc -c < "$f" | tr -d ' ')" "$code"
    done || rc=1
    return $rc
}
gate 'generated page present' artifact_present

# --- 8. git cleanliness of tracked files -------------------------------------
git_clean() {
    local rc=0 tracked after
    tracked="$(git ls-files -- fr/ es/ zh-hans/ hi/ ar/ i18n/homepage.pot)"
    if [ -n "$tracked" ]; then
        echo '  generated files are tracked and must not be:'
        printf '    %s\n' $tracked
        rc=1
    else
        echo '  no generated artifact is tracked'
    fi
    # running the gates above must leave the tree exactly as it was found
    after="$(git status --porcelain 2>/dev/null || echo '(no git)')"
    if [ "$after" != "$GIT_BEFORE" ]; then
        echo '  the checks changed the working tree:'
        diff <(printf '%s\n' "$GIT_BEFORE") <(printf '%s\n' "$after") \
            | sed 's/^/    /' || true
        rc=1
    else
        echo '  the checks left the working tree exactly as they found it'
    fi
    # on a clean checkout (CI) the tree must additionally be pristine
    if [ -z "$GIT_BEFORE" ]; then
        echo '  checkout was pristine before the checks'
    else
        echo '  note: tree already had local changes before the checks:'
        printf '%s\n' "$GIT_BEFORE" | sed 's/^/    /'
    fi
    return $rc
}
gate 'git cleanliness' git_clean

# --- summary -----------------------------------------------------------------
printf '\n\033[1m── summary\033[0m\n'
for g in "${GATES[@]}"; do printf '  %s\n' "$g"; done
printf '\n'
if [ $FAILED -eq 0 ]; then
    printf 'I18N CI CHECK: PASS (%d gates)\n' "${#GATES[@]}"
    exit 0
fi
printf 'I18N CI CHECK: FAIL\n'
exit 1
