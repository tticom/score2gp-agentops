# Score2GP task container runtime

Workers use independent task clones and published task branches. A local
commit or Docker volume is not a durable checkpoint. Follow the
[task checkpoint policy](../projects/score2gp/TASK_CHECKPOINT_POLICY.md).

## Prepare the host

Use `scripts/bootstrap-instance.sh` and the appropriate
`scripts/build-runtime-image.sh` or `scripts/build-codex-image.sh`.
Bootstrap only fast-forwards clean checkouts already on the requested branch;
it refuses dirty, ahead, or differently checked-out repositories.
The host needs Docker, Git, Python 3, gh, gcloud, and setfacl (Ubuntu `acl`).
Authenticate gcloud and set `SCORE2GP_GCP_PROJECT_ID` and
`SCORE2GP_GITHUB_SECRET_NAME` for the role. Secrets are not baked into images
or stored in Docker volumes.

## Start an author session

From the AgentOps repository, with GCP credentials configured:

```bash
SCORE2GP_TASK=assigned-task \
SCORE2GP_TASK_BRANCH=codex/assigned-task \
  ./agent-runtime/scripts/run-codex.sh
```

For AGY use `scripts/run-agy.sh`, with `SCORE2GP_AGENT_ROLE=automation`
(default) or `gov`. GitHub login must match the configured role identity.
Set `SCORE2GP_REPOSITORY_DIR` to select the source repository (default product
clone), `SCORE2GP_BASE_REF` for a new branch's base (default main), and
`AGY_SKILLS_DIR` for the read-only skills checkout. Source repositories are not
mounted into workers. The launcher creates a separate role/task clone, or
resumes `SCORE2GP_TASK_WORKTREE` if explicitly supplied. Old linked worktrees
are rejected; use a fresh destination. Existing dirty work is never reset.

The assigned branch is pushed and read back before launching. During work:

```bash
git add path/to/intended-file
git commit -m 'checkpoint: describe completed work and remaining validation'
task-checkpoint
```

Commit safe explicit paths after each meaningful change and before pausing.
Never commit credentials, private source PDFs, fixtures, or generated private
artifacts. WIP commits are allowed; a PR is a separate readiness step.
Worker and host check branch, origin, cleanliness, and exact remote HEAD at
completion. Failed workers or checkpoints retain the container and clone and
report `RECOVERY_REQUIRED`. Inspect, commit safe changes, publish, and verify
before manually disposing of recovery state. Relaunch refuses dirty or
divergent work; it does not silently repair it.

Use `SCORE2GP_SESSION_MODE=review` for independent review of an already-published
branch. It verifies without publishing. Repository authoring is forbidden,
including fixes discovered during review.

## Offline validation

Compose is network-disabled validation, not an author session. Supply an
already-published independent product clone and branch; the host verifies its
remote checkpoint before and after execution:

```bash
SCORE2GP_PRODUCT_DIR=/absolute/path/to/product-task-clone \
SCORE2GP_TASK=assigned-task \
SCORE2GP_TASK_BRANCH=codex/assigned-task \
  ./agent-runtime/scripts/verify-runtime.sh
```

The same variables apply to `agent-runtime/start-agent.sh <command>` and
`agent-runtime/setup-venv.sh`. Validation must not leave source edits.
The virtual environment uses a task-scoped Compose volume.

## Isolation and recovery limits

Live workers run as UID 10001, with a read-only root filesystem, dropped
capabilities, no-new-privileges, no Docker socket, and no host home, workspace
root, sibling repository, or shared Git administration mounted. Only the task
clone is writable; skills and the short-lived token mount are read-only.
Client state and installation volumes must be role-scoped. Git author and
authenticated GitHub role are checked. Codex authentication is separate from
GitHub and uses its role-scoped Codex home volume.

Live workers use bridge networking to publish checkpoints; offline Compose
has no network. `/tmp` is noexec; test doubles can execute in `/test-tmp`.
Normal launcher exit removes its temporary token file. Failed containers are
retained. Hard host loss can still lose edits since the last verified
checkpoint: frequent explicit checkpoints are mandatory. This lifecycle is
not a per-command Git security sandbox, a private-input backup, or a
replacement for independent review and merge authorization.
