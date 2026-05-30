#!/usr/bin/env bash
set -euo pipefail

ROLE="${1:-architect}"
TASK_SLUG="${2:-pdf-to-gp-smoke-v1}"
WORKSPACE_ROOT="${3:-/home/tticom/work/score2gp-workspace}"

WT="${WORKSPACE_ROOT}/agent-worktrees/${TASK_SLUG}/score2gp-${ROLE}"
CONTROL_DIR="${WORKSPACE_ROOT}/score2gp-control"
OUT="${CONTROL_DIR}/tasks/${TASK_SLUG}/logs/pytest-${ROLE}-latest.txt"

cd "${WT}"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
mkdir -p "$(dirname "${OUT}")"
python -m pytest 2>&1 | tee "${OUT}"

echo
echo "Saved pytest output to:"
echo "${OUT}"
