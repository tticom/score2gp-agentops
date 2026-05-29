#!/usr/bin/env bash
set -euo pipefail

TASK_SLUG="${1:-pdf-to-gp-smoke-v1}"
WORKSPACE_ROOT="${2:-/home/tticom/work/score2gp-workspace}"
CONTROL_DIR="${WORKSPACE_ROOT}/score2gp-control"
AGENT_ROOT="${WORKSPACE_ROOT}/agent-worktrees/${TASK_SLUG}"

echo "Controller:"
echo "  ${CONTROL_DIR}"
echo

echo "Task files:"
ls -la "${CONTROL_DIR}/tasks/${TASK_SLUG}"
echo

for role in architect tpo developer reviewer; do
  WT="${AGENT_ROOT}/score2gp-${role}"
  echo "=== ${role}: ${WT} ==="
  if [[ -d "${WT}" ]]; then
    (
      cd "${WT}"
      echo -n "branch: "
      git branch --show-current
      echo "status:"
      git status --short
      if [[ -d .venv ]]; then
        echo "venv: present"
      else
        echo "venv: missing"
      fi
    )
  else
    echo "missing"
  fi
  echo
done
