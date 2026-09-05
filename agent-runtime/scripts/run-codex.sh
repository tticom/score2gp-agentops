#!/usr/bin/env bash
set -euo pipefail
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
export SCORE2GP_AGENT_ROLE=${SCORE2GP_AGENT_ROLE:-codex}
exec bash "$script_dir/run-worker.sh" codex "$@"
