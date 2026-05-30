#!/usr/bin/env bash
set -euo pipefail

TASK_SLUG="${1:-pdf-to-gp-smoke-v1}"
WORKSPACE_ROOT="${2:-/home/tticom/work/score2gp-workspace}"

DEV="${WORKSPACE_ROOT}/agent-worktrees/${TASK_SLUG}/score2gp-developer"
OUT="${WORKSPACE_ROOT}/score2gp-control/tasks/${TASK_SLUG}/logs/developer-diff.patch"

cd "${DEV}"
mkdir -p "$(dirname "${OUT}")"
git diff --stat > "${OUT}.stat"
git diff > "${OUT}"

echo "Saved developer diff:"
echo "${OUT}.stat"
echo "${OUT}"
