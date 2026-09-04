# Score2GP Docker agent runtime

This runtime launches one disposable, non-root worker against one explicitly
selected Score2GP task worktree. Docker Desktop may use its shared engine, but
the source checkout and credentials remain in the calling WSL distribution.

## Start

From a fresh Ubuntu/WSL instance with Docker Desktop integration enabled:

```bash
curl --fail --silent --show-error --location \
  https://raw.githubusercontent.com/tticom/score2gp-agentops/main/agent-runtime/scripts/bootstrap-instance.sh \
  --output /tmp/score2gp-bootstrap-instance.sh
bash /tmp/score2gp-bootstrap-instance.sh
cd "$HOME/work/score2gp-workspace/score2gp-agentops"
./agent-runtime/scripts/build-runtime-image.sh
./agent-runtime/scripts/verify-runtime.sh
```

The script stores source checkouts and Docker state locally;
the durable inputs remain the GitHub repositories and version declarations in
this directory.

Bootstrap also adds an interactive-shell hook to `~/.bashrc`. It changes to
the AgentOps checkout and starts AGY automatically in Ubuntu-Automation and
Ubuntu-Gov once the runtime image exists. Ubuntu-Codex remains opt-in until
Codex configuration is complete; enable it by creating
`~/.config/score2gp/codex-enabled`.

Each startup hook synchronizes the three clean checkouts from `main` before
launching its runtime. A dirty checkout is left untouched and prevents the
runtime from launching, so in-progress agent work cannot be overwritten.

```bash
SCORE2GP_PRODUCT_DIR=/absolute/path/to/score2gp \
SCORE2GP_TASK=rec-03-vector-text-observations \
  ./start-agent.sh python -m pytest tests/recognition/test_observations.py
```

The first invocation builds the local image and installs the mounted product
editable without resolving additional dependencies. Runtime and validation
dependencies are baked into the image from `requirements.txt`.

To launch a live Linux Antigravity CLI with an isolated config volume:

```bash
SCORE2GP_TASK=rec-03-vector-text-observations \
  ./agent-runtime/scripts/run-agy.sh
```

The launcher creates the product task worktree automatically and mounts the
workspace's `agy-skills` checkout read-only. Set `AGY_SKILLS_DIR` when that
checkout is not at `$HOME/work/score2gp-workspace/agy-skills`.
The writable package-install volume is role-scoped as
`score2gp-automation-agent-local` (or `score2gp-gov-agent-local`).
The default Docker volumes are role-scoped as
`score2gp-automation-agy-config` and `score2gp-automation-agy-state`; use
`SCORE2GP_AGENT_ROLE=gov` for the governance instance. Override
`AGY_CONFIG_VOLUME` or `AGY_STATE_VOLUME` only with equally role-scoped names.

The container process runs as the unprivileged `agent` user. The launcher
passes `SCORE2GP_AGENT_ROLE=automation` or `gov`; this role attestation is the
supported container equivalent of the host Linux identity and is checked by
the dispatch router together with the GitHub login. The task worktree is
mounted at `/workspace/score2gp`, and the source repository's Git
administrative directory is mounted at its original absolute path so the
worktree's `.git` pointer remains valid inside the container.
Before launch, the host launcher requires `setfacl` and grants UID 10001
recursive read/write/execute access plus default ACLs on the task worktree and
Git administrative directory. Docker's `readonly=false` flag alone cannot
override host filesystem permissions.

To enable GitHub access, authenticate `gcloud` in the WSL instance and set
`SCORE2GP_GCP_PROJECT_ID` and `SCORE2GP_GITHUB_SECRET_NAME`. The launcher reads
the latest secret version into a temporary read-only mount, and the container
exposes it to `gh` as `GH_TOKEN` and to Git as an askpass credential. The token
is not stored in the image or a Docker volume. Commits default to the
`tticom-automation` Git author identity; set `SCORE2GP_GIT_NAME` and
`SCORE2GP_GIT_EMAIL` for another role.

```bash
SCORE2GP_GCP_PROJECT_ID=your-project SCORE2GP_GITHUB_SECRET_NAME=score2gp-github-automation-token SCORE2GP_TASK=rec-03-vector-text-observations ./agent-runtime/scripts/run-agy.sh
```

This is intentionally an explicit network-enabled operation. GitHub
credentials are not mounted or installed by the bootstrap scripts.

The image also contains the native Linux Antigravity CLI. Verify it without
the worker entrypoint with:

```bash
docker run --rm --entrypoint agy score2gp-agent:local --version
```

This reports the installed CLI version only. A live Antigravity session needs
an explicit network and authentication design; the default worker service
remains network-disabled.

To create the conventional product virtual environment inside a disposable
Docker volume (without adding `.venv` to the host worktree):

```bash
SCORE2GP_PRODUCT_DIR=/absolute/path/to/score2gp-task-worktree \
SCORE2GP_TASK=rec-03-vector-text-observations \
  ./setup-venv.sh
```

## Codex runtime

The parallel Codex runtime uses `codex.Dockerfile`, a role-scoped Codex home
volume, the same task-worktree and GCP GitHub-token flow, and the same
non-root container boundary. Build it with:

```bash
./agent-runtime/scripts/build-codex-image.sh
```

Launch it with `SCORE2GP_GCP_PROJECT_ID` and
`SCORE2GP_GITHUB_SECRET_NAME` set:

```bash
SCORE2GP_TASK=runtime-codex-smoke ./agent-runtime/scripts/run-codex.sh
```

Codex authentication is separate from GitHub authentication. On first launch,
Codex may require its normal ChatGPT or API-key sign-in; its state is stored in
the role-specific `score2gp-codex-codex-home` volume when launched by the
Codex instance startup hook.

## Isolation policy

- Only the selected product worktree is mounted, and it is task-scoped.
- No WSL home, workspace root, sibling checkout, SSH/GitHub configuration,
  Docker socket, or private-fixture directory is mounted.
- Runtime networking is disabled, the root filesystem is read-only, the
  process runs as UID 10001, all Linux capabilities are dropped, and
  `no-new-privileges` is enabled.
- Normal `/tmp` is `noexec`; test tools use a separate disposable `/test-tmp`
  tmpfs for legitimate executable test doubles.
- The task worktree is writable because editable Python installation can write
  package metadata. Keep it a disposable task worktree, never a shared clone.
- The writable home-local volume is limited to the container's pip user
  installation and is recreated only when its Compose project is removed.
- The product `.venv` is a separate named volume, scoped to the Compose task
  project and never stored in the host checkout.

Networked setup operations such as dependency refreshes or GitHub access are
host-side/controller operations and are intentionally outside this runtime.
