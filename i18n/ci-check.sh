#!/usr/bin/env bash
# BATHRON homepage i18n — the single set of checks.
#
# This script is the ONLY definition of "the i18n gates". The pull-request
# workflow and the Pages deploy workflow both call it, so the checks that guard
# a PR and the checks that guard a publication cannot drift apart.
#
# It needs Python 3 and git. Nothing is installed, nothing is downloaded, no
# secret is read: a site publication must not depend on a package archive.
#
#   bash i18n/ci-check.sh
#     0 = every gate passed
#     1 = at least one gate failed (details above the summary)
#
# Not included on purpose: i18n/msgmerge-compat.sh, which needs GNU gettext.
# It is an optional, separate check — see i18n/README.md.
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

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
gate 'catalogue audit (check fr)' python3 i18n/i18n.py check fr

# --- 4. build ----------------------------------------------------------------
gate 'build fr' python3 i18n/i18n.py build fr

# --- 5. structural validation of both served pages ---------------------------
gate 'verify en' python3 i18n/i18n.py verify en
gate 'verify fr' python3 i18n/i18n.py verify fr
gate 'EN/FR skeleton comparison' python3 i18n/i18n.py compare

# --- 6. static overflow scan -------------------------------------------------
# Reads the markup for fixed widths wider than the smallest supported viewport.
# It does NOT lay the page out and is not a substitute for looking at it in a
# browser; that remains a local editorial step.
gate 'static-overflow-check' python3 i18n/i18n.py static-overflow-check

# --- 7. the generated page must exist and be well-formed ---------------------
artifact_present() {
    [ -s fr/index.html ] || { echo '  fr/index.html is missing or empty'; return 1; }
    grep -q '<html lang="fr"' fr/index.html || { echo '  fr/index.html does not declare lang="fr"'; return 1; }
    if grep -q 'data-i18n-context' fr/index.html; then
        echo '  build metadata leaked into the generated page'; return 1
    fi
    printf '  fr/index.html present, %s bytes, lang=fr, no build metadata\n' "$(wc -c < fr/index.html)"
}
gate 'generated page present' artifact_present

# --- 8. git cleanliness of tracked files -------------------------------------
git_clean() {
    local rc=0 tracked dirty
    tracked="$(git ls-files -- fr/ i18n/homepage.pot)"
    if [ -n "$tracked" ]; then
        echo '  generated files are tracked and must not be:'
        printf '    %s\n' $tracked
        rc=1
    else
        echo '  no generated artifact is tracked'
    fi
    # running the gates above must leave the tree exactly as it was found
    local after
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
