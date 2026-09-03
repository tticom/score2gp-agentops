#!/bin/sh
set -eu

runtime_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
exec "$runtime_dir/start-agent.sh" /bin/sh -ec '
  venv=/workspace/score2gp/.venv
  if [ ! -x "$venv/bin/python" ]; then
    python -m venv --system-site-packages "$venv"
  fi
  env -u PIP_USER "$venv/bin/python" -m pip install --no-deps --no-build-isolation --editable /workspace/score2gp >/dev/null
  echo "ready: $venv"
'
