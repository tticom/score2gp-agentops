#!/usr/bin/env bash
set -euo pipefail

startup_file=${SCORE2GP_SHELL_STARTUP_FILE:-"$HOME/.bashrc"}
marker="# score2gp-agent-runtime-startup-v2"
launcher_path="${SCORE2GP_AGENTOPS_DIR:-$HOME/work/score2gp-workspace/score2gp-agentops}/agent-runtime/scripts/start-instance.sh"
mkdir -p "$(dirname "$startup_file")"
touch "$startup_file"

if ! grep -Fqx "$marker" "$startup_file"; then
  {
    printf '\n%s\n' "$marker"
    printf 'if [[ $- == *i* ]] && [[ -x %q ]]; then\n' "$launcher_path"
    printf '  %q\n' "$launcher_path"
    printf 'fi\n'
  } >> "$startup_file"
fi
