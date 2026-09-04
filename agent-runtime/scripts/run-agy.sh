#!/usr/bin/env bash
set -euo pipefail

workspace_root=${SCORE2GP_WORKSPACE_ROOT:-"$HOME/work/score2gp-workspace"}
product_dir=${SCORE2GP_PRODUCT_DIR:-"$workspace_root/score2gp"}
config_volume=${AGY_CONFIG_VOLUME:-agy-config}
state_volume=${AGY_STATE_VOLUME:-agy-state}
image_tag=${SCORE2GP_AGENT_IMAGE:-score2gp-agent:local}

if [ ! -f "$product_dir/pyproject.toml" ]; then
  echo "error: product worktree not found: $product_dir" >&2
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
  --mount "type=bind,src=$product_dir,dst=/workspace/score2gp,readonly=false" \
  --mount "type=volume,src=$config_volume,dst=/home/agent/.config" \
  --mount "type=volume,src=$state_volume,dst=/home/agent/.gemini" \
  --entrypoint agy \
  "$image_tag" "$@"
