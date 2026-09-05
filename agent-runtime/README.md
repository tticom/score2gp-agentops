# Disposable Score2GP agent cycles

A cycle is one approved assignment, one independent clone and one bounded
agent invocation. The host controller owns validation and branch publication.
No host source clone, shared Git administrative directory, Docker socket,
home directory or Google credential store is mounted into a worker.

## Lifecycle

1. Require an explicit repository, existing task branch and exact starting SHA.
2. Retrieve the role's GitHub token through host-side Secret Manager and check
   its GitHub login. Clone the remote branch without local object sharing;
   refuse a head that differs from the assignment.
3. Run the agent with the WSL owner's numeric UID/GID. The container still sees
   the account name `agent`. Its root filesystem is read-only; capabilities
   are dropped; privilege escalation is disabled; CPU, memory and process
   counts are bounded.
4. Run the assignment's validation commands in separate offline containers
   with no token, authentication state or skills mount.
5. For an author, reject changed paths outside the assignment, forbidden
   private/generated paths, switched branches, rewritten history, unknown
   ignored outputs, and changes made concurrently on the remote branch. Check
   every new commit, including files added and then removed. Sanitize Git
   configuration before running host Git; worker hooks and filters never run
   on the host. Commit permitted changes and sanitized validation evidence in
   the checkpoint commit message, then push normally to the assigned branch.
6. Read the remote branch back and compare its full SHA. Delete the unique
   source/context clones only when publication is verified and validation
   passed. No force push, merge, branch deletion or remote-main write occurs.

A validation failure can still produce an incomplete-work checkpoint. Its
nonzero exit codes are in the commit message; the controller returns failure
and retains the local clone. An agent failure, interruption, scope violation,
push rejection or failed remote readback retains the clone. It never counts
as completion. The controller removes the temporary token and Docker resources
on ordinary exit, SIGINT and SIGTERM. SIGKILL, host failure or power loss cannot
run cleanup; inspect retained cycle directories before restarting after those
failures, including leftover secret files and containers.

For a reviewer, source and context mounts are read-only. The controller checks
that the assigned PR belongs to another author and matches the repository,
branch and full SHA. It never stages, commits or pushes the source branch.
Disposal requires a published formal review by the assigned login on the same
head, with `<!-- score2gp-cycle:CYCLE_ID -->` in its body, plus passing
validation. A changed PR or absent review receipt retains the clone. Review
validation status remains in the local receipt; the worker's published review
must include its own evidence. This runtime does not replace the project's
exact-head review publisher or its evidence requirements.

## Setup and explicit startup

From the owning Ubuntu/WSL distribution with Docker Desktop integration,
Python 3, Git, `gh`, and authenticated host `gcloud` available:

```bash
./agent-runtime/scripts/bootstrap-instance.sh
./agent-runtime/scripts/build-runtime-image.sh  # AGY
./agent-runtime/scripts/build-codex-image.sh    # Codex, if needed
```

Bootstrap synchronizes only clean controller and skills clones already on
the configured branch, using fast-forward-only updates. It never updates the
legacy product/sandbox clones, resets a branch, or installs ACL tools.
Shell startup does not reset old source worktrees. If no assignment path is
set, it asks the existing role-specific `go` or `got` helper for the current
authorized assignment and converts it to the disposable-cycle envelope. You
do not hand-author JSON. It fails closed on blocked, stale, missing or
unvalidated authority. If `SCORE2GP_EGRESS_HOSTS` is absent it remains idle.
A running WSL distribution does not imply a running Docker worker.

Set only the host configuration needed for automatic dispatch:

```bash
export SCORE2GP_GCP_PROJECT_ID=your-project
export SCORE2GP_GITHUB_SECRET_NAME=score2gp-github-automation-token
export SCORE2GP_EGRESS_HOSTS="api.github.com github.com antigravity.google"
```

Then `wsl -d Ubuntu-Automation` starts one generated assignment. Use the
analogous Gov settings with the Gov token and the provider hosts required by
the reviewer CLI. Use `run-codex.sh` for Codex. Each invocation runs one prompt to completion
(AGY print mode or ephemeral Codex exec), then validates/checkpoints; it does
not leave an interactive session or start another cycle. Optional agent CLI
flags follow the launcher command. Update the assignment's `base_sha` from
fresh remote state before the next cycle. `SCORE2GP_AGENT_ROLE` identifies the
credential principal; `mode` independently specifies author or reviewer.
Gov can therefore author governance work or review product work without being
mistaken for an author solely because it has a token.

The shell hook loads `~/.config/score2gp/runtime.env`. Put the assignment path
and GCP settings there to enable assigned startup. Ubuntu-Codex additionally
requires the existing `~/.config/score2gp/codex-enabled` opt-in file. The new
launcher ignores the obsolete `SCORE2GP_TASK_WORKTREE` and package-volume
settings; it never resumes or disposes of a legacy sandbox implicitly.

## Persistence and recovery

Successful source work and sanitized validation results live in the remote
task branch and checkpoint commit message. The image ID, skills SHA and pinned
context SHAs are recorded; publish and retain the corresponding runtime image
in your image registry if recovery on another machine must reproduce it.
The existing Dockerfiles contain version ranges/dynamic installers, so
rebuilding an image is not a substitute for retaining its digest.

