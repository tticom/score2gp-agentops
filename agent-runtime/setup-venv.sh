#!/bin/sh
set -eu

runtime_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
if [ "$#" -eq 0 ]; then
  set -- python -m score2gp.cli --help
fi
exec "$runtime_dir/start-agent.sh" /bin/sh -ec '
  venv=/home/agent/.venv
  if [ ! -x "$venv/bin/python" ]; then
    python -m venv --system-site-packages "$venv"
  fi
  env -u PIP_USER "$venv/bin/python" -m pip install --no-deps --no-build-isolation --editable /workspace/score2gp >/dev/null
  export PATH="$venv/bin:$PATH"
  echo "ready: disposable $venv (removed when this command exits)"
  exec "$@"
' sh "$@"
