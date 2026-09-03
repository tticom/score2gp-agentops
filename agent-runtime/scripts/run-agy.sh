#!/usr/bin/env bash
set -euo pipefail

workspace_root=${SCORE2GP_WORKSPACE_ROOT:-"$HOME/work/score2gp-workspace"}
product_dir=${SCORE2GP_PRODUCT_DIR:-"$workspace_root/score2gp"}
config_volume=${AGY_CONFIG_VOLUME:-agy-config}
image_tag=${SCORE2GP_AGENT_IMAGE:-score2gp-agent:local}

if [ ! -f "$product_dir/pyproject.toml" ]; then
  echo "error: product worktree not found: $product_dir" >&2
  exit 66
fi

docker volume create "$config_volume" >/dev/null
exec docker run --rm -it \
  --network bridge \
  --user 10001:10001 \
  --read-only \
  --workdir /workspace/score2gp \
  --tmpfs /tmp:rw,noexec,nosuid,size=256m \
  --mount "type=bind,src=$product_dir,dst=/workspace/score2gp,rw" \
  --mount "type=volume,src=$config_volume,dst=/home/agent/.config" \
  --entrypoint agy \
  "$image_tag" "$@"
