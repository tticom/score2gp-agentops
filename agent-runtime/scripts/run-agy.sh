#!/usr/bin/env bash
set -euo pipefail

workspace_root=${SCORE2GP_WORKSPACE_ROOT:-"$HOME/work/score2gp-workspace"}
source_dir=${SCORE2GP_PRODUCT_DIR:-"$workspace_root/score2gp"}
task_slug=${SCORE2GP_TASK:-sandbox}
task_worktree=${SCORE2GP_TASK_WORKTREE:-"$workspace_root/score2gp-$task_slug-worktree"}
config_volume=${AGY_CONFIG_VOLUME:-agy-config}
state_volume=${AGY_STATE_VOLUME:-agy-state}
image_tag=${SCORE2GP_AGENT_IMAGE:-score2gp-agent:local}

case "$task_slug" in
  *[!A-Za-z0-9._-]*) echo "error: SCORE2GP_TASK contains unsupported characters" >&2; exit 64 ;;
esac

if [ ! -f "$source_dir/pyproject.toml" ] || { [ ! -d "$source_dir/.git" ] && [ ! -f "$source_dir/.git" ]; }; then
  echo "error: product Git worktree not found: $source_dir" >&2
  exit 66
fi
if [ "$source_dir" = "$task_worktree" ]; then
  echo "error: SCORE2GP_TASK_WORKTREE must differ from the source worktree" >&2
  exit 64
fi

if [ ! -e "$task_worktree" ]; then
  mkdir -p "$(dirname "$task_worktree")"
  git -C "$source_dir" worktree add --detach "$task_worktree" "${SCORE2GP_BASE_REF:-HEAD}"
elif [ ! -f "$task_worktree/pyproject.toml" ] || { [ ! -d "$task_worktree/.git" ] && [ ! -f "$task_worktree/.git" ]; }; then
  echo "error: task worktree path exists but is not a Score2GP Git worktree: $task_worktree" >&2
  exit 66
fi

docker volume create "$config_volume" >/dev/null
docker volume create "$state_volume" >/dev/null
exec docker run --rm -it \
  --network bridge \
  --user 10001:10001 \
  --read-only \
  --workdir /workspace/score2gp \
  --tmpfs /tmp:rw,noexec,nosuid,size=256m \
  --mount "type=bind,src=$task_worktree,dst=/workspace/score2gp,readonly=false" \
  --mount "type=volume,src=$config_volume,dst=/home/agent/.config" \
  --mount "type=volume,src=$state_volume,dst=/home/agent/.gemini" \
  --entrypoint agy \
  "$image_tag" --dangerously-skip-permissions "$@"
