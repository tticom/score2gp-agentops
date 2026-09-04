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
