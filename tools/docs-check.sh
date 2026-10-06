#!/usr/bin/env bash
# Single entry point for pull requests, publication and offline checks.
# Bash 3.2; Python standard library and the already installed pinned mdBook.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)" || exit 3
cd "$ROOT" || exit 3
OFFLINE=0
if [ "${1:-}" = '--offline' ]; then OFFLINE=1
elif [ "$#" -gt 0 ]; then echo 'usage: tools/docs-check.sh [--offline]'; exit 2
fi
FAILED=0
GATES=()
gate() {
    local name="$1"; shift
    printf '\n-- %s\n' "$name"
    if "$@"; then GATES+=("PASS $name")
    else GATES+=("FAIL $name"); FAILED=1
    fi
}
build_book() {
    if ! command -v mdbook >/dev/null 2>&1; then
        echo 'Pinned mdBook is required; this script downloads nothing.'; return 1
    fi
    if [ "$(mdbook --version)" != 'mdbook v0.4.52' ]; then
        echo 'Unexpected mdBook version'; return 1
    fi
    mdbook build docs
}
gate 'public confidentiality' python3 tools/confidentiality-check.py
gate 'vocabulary V1–V12' python3 tools/vocab-check.py
gate 'sandbox mutation tests' python3 tools/mutation-test.py
gate 'homepage generation' python3 i18n/i18n.py build all
gate 'book build' build_book
gate 'links and anchors' python3 tools/link-check.py --only links
gate 'direct redirects' python3 tools/link-check.py --only redirects
gate 'referenced images' python3 tools/link-check.py --only images
gate 'sitemap' python3 tools/gen-sitemap.py --check
# Offline is never a publication bypass: unresolved or unchecked sources fail.
gate 'pinned normative sources' python3 tools/link-check.py --only sources
if [ -n "${DOCS_BASE:-}" ] || [ -n "${DOCS_BRANCH:-}" ]; then
    gate 'PR metadata' python3 tools/confidentiality-check.py --metadata
elif [ "$OFFLINE" -eq 1 ]; then
    echo 'PR metadata: not run (offline working tree, no PR range supplied).'
elif [ "${GITHUB_EVENT_NAME:-}" = 'pull_request' ]; then
    echo 'FAIL: missing pull-request metadata'; FAILED=1
else
    echo 'PR metadata: not applicable to a non-PR event.'
fi
printf '\n'
for result in "${GATES[@]}"; do printf '%s\n' "$result"; done
if [ "$FAILED" -eq 0 ]; then echo 'DOCS CHECK: PASS'
else echo 'DOCS CHECK: FAIL'
fi
exit "$FAILED"
