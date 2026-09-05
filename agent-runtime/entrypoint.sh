#!/bin/sh
set -eu

product_dir=${SCORE2GP_REPOSITORY_DIR:-/workspace/score2gp}
if [ ! -d "$product_dir/.git" ]; then
  echo "error: runtime requires an isolated task clone with its own .git" >&2
  exit 64
fi

if [ -z "${SCORE2GP_TASK:-}" ]; then
  echo "error: SCORE2GP_TASK is required" >&2
  exit 64
fi

if [ -f /run/secrets/github-token ]; then
  export GH_TOKEN=$(tr -d '\r\n' < /run/secrets/github-token)
  test -n "$GH_TOKEN" || { echo "error: GitHub token secret is empty" >&2; exit 64; }
  export GIT_ASKPASS=/usr/local/bin/github-askpass.sh
  export GIT_TERMINAL_PROMPT=0
fi

export GIT_CONFIG_GLOBAL=/tmp/score2gp-gitconfig
git config --global safe.directory "$product_dir"
git config --global user.name "${GIT_AUTHOR_NAME:?}"
git config --global user.email "${GIT_AUTHOR_EMAIL:?}"
git config --global push.default simple
cd "$product_dir"
test "$(git branch --show-current)" = "${SCORE2GP_TASK_BRANCH:?}" || {
  echo 'error: task branch mismatch' >&2; exit 75;
}
if [ -f /run/secrets/github-token ]; then
  test "$(gh api user --jq .login)" = "$GIT_AUTHOR_NAME" || {
    echo 'error: GitHub role identity mismatch' >&2; exit 77;
  }
fi

# Offline validation is read-only task execution; the host verifies its remote
# checkpoint. Live workers verify from inside as well as from the host.
if [ "${SCORE2GP_SESSION_MODE:-author}" != validation ]; then task-checkpoint; fi
if [ -f "$product_dir/pyproject.toml" ]; then
  python -m pip install --user --no-deps --no-build-isolation --editable "$product_dir" >/dev/null
fi
echo 'Task policy: work on the assigned branch; commit safe explicit paths and run task-checkpoint after each meaningful change and before ending. PRs are a separate readiness step.'
status=0
# Explicit redirection preserves interactive input for an asynchronous child.
exec 3<&0
"$@" <&3 &
child=$!
exec 3<&-
trap 'kill -TERM "$child" 2>/dev/null || true; wait "$child" 2>/dev/null || true; exit 143' TERM
trap 'kill -INT "$child" 2>/dev/null || true; wait "$child" 2>/dev/null || true; exit 130' INT
wait "$child" || status=$?
if [ "${SCORE2GP_SESSION_MODE:-author}" != validation ]; then
  task-checkpoint || exit 75
elif [ -n "$(git status --porcelain=v1 --untracked-files=all)" ]; then
  echo 'error: offline validation left uncommitted files; host recovery required' >&2
  exit 75
fi
exit "$status"
