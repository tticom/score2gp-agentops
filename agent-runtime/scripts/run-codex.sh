#!/usr/bin/env bash
set -euo pipefail

workspace_root=${SCORE2GP_WORKSPACE_ROOT:-"$HOME/work/score2gp-workspace"}
source_dir=${SCORE2GP_PRODUCT_DIR:-"$workspace_root/score2gp"}
skills_dir=${AGY_SKILLS_DIR:-"$workspace_root/agy-skills"}
task_slug=${SCORE2GP_TASK:-sandbox}
task_worktree=${SCORE2GP_TASK_WORKTREE:-"$workspace_root/score2gp-$task_slug-worktree"}
agent_role=${SCORE2GP_AGENT_ROLE:-codex}
codex_home_volume=${CODEX_HOME_VOLUME:-"score2gp-$agent_role-codex-home"}
local_volume=${AGENT_LOCAL_VOLUME:-"score2gp-$agent_role-agent-local"}
gcp_project=${SCORE2GP_GCP_PROJECT_ID:-${PROJECT_ID:-}}
github_secret=${SCORE2GP_GITHUB_SECRET_NAME:-${SECRET_NAME:-"score2gp-github-$agent_role-token"}}
case "$agent_role" in
  automation) default_git_name=tticom-automation; default_git_email=tticomautomation@gmail.com ;;
  gov) default_git_name=tticom-gov; default_git_email=tticomgov@gmail.com ;;
  codex) default_git_name=tticom-codex; default_git_email=tticomcodex@gmail.com ;;
  *) default_git_name=; default_git_email= ;;
esac
git_name=${SCORE2GP_GIT_NAME:-$default_git_name}
git_email=${SCORE2GP_GIT_EMAIL:-$default_git_email}
image_tag=${SCORE2GP_CODEX_IMAGE:-score2gp-codex:local}

case "$task_slug" in
  *[!A-Za-z0-9._-]*) echo "error: SCORE2GP_TASK contains unsupported characters" >&2; exit 64 ;;
esac
case "$agent_role" in
  automation|gov|codex) ;;
  *) echo "error: SCORE2GP_AGENT_ROLE must be automation, gov, or codex" >&2; exit 64 ;;
esac
if [ -z "$gcp_project" ]; then
  echo "error: SCORE2GP_GCP_PROJECT_ID is required" >&2
  exit 64
fi
command -v gcloud >/dev/null 2>&1 || { echo "error: gcloud is required" >&2; exit 69; }

if [ ! -f "$source_dir/pyproject.toml" ] || { [ ! -d "$source_dir/.git" ] && [ ! -f "$source_dir/.git" ]; }; then
  echo "error: product Git worktree not found: $source_dir" >&2
  exit 66
fi
if [ ! -d "$skills_dir" ]; then
  echo "error: skills checkout not found: $skills_dir" >&2
  exit 66
fi
if [ "$source_dir" = "$task_worktree" ]; then
  echo "error: SCORE2GP_TASK_WORKTREE must differ from the source worktree" >&2
  exit 64
fi

if [ ! -e "$task_worktree" ]; then
  mkdir -p "$(dirname "$task_worktree")"
  git -C "$source_dir" worktree add --detach "$task_worktree" "${SCORE2GP_BASE_REF:-HEAD}"
elif [ ! -f "$task_worktree/pyproject.toml" ] || { [ ! -d "$task_worktree/.git" ] && [ ! -f "$task_worktree/.git" ]; }; then
  echo "error: task worktree path exists but is not a Score2GP Git worktree: $task_worktree" >&2
  exit 66
fi

secret_file=$(mktemp)
cleanup_secret() {
  rm -f "$secret_file"
}
trap cleanup_secret EXIT INT TERM
gcloud secrets versions access latest --secret="$github_secret" --project="$gcp_project" \
  | tr -d '\r\n' > "$secret_file"
# The container runs as UID 10001; Docker bind mounts preserve host file mode.
# This file is temporary, read-only in the container, and removed on exit.
chmod 644 "$secret_file"
test -s "$secret_file" || { echo "error: GitHub secret is empty" >&2; exit 74; }

exec docker run --rm -it \
  --network bridge \
  --user 10001:10001 \
  --env "SCORE2GP_TASK=$task_slug" \
  --env "SCORE2GP_AGENT_ROLE=$agent_role" \
  --env CODEX_HOME=/home/agent/.codex \
  --env "GIT_AUTHOR_NAME=$git_name" \
  --env "GIT_AUTHOR_EMAIL=$git_email" \
  --env "GIT_COMMITTER_NAME=$git_name" \
  --env "GIT_COMMITTER_EMAIL=$git_email" \
  --read-only \
  --workdir /workspace/score2gp \
  --tmpfs /tmp:rw,noexec,nosuid,size=256m \
  --mount "type=bind,src=$task_worktree,dst=/workspace/score2gp,readonly=false" \
  --mount "type=bind,src=$source_dir/.git,dst=$source_dir/.git,readonly=false" \
  --mount "type=bind,src=$skills_dir,dst=/workspace/agy-skills,readonly" \
  --mount "type=bind,src=$secret_file,dst=/run/secrets/github-token,readonly" \
  --mount "type=volume,src=$codex_home_volume,dst=/home/agent/.codex" \
  --mount "type=volume,src=$local_volume,dst=/home/agent/.local" \
  --entrypoint /usr/local/bin/entrypoint.sh \
  "$image_tag" codex --dangerously-bypass-approvals-and-sandbox --add-dir /workspace/agy-skills "$@"
