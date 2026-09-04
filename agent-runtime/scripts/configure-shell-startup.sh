#!/usr/bin/env bash
set -euo pipefail

startup_file=${SCORE2GP_SHELL_STARTUP_FILE:-"$HOME/.bashrc"}
marker="# score2gp-agent-runtime-startup"
mkdir -p "$(dirname "$startup_file")"
touch "$startup_file"

if ! grep -Fqx "$marker" "$startup_file"; then
  {
    printf '\n%s\n' "$marker"
    printf 'if [[ $- == *i* ]] && [[ -x %q ]]; then\n' "$startup_file"
    printf '  %q\n' "${SCORE2GP_AGENTOPS_DIR:-$HOME/work/score2gp-workspace/score2gp-agentops}/agent-runtime/scripts/start-instance.sh"
    printf 'fi\n'
  } >> "$startup_file"
fi
