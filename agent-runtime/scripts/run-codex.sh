#!/usr/bin/env bash
set -euo pipefail
runtime_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd -P)
exec python3 "$runtime_dir/cycle.py" --engine codex "$@"
