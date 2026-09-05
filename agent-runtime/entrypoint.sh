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

# Dependencies are baked into the image; import the mounted source without
# creating package metadata or a persistent user installation on the host.
export PYTHONPATH="$product_dir/src${PYTHONPATH:+:$PYTHONPATH}"
exec "$@"
