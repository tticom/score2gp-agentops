# Docker agent runtime migration handoff

## Authority

- Active task: REC-02 — Recognition Contract Schemas (`PROMOTED`; unrelated to this discussion)
- Authority source: `projects/score2gp/ORCHESTRATION_STATE.json`
- Project profile: `projects/score2gp/AGENT_CONTROL.md`
- Skills revision: workspace `agy-skills` local HEAD `f2ad6fe04090506ab5024de49a884cb00b0aa58a`; the AgentOps skills lock separately requires `439404f7342f4e324147efb6b0276f698fbf2bdb`

## Repository state

- Repository: `score2gp-agentops`
- Base revision: `80d2b5a77c156825f502d402878cf0353fbf435c`
- Branch: `main`
- Local HEAD: `80d2b5a77c156825f502d402878cf0353fbf435c`
- Remote HEAD: `80d2b5a77c156825f502d402878cf0353fbf435c`
- Worktree: clean before this handoff file; this file is the only new local change
- PR: none

## Outcome and scope

- Outcome: Agreed to migrate agent execution from unrestricted WSL sessions to disposable Docker containers managed by Docker Desktop on Windows 11.
- Proposed owner: `score2gp-agentops`, under a new `agent-runtime/` directory, because this is agent infrastructure and governance.
- Product repositories remain owners of their own `pyproject.toml` files, tests, and application runtime dependencies.
- Proposed runtime files: `Dockerfile`, `requirements.txt`, `compose.yaml`, `start-agent.sh`, `entrypoint.sh`, role policies, and a README.
- Frozen or excluded scope: do not mount the whole WSL home, workspace root, sibling repositories, SSH keys, GitHub config, Docker socket, or private fixtures into an agent container.

## Evidence

- Independently verified: workspace startup was run; `agy-logs/workspace-state/latest.tsv` reports the canonical clones clean and updated where applicable.
- Independently verified: `score2gp/pyproject.toml` declares Python `>=3.11`, `pydantic`, `typer`, `pymupdf`, and dev dependencies `pytest`, `pillow`, pinned `ruff`, and pinned `pylint`.
- Independently verified: sibling packages mainly add local dependencies on `score2gp-core` and `score2gp-exporter`; `agy-skills/package.json` uses npm 10.9.4 and has a checked-in `package-lock.json`.
- Independently verified: visible Score2GP code uses PyMuPDF for PDF handling; no required external MuseScore, Ghostscript, Poppler, FFmpeg, or LilyPond executable was found in the inspected sources.
- Independently verified: current workspace `AGENTS.md` is behavioral only; this session environment has unrestricted filesystem and network access.
- Independently verified: Docker Desktop uses a shared engine, while WSL distributions have separate filesystems. WSL integration is configured per distribution.
- Author-reported: Docker Desktop is installed on Windows 11; the current agent environment is accessed through WSL.
- Intentionally unrun: Docker build/run, Docker Desktop configuration, and repository changes beyond this handoff.

## Risks and comments

- The current AgentOps rules contain identity-specific WSL paths such as `/home/tticom-codex`, `/home/tticom-gov`, and `/home/tticom-automation`. Container launchers must use injected paths and identity variables rather than hard-coded host paths.
- Each WSL distribution needs its own copy or Git checkout of Dockerfiles and launcher scripts if it launches containers. Docker images and the Docker Desktop engine are shared, but WSL files are not.
- Do not share one writable worktree between Codex, Gov, and automation identities. Create separate task worktrees and mount only the assigned one.
- Network should default to disabled. GitHub/package access, if required, should use a controlled proxy or a host-side controller with short-lived credentials.
- Product code should initially be mounted at runtime and installed editable with `pip install --no-deps -e /workspace/score2gp`; third-party dependencies belong in the image. `agy-skills` needs Node/npm only for skills-repository maintenance and can be a separate profile.
- Docker Desktop bind mounts can write to host files; every writable mount must be explicit and task-scoped.

## Next authorised action

- Action: After restart, reread this handoff and inspect live AgentOps state. Then, if implementation is requested, propose or implement the smallest AgentOps change that adds `agent-runtime/` with a hardened base image, explicit Python dependency list, Docker Compose policy, and a task-scoped launcher.
- Stop condition: do not alter orchestration behavior, identity policy, active task authority, or product code as part of the initial container-runtime change without a separate explicit task and review gate.

## References

- Docker WSL development: https://docs.docker.com/desktop/features/wsl/use-wsl/
- Docker Desktop settings and WSL integration: https://docs.docker.com/desktop/settings-and-maintenance/settings/
- Docker bind mounts: https://docs.docker.com/engine/storage/bind-mounts/
