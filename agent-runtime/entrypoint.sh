#!/bin/sh
set -eu

product_dir=/workspace/score2gp
if [ ! -f "$product_dir/pyproject.toml" ]; then
  echo "error: /workspace/score2gp is not a Score2GP worktree" >&2
  exit 64
fi

if [ -z "${SCORE2GP_TASK:-}" ]; then
  echo "error: SCORE2GP_TASK is required" >&2
  exit 64
fi

if [ -f /run/secrets/github-token ]; then
  export GH_TOKEN=$(tr -d '\r\n' < /run/secrets/github-token)
  test -n "$GH_TOKEN" || { echo "error: GitHub token secret is empty" >&2; exit 64; }
  export GIT_ASKPASS=/usr/local/bin/github-askpass.sh
  export GIT_TERMINAL_PROMPT=0
fi

# The task worktree is explicit and writable only because editable installation
# may create metadata beside the mounted source. No parent workspace is mounted.
python -m pip install --user --no-deps --no-build-isolation --editable "$product_dir" >/dev/null
exec "$@"
