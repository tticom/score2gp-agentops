#!/usr/bin/env bash
set -euo pipefail
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
runtime_dir=$(CDPATH= cd -- "$script_dir/.." && pwd -P)
client=${1:?expected agy or codex}; shift
workspace_root=${SCORE2GP_WORKSPACE_ROOT:-"$HOME/work/score2gp-workspace"}
source_dir=${SCORE2GP_REPOSITORY_DIR:-${SCORE2GP_PRODUCT_DIR:-"$workspace_root/score2gp"}}
skills_dir=${AGY_SKILLS_DIR:-"$workspace_root/agy-skills"}
task_slug=${SCORE2GP_TASK:?set SCORE2GP_TASK to the assigned task}
branch=${SCORE2GP_TASK_BRANCH:?set SCORE2GP_TASK_BRANCH to the assigned branch}
role=${SCORE2GP_AGENT_ROLE:-automation}
mode=${SCORE2GP_SESSION_MODE:-author}
case "$task_slug" in ''|*[!A-Za-z0-9._-]*) echo 'error: invalid task slug' >&2; exit 64;; esac
case "$role" in
  automation) git_name=tticom-automation; git_email=tticomautomation@gmail.com;;
  gov) git_name=tticomgov-code; git_email=tticomgov@gmail.com;;
  codex) git_name=tticom-codex; git_email=tticom-codex@users.noreply.github.com;;
  *) echo 'error: unknown worker role' >&2; exit 64;;
esac
case "$mode" in author|review) ;; *) echo 'error: invalid session mode' >&2; exit 64;; esac
case "$client" in
  agy)
    case "$role" in automation|gov) ;; *) echo 'error: AGY role must be automation or gov' >&2; exit 64;; esac
    image=${SCORE2GP_AGENT_IMAGE:-score2gp-agent:local};;
  codex) image=${SCORE2GP_CODEX_IMAGE:-score2gp-codex:local};;
  *) exit 64;;
esac
for command in git python3 docker gcloud setfacl gh; do
  command -v "$command" >/dev/null || { echo "error: $command is required" >&2; exit 69; }
done
test -d "$skills_dir" || { echo 'error: missing skills checkout' >&2; exit 66; }
repo_name=$(basename "$(git -C "$source_dir" rev-parse --show-toplevel)")
case "$repo_name" in ''|*[!A-Za-z0-9._-]*) echo 'error: invalid repository name' >&2; exit 64;; esac
task_dir=${SCORE2GP_TASK_WORKTREE:-"$workspace_root/$repo_name-$role-$task_slug-task"}
mount_dir=/workspace/$repo_name
gcp_project=${SCORE2GP_GCP_PROJECT_ID:-${PROJECT_ID:-}}
test -n "$gcp_project" || { echo 'error: SCORE2GP_GCP_PROJECT_ID is required' >&2; exit 64; }
secret_name=${SCORE2GP_GITHUB_SECRET_NAME:-${SECRET_NAME:-"score2gp-github-$role-token"}}
secret_file=$(mktemp)
cleanup() { rm -f -- "$secret_file"; }
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
gcloud secrets versions access latest --secret="$secret_name" --project="$gcp_project" | tr -d '\r\n' > "$secret_file"
test -s "$secret_file" || { echo 'error: empty GitHub secret' >&2; exit 74; }
chmod 600 "$secret_file"
setfacl -m u:10001:r "$secret_file"
export GH_TOKEN=$(<"$secret_file")
export GIT_ASKPASS="$runtime_dir/github-askpass.sh" GIT_TERMINAL_PROMPT=0
test "$(gh api user --jq .login)" = "$git_name" || { echo 'error: GitHub role identity mismatch' >&2; exit 77; }
review_args=()
if [ "$mode" = review ]; then review_args=(--review); fi
python3 "$runtime_dir/task_branch.py" prepare --source "$source_dir" --repo "$task_dir" \
  --branch "$branch" --base "${SCORE2GP_BASE_REF:-main}" "${review_args[@]}"
remote=$(git -C "$task_dir" remote get-url origin)
setfacl -R -m u:10001:rwX "$task_dir"
setfacl -R -d -m u:10001:rwX "$task_dir"

local_volume=${AGENT_LOCAL_VOLUME:-"score2gp-$role-agent-local"}
case "$local_volume" in score2gp-"$role"-*) ;; *) echo 'error: local volume must be role-scoped' >&2; exit 64;; esac
mounts=(--mount "type=bind,src=$task_dir,dst=$mount_dir"
  --mount "type=bind,src=$skills_dir,dst=/workspace/agy-skills,readonly"
  --mount "type=bind,src=$secret_file,dst=/run/secrets/github-token,readonly"
  --mount "type=volume,src=$local_volume,dst=/home/agent/.local")
