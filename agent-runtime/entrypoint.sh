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

# The task worktree is explicit and writable only because editable installation
# may create metadata beside the mounted source. No parent workspace is mounted.
python -m pip install --user --no-deps --no-build-isolation --editable "$product_dir" >/dev/null
exec "$@"
