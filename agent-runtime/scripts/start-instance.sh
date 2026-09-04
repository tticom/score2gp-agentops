#!/usr/bin/env bash
set -euo pipefail

if [ "${SCORE2GP_INSTANCE_STARTUP_DONE:-0}" = 1 ]; then
  exit 0
fi
export SCORE2GP_INSTANCE_STARTUP_DONE=1

workspace_root=${SCORE2GP_WORKSPACE_ROOT:-"$HOME/work/score2gp-workspace"}
config_file=${SCORE2GP_RUNTIME_ENV_FILE:-"$HOME/.config/score2gp/runtime.env"}
if [ -r "$config_file" ]; then
  # shellcheck disable=SC1090
  . "$config_file"
fi

case "${WSL_DISTRO_NAME:-}" in
  Ubuntu-Automation) role=automation; launcher=run-agy.sh; image=score2gp-agent:local ;;
  Ubuntu-Gov) role=gov; launcher=run-agy.sh; image=score2gp-agent:local ;;
  Ubuntu-Codex)
    if [ ! -e "$HOME/.config/score2gp/codex-enabled" ]; then
      exit 0
    fi
    role=codex; launcher=run-codex.sh; image=score2gp-codex:local ;;
  *) exit 0 ;;
esac

agentops_dir="$workspace_root/score2gp-agentops"
if [ "${SCORE2GP_INSTANCE_BOOTSTRAP_DONE:-0}" != 1 ] && [ -x "$agentops_dir/agent-runtime/scripts/bootstrap-instance.sh" ]; then
  export SCORE2GP_INSTANCE_BOOTSTRAP_DONE=1
  AGENTOPS_REF=${AGENTOPS_REF:-main} "$agentops_dir/agent-runtime/scripts/bootstrap-instance.sh"
fi
cd "$agentops_dir"
if [ ! -x "$agentops_dir/agent-runtime/scripts/$launcher" ]; then
  echo "score2gp: $launcher is not installed; run bootstrap-instance.sh" >&2
  exit 0
fi
if ! docker image inspect "$image" >/dev/null 2>&1; then
  echo "score2gp: $image is not built; run its build script" >&2
  exit 0
fi

SCORE2GP_AGENT_ROLE="$role" exec "./agent-runtime/scripts/$launcher"
