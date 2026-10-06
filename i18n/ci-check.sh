#!/usr/bin/env bash
# Keep the established CI entry point; translation generation has been retired.
set -eu
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/tools/site-check.py"
