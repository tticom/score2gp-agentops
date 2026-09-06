#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd -P)
venv="$repo_root/.venv"

if [ ! -x "$venv/bin/python" ]; then
  python3 -m venv "$venv"
fi

if ! "$venv/bin/python" -c 'import pytest' >/dev/null 2>&1; then
  "$venv/bin/python" -m pip install --disable-pip-version-check -r "$repo_root/agent-runtime/requirements.txt"
fi

printf '%s\n' "$venv/bin/python"
