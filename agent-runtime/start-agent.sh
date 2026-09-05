#!/bin/sh
set -eu

runtime_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
product_dir=${SCORE2GP_PRODUCT_DIR:-}
task_slug=${SCORE2GP_TASK:-}
task_branch=${SCORE2GP_TASK_BRANCH:?set SCORE2GP_TASK_BRANCH to the assigned branch}

if [ -z "$product_dir" ] || [ ! -d "$product_dir" ]; then
  echo "usage: SCORE2GP_PRODUCT_DIR=/absolute/task/worktree SCORE2GP_TASK=task-slug $0 [command ...]" >&2
  exit 64
fi
case "$product_dir" in
  /*) ;;
  *) echo "error: SCORE2GP_PRODUCT_DIR must be absolute" >&2; exit 64 ;;
esac
if [ -z "$task_slug" ]; then
  echo "error: SCORE2GP_TASK is required" >&2
  exit 64
fi
case "$task_slug" in
  *[!A-Za-z0-9._-]*) echo "error: SCORE2GP_TASK contains unsupported characters" >&2; exit 64 ;;
esac
if [ ! -f "$product_dir/pyproject.toml" ] || [ ! -d "$product_dir/.git" ] && [ ! -f "$product_dir/.git" ]; then
  echo "error: SCORE2GP_PRODUCT_DIR must be one Score2GP git worktree" >&2
  exit 64
fi

export SCORE2GP_PRODUCT_DIR="$product_dir"
export SCORE2GP_TASK="$task_slug"
export SCORE2GP_TASK_BRANCH="$task_branch"
task_remote=$(git -C "$product_dir" remote get-url origin)
python3 "$runtime_dir/task_branch.py" verify --repo "$product_dir" --branch "$task_branch" --remote "$task_remote"
export COMPOSE_PROJECT_NAME="score2gp-agent-$task_slug"
if [ "$#" -eq 0 ]; then
  set -- python -m score2gp.cli --help
fi
status=0
docker compose --file "$runtime_dir/compose.yaml" run --rm agent "$@" || status=$?
python3 "$runtime_dir/task_branch.py" verify --repo "$product_dir" --branch "$task_branch" --remote "$task_remote"
exit "$status"
