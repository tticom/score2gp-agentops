#!/usr/bin/env bash
set -euo pipefail

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
runtime_dir=$(CDPATH= cd -- "$script_dir/.." && pwd -P)
workspace_root=${SCORE2GP_WORKSPACE_ROOT:-"$HOME/work/score2gp-workspace"}
product_dir=${SCORE2GP_PRODUCT_DIR:?set SCORE2GP_PRODUCT_DIR to a published isolated task clone}
task_slug=${SCORE2GP_TASK:?set SCORE2GP_TASK to the assigned task}
: "${SCORE2GP_TASK_BRANCH:?set SCORE2GP_TASK_BRANCH to the published task branch}"

if [ ! -f "$product_dir/pyproject.toml" ]; then
  echo "error: product worktree not found: $product_dir" >&2
  exit 66
fi

SCORE2GP_PRODUCT_DIR="$product_dir" SCORE2GP_TASK="$task_slug" \
  "$runtime_dir/start-agent.sh" python -c 'import score2gp; print(score2gp.__file__)'
SCORE2GP_PRODUCT_DIR="$product_dir" SCORE2GP_TASK="$task_slug" \
  "$runtime_dir/start-agent.sh" python -m pytest -q tests/recognition/test_schemas.py