Local receipts/logs and failed clones are under:

```
~/.local/state/score2gp/cycles/<role>-<unique-id>/
```

`receipt.json` records status, assignment and any verified published head;
`repo/` is the retained independent clone. Validation logs stay local and are
not automatically added to Git. Treat them as potentially private. On a
failed push, inspect `git status`, `git log` and the live remote before retrying
a normal push from this clone. On concurrent remote changes, reconcile in the
retained clone with a fresh assignment; never reset it or force push. Recovery
is explicit in this version: starting a fresh cycle does not retry or delete
an earlier failed cycle. Agent authentication is separate from GitHub auth.

Only role-scoped agent auth/config state is persistent, under:

```
~/.local/share/score2gp/<role>/auth/.codex
~/.local/share/score2gp/<role>/auth/.config
~/.local/share/score2gp/<role>/auth/.gemini
```

These are new locations; old Docker volumes are not silently copied or
reowned. Provision the matching CLI's authentication in the new location
before the first unattended cycle. Do not copy credentials between roles.
Each worker home/package area is otherwise tmpfs, so package installations
and session-local files do not survive disposal. Required dependencies belong
in the runtime image. Configure the worker for container/device-code auth;
there are no published callback ports.

Existing UID-10001 legacy work is left intact. To recover its host ownership,
with no legacy worker running, execute this inside each affected distribution
as its normal `tticom` user (one time, not during every startup):

```bash
workspace="$HOME/work/score2gp-workspace"
host_owner="$(id -u):$(id -g)"
sudo find "$workspace/score2gp/.git" "$workspace/score2gp-sandbox-worktree" \
  -xdev -uid 10001 -exec chown -h "$host_owner" {} +
```

Inspect and push permitted legacy work before retiring those old clones.
The new runtime never needs root ownership repairs for its own clones.

## Network and credential boundary

The worker is attached only to a per-cycle internal Docker network. A separate
non-root proxy has external connectivity and shares that internal network.
The worker receives HTTP(S)_PROXY settings; no direct external network, Docker
socket, host networking or published port is provided. The proxy accepts only
HTTPS CONNECT to port 443 on exact `egress_hosts` names. It rejects private,
loopback, link-local and other non-public DNS results and connects to the
validated numeric address, avoiding a second DNS lookup.

List GitHub API/Git endpoints and the agent provider's actual API, login and
artifact endpoints required by your configured workflow. Add endpoints only
after observing the required dependency. There are no wildcard domains or
an unrestricted bridge fallback. A client that ignores HTTPS proxy settings
fails closed. Test provider authentication, streaming and any gRPC/WebSocket
usage in the intended instance before rollout; the infrastructure smoke test
alone does not prove provider compatibility.

The host performs Google token acquisition and Secret Manager access. Workers
receive only the role's GitHub token, not Google credentials or project-wide
Secret Manager authority. Grant the host principal secret-version access to
that one secret; use GitHub tokens limited to the assigned repositories and
needed operations. Enforce protected refs and role permissions on GitHub too:
an HTTPS destination allowlist cannot restrict actions within an allowed
service, and the worker can read its injected token.

Host fetch/push and Secret Manager traffic do not traverse the worker proxy.
The proxy policy therefore constrains worker egress, not all WSL host traffic.

## Verification and offline utility

```bash
python -m pytest -q tests/test_disposable_cycle.py tests/test_cycle_egress.py \
  tests/test_agent_runtime.py tests/test_codex_runtime.py
SCORE2GP_DOCKER_TESTS=1 python -m pytest -q tests/test_cycle_egress.py
```

The Docker test uses an installed `score2gp-codex:local` image (override
`SCORE2GP_TEST_IMAGE`), real host-owned writes and Git objects, allowlisted
GitHub HTTPS, a denied HTTPS destination and a direct-IP bypass attempt. It
never authenticates an agent or reads a real GitHub secret. Controller tests
use real Git remotes for checkpoint/conflict/recovery and stub cloud identity
and Docker orchestration; neither test layer constitutes live agent acceptance.
Worker-entrypoint tests execute `worker.py` with substituted assignment/secret
reads and client subprocess calls, checking prompts, arguments, plugin failures
and exit propagation. They do not authenticate a real agent. Workers use
`GH_TOKEN` for GitHub API access; only the host controller installs a Git
askpass helper for managed publication.

When the default temporary directory is mounted `noexec`, the test suite
automatically creates a unique executable test directory under ignored
`work/test-tmp/`. An explicit `--basetemp` is preserved; choose an executable
mount when supplying it. This keeps real Git hooks and CLI test doubles
executable without weakening the worker's `/tmp` mount policy.

`start-agent.sh` remains an explicit offline utility for a caller-selected
worktree, not a managed/published cycle. It now uses the host UID/GID and
transient home/venv mounts with no persistent package volumes. Run its command
against disposable source. `setup-venv.sh COMMAND...` creates a venv and executes
that command in the same container; the venv disappears on exit.
