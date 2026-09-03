# Score2GP Docker agent runtime

This runtime launches one disposable, non-root worker against one explicitly
selected Score2GP task worktree. Docker Desktop may use its shared engine, but
the source checkout and credentials remain in the calling WSL distribution.

## Start

```bash
SCORE2GP_PRODUCT_DIR=/absolute/path/to/score2gp-task-worktree \
SCORE2GP_TASK=rec-03-vector-text-observations \
  ./start-agent.sh python -m pytest tests/recognition/test_observations.py
```

The first invocation builds the local image and installs the mounted product
editable without resolving additional dependencies. Runtime and validation
dependencies are baked into the image from `requirements.txt`.

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

Networked setup operations such as dependency refreshes or GitHub access are
host-side/controller operations and are intentionally outside this runtime.