if [ "$client" = agy ]; then
  config_volume=${AGY_CONFIG_VOLUME:-"score2gp-$role-agy-config"}
  state_volume=${AGY_STATE_VOLUME:-"score2gp-$role-agy-state"}
  for volume in "$config_volume" "$state_volume"; do
    case "$volume" in score2gp-"$role"-*) ;; *) echo 'error: AGY volumes must be role-scoped' >&2; exit 64;; esac
  done
  docker volume create "$config_volume" >/dev/null
  docker volume create "$state_volume" >/dev/null
  docker run --rm --network none --user 0:0 --cap-drop ALL --cap-add CHOWN \
    --security-opt no-new-privileges:true --read-only \
    --mount "type=volume,src=$state_volume,dst=/home/agent/.gemini" \
    --entrypoint chown "$image" 10001:10001 /home/agent/.gemini
  for plugin in engineering productivity; do
    test -f "$skills_dir/plugins/$plugin/plugin.json"
    docker run --rm --network none --user 10001:10001 --read-only --cap-drop ALL \
      --security-opt no-new-privileges:true --tmpfs /tmp:rw,noexec,nosuid,size=64m \
      --mount "type=bind,src=$skills_dir,dst=/workspace/agy-skills,readonly" \
      --mount "type=volume,src=$state_volume,dst=/home/agent/.gemini" \
      --entrypoint agy "$image" plugin install "/workspace/agy-skills/plugins/$plugin"
  done
  mounts+=(--mount "type=volume,src=$config_volume,dst=/home/agent/.config"
    --mount "type=volume,src=$state_volume,dst=/home/agent/.gemini")
  worker=(agy --dangerously-skip-permissions "$@")
else
  home_volume=${CODEX_HOME_VOLUME:-"score2gp-$role-codex-home"}
  case "$home_volume" in score2gp-"$role"-*) ;; *) echo 'error: Codex volume must be role-scoped' >&2; exit 64;; esac
  mounts+=(--mount "type=volume,src=$home_volume,dst=/home/agent/.codex")
  worker=(codex --dangerously-bypass-approvals-and-sandbox --add-dir /workspace/agy-skills "$@")
fi

# A failed session is retained. Only verified remote work permits disposal.
container_name="score2gp-$role-$task_slug-$$"
tty_args=()
if [ -t 0 ] && [ -t 1 ]; then tty_args=(-it); fi
status=0
docker run --name "$container_name" "${tty_args[@]}" --init --network bridge \
  --user 10001:10001 --read-only --cap-drop ALL --security-opt no-new-privileges:true \
  --workdir "$mount_dir" --tmpfs /tmp:rw,noexec,nosuid,size=256m \
  --tmpfs /test-tmp:rw,exec,nosuid,size=256m \
  --env TMPDIR=/test-tmp --env 'PYTEST_ADDOPTS=-p no:cacheprovider' \
  --env "SCORE2GP_TASK=$task_slug" --env "SCORE2GP_TASK_BRANCH=$branch" \
  --env "SCORE2GP_AGENT_ROLE=$role" --env "SCORE2GP_SESSION_MODE=$mode" \
  --env "SCORE2GP_REPOSITORY_DIR=$mount_dir" --env "SCORE2GP_TASK_REMOTE=$remote" \
  --env CODEX_HOME=/home/agent/.codex \
  --env "GIT_AUTHOR_NAME=$git_name" --env "GIT_AUTHOR_EMAIL=$git_email" \
  --env "GIT_COMMITTER_NAME=$git_name" --env "GIT_COMMITTER_EMAIL=$git_email" \
  "${mounts[@]}" --entrypoint /usr/local/bin/entrypoint.sh "$image" "${worker[@]}" || status=$?
checkpoint_status=0
python3 "$runtime_dir/task_branch.py" checkpoint --repo "$task_dir" --branch "$branch" \
  --remote "$remote" "${review_args[@]}" || checkpoint_status=$?
if [ "$status" -eq 0 ] && [ "$checkpoint_status" -eq 0 ]; then
  docker rm "$container_name" >/dev/null
else
  echo "RECOVERY_REQUIRED: retained container $container_name and task clone $task_dir" >&2
  echo 'Inspect and commit safe task files, push and verify the branch before disposal.' >&2
  if [ "$checkpoint_status" -ne 0 ]; then exit "$checkpoint_status"; fi
fi
exit "$status"
