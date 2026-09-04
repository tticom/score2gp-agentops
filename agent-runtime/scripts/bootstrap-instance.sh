#!/usr/bin/env bash
set -euo pipefail

workspace_root=${SCORE2GP_WORKSPACE_ROOT:-"$HOME/work/score2gp-workspace"}
agentops_ref=${AGENTOPS_REF:-main}
product_ref=${SCORE2GP_REF:-main}
skills_ref=${AGY_SKILLS_REF:-main}
agentops_repo=${AGENTOPS_REPO:-https://github.com/tticom/score2gp-agentops.git}
product_repo=${SCORE2GP_REPO:-https://github.com/tticom/score2gp.git}
skills_repo=${AGY_SKILLS_REPO:-https://github.com/tticom/agy-skills.git}

require_command() {
  command -v "$1" >/dev/null 2>&1 || { echo "error: required command not found: $1" >&2; exit 69; }
}

sync_repo() {
  local repo_dir=$1 remote_url=$2 ref=$3
  if [ ! -e "$repo_dir/.git" ]; then
    mkdir -p "$(dirname "$repo_dir")"
    git clone "$remote_url" "$repo_dir"
  fi
  if [ -n "$(git -C "$repo_dir" status --porcelain)" ]; then
    echo "error: refusing to update dirty repository: $repo_dir" >&2
    exit 75
  fi
  git -C "$repo_dir" fetch --prune origin
  if git -C "$repo_dir" show-ref --verify --quiet "refs/remotes/origin/$ref"; then
    git -C "$repo_dir" switch --force-create "$ref" "origin/$ref" 2>/dev/null \
      || git -C "$repo_dir" switch "$ref"
    git -C "$repo_dir" reset --hard "origin/$ref" >/dev/null
  else
    git -C "$repo_dir" switch "$ref"
  fi
}

require_command git
require_command docker
docker info >/dev/null
mkdir -p "$workspace_root"
sync_repo "$workspace_root/score2gp-agentops" "$agentops_repo" "$agentops_ref"
sync_repo "$workspace_root/score2gp" "$product_repo" "$product_ref"
sync_repo "$workspace_root/agy-skills" "$skills_repo" "$skills_ref"

SCORE2GP_AGENTOPS_DIR="$workspace_root/score2gp-agentops" \
  "$workspace_root/score2gp-agentops/agent-runtime/scripts/configure-shell-startup.sh"

echo "ready: $workspace_root"
echo "agentops: $(git -C "$workspace_root/score2gp-agentops" rev-parse HEAD)"
echo "product:  $(git -C "$workspace_root/score2gp" rev-parse HEAD)"
echo "skills:   $(git -C "$workspace_root/agy-skills" rev-parse HEAD)"
