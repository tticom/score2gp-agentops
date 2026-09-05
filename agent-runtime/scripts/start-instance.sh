#!/usr/bin/env bash
set -euo pipefail

if [ "${SCORE2GP_INSTANCE_STARTUP_DONE:-0}" = 1 ]; then
  exit 0
fi
export SCORE2GP_INSTANCE_STARTUP_DONE=1
if [ -t 0 ] && [ -t 1 ]; then
  export SCORE2GP_INTERACTIVE_AUTH=1
fi

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
gcp_project=${SCORE2GP_GCP_PROJECT_ID:-${PROJECT_ID:-}}
github_secret=${SCORE2GP_GITHUB_SECRET_NAME:-${SECRET_NAME:-}}
# Updating the controller is an explicit host maintenance operation. Starting
# a shell must not reset repositories, switch task branches or touch old worktrees.
cycle_assignment=${SCORE2GP_CYCLE_ASSIGNMENT:-}
generated_assignment=
if [ -z "$cycle_assignment" ]; then
  if [ -z "${SCORE2GP_EGRESS_HOSTS:-}" ]; then
    echo "score2gp: idle; set SCORE2GP_EGRESS_HOSTS before starting an assigned cycle"
    exit 0
  fi
  if [ -z "$gcp_project" ]; then
    echo "error: SCORE2GP_GCP_PROJECT_ID is required for dispatch" >&2
    exit 64
  fi
  github_secret=${github_secret:-score2gp-github-$role-token}
  command -v gcloud >/dev/null 2>&1 || { echo "error: gcloud is required" >&2; exit 69; }
  mkdir -p "$HOME/.config/score2gp"
  dispatch_secret=$(mktemp "$HOME/.config/score2gp/dispatch-secret.XXXXXX")
  chmod 600 "$dispatch_secret"
  trap 'rm -f "$dispatch_secret"' EXIT INT TERM
  if ! gcloud secrets versions access latest --secret="$github_secret" --project="$gcp_project" \
      | tr -d '\r\n' > "$dispatch_secret"; then
    echo "error: gcloud could not read the GitHub secret; run gcloud auth login" >&2
    exit 77
  fi
  test -s "$dispatch_secret" || { echo "error: GitHub secret is empty" >&2; exit 74; }
  export GH_TOKEN=$(<"$dispatch_secret")
  export GIT_TERMINAL_PROMPT=0
  generated_assignment=$(mktemp "$HOME/.config/score2gp/cycle.XXXXXX.json")
  rm -f "$generated_assignment"
  trap 'rm -f "$generated_assignment"' EXIT INT TERM
  python3 "$agentops_dir/agent-runtime/assignment_adapter.py" \
    --role "$role" --agentops "$agentops_dir" --product "$workspace_root/score2gp" \
    --output "$generated_assignment"
  cycle_assignment=$generated_assignment
fi
export SCORE2GP_CYCLE_ASSIGNMENT="$cycle_assignment"
export SCORE2GP_GCP_PROJECT_ID="$gcp_project"
export SCORE2GP_GITHUB_SECRET_NAME="$github_secret"
cd "$agentops_dir"
if [ ! -x "$agentops_dir/agent-runtime/scripts/$launcher" ]; then
  echo "score2gp: $launcher is not installed; run bootstrap-instance.sh" >&2
  exit 69
fi
if ! docker image inspect "$image" >/dev/null 2>&1; then
  echo "score2gp: $image is not built; run its build script" >&2
  exit 69
fi

if [ -n "$generated_assignment" ]; then
  set +e
  SCORE2GP_AGENT_ROLE="$role" "./agent-runtime/scripts/$launcher"
  status=$?
  set -e
  rm -f "$generated_assignment"
  trap - EXIT INT TERM
  exit "$status"
fi
SCORE2GP_AGENT_ROLE="$role" exec "./agent-runtime/scripts/$launcher"
