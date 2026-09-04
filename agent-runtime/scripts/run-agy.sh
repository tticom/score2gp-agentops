#!/usr/bin/env bash
set -euo pipefail

workspace_root=${SCORE2GP_WORKSPACE_ROOT:-"$HOME/work/score2gp-workspace"}
source_dir=${SCORE2GP_PRODUCT_DIR:-"$workspace_root/score2gp"}
skills_dir=${AGY_SKILLS_DIR:-"$workspace_root/agy-skills"}
task_slug=${SCORE2GP_TASK:-sandbox}
task_worktree=${SCORE2GP_TASK_WORKTREE:-"$workspace_root/score2gp-$task_slug-worktree"}
agent_role=${SCORE2GP_AGENT_ROLE:-automation}
config_volume=${AGY_CONFIG_VOLUME:-"score2gp-$agent_role-agy-config"}
state_volume=${AGY_STATE_VOLUME:-"score2gp-$agent_role-agy-state"}
local_volume=${AGENT_LOCAL_VOLUME:-"score2gp-$agent_role-agent-local"}
gcp_project=${SCORE2GP_GCP_PROJECT_ID:-${PROJECT_ID:-}}
github_secret=${SCORE2GP_GITHUB_SECRET_NAME:-${SECRET_NAME:-"score2gp-github-$agent_role-token"}}
git_name=${SCORE2GP_GIT_NAME:-tticom-automation}
git_email=${SCORE2GP_GIT_EMAIL:-tticomautomation@gmail.com}
image_tag=${SCORE2GP_AGENT_IMAGE:-score2gp-agent:local}

case "$task_slug" in
  *[!A-Za-z0-9._-]*) echo "error: SCORE2GP_TASK contains unsupported characters" >&2; exit 64 ;;
esac
case "$agent_role" in
  automation|gov) ;;
  *) echo "error: SCORE2GP_AGENT_ROLE must be automation or gov" >&2; exit 64 ;;
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
if [ ! -f "$skills_dir/plugins/engineering/plugin.json" ] || [ ! -f "$skills_dir/plugins/productivity/plugin.json" ]; then
  echo "error: agy-skills checkout not found or incomplete: $skills_dir" >&2
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

docker volume create "$config_volume" >/dev/null
docker volume create "$state_volume" >/dev/null
docker run --rm --user 0:0 \
  --mount "type=volume,src=$state_volume,dst=/home/agent/.gemini" \
  --entrypoint chown \
  "$image_tag" 10001:10001 /home/agent/.gemini
for plugin in engineering productivity; do
docker run --rm \
    --network none \
    --user 10001:10001 \
    --read-only \
    --tmpfs /tmp:rw,noexec,nosuid,size=64m \
    --mount "type=bind,src=$skills_dir,dst=/workspace/agy-skills,readonly" \
    --mount "type=volume,src=$state_volume,dst=/home/agent/.gemini" \
    --entrypoint agy \
    "$image_tag" plugin install "/workspace/agy-skills/plugins/$plugin"
done
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
  --env "GIT_AUTHOR_NAME=$git_name" \
  --env "GIT_AUTHOR_EMAIL=$git_email" \
  --env "GIT_COMMITTER_NAME=$git_name" \
  --env "GIT_COMMITTER_EMAIL=$git_email" \
  --read-only \
  --workdir /workspace/score2gp \
  --tmpfs /tmp:rw,noexec,nosuid,size=256m \
  --mount "type=bind,src=$task_worktree,dst=/workspace/score2gp,readonly=false" \
  --mount "type=bind,src=$skills_dir,dst=/workspace/agy-skills,readonly" \
  --mount "type=bind,src=$secret_file,dst=/run/secrets/github-token,readonly" \
  --mount "type=volume,src=$config_volume,dst=/home/agent/.config" \
  --mount "type=volume,src=$state_volume,dst=/home/agent/.gemini" \
  --mount "type=volume,src=$local_volume,dst=/home/agent/.local" \
  --entrypoint /usr/local/bin/entrypoint.sh \
  "$image_tag" agy --dangerously-skip-permissions "$@"
