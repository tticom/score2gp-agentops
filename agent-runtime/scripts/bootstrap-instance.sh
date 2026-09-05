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

ensure_setfacl() {
  if command -v setfacl >/dev/null 2>&1; then
    return
  fi
  if ! command -v sudo >/dev/null 2>&1; then
    echo "error: setfacl is required; install it with: sudo apt-get update && sudo apt-get install -y acl" >&2
    exit 69
  fi
  if ! sudo -n true >/dev/null 2>&1; then
    echo "error: setfacl is required; run: sudo apt-get update && sudo apt-get install -y acl" >&2
    exit 69
  fi
  sudo apt-get update
  sudo apt-get install --yes acl
  require_command setfacl
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
    if [ "$(git -C "$repo_dir" branch --show-current)" != "$ref" ]; then
      echo "error: checkout is on another branch; checkpoint it before explicit switching: $repo_dir" >&2
      exit 75
    fi
    if [ "$(git -C "$repo_dir" rev-list --count "origin/$ref..HEAD")" != 0 ]; then
      echo "error: local commits are not on origin/$ref; preserve and push the task branch: $repo_dir" >&2
      exit 75
    fi
    git -C "$repo_dir" merge --ff-only "origin/$ref"
  else
    echo "error: requested remote branch does not exist: $ref" >&2
    exit 75
  fi
}

require_command git
require_command docker
ensure_setfacl
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
