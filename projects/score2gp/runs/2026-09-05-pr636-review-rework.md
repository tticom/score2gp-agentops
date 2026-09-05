# PR #636 review rework

## Authority and repository state

- Authority: maintainer's request to address changes requested on PR #636;
  author rework only, not a reviewer or integration operation.
- Repository: `tticom/score2gp-agentops`; PR:
  https://github.com/tticom/score2gp-agentops/pull/636 (open draft).
- Branch: `feat/disposable-agent-cycles`.
- Base: `1d428ee782a6465e8ff5eb916979848d470d1972`.
- Reviewed predecessor: `16e4e9ffea52c58b3d6c99ca4657dea86ab9b955`.
- Implementation local and verified remote checkpoint:
  `b6ecc6d4c7f6b18b11f78d40847c6e4497352d1d`, clean after publication.
  This handoff is a subsequent documentation-only commit; its containing
  commit identifies the handoff revision.
- Project profile: `projects/score2gp/WORKFLOW_SKILLS_PROFILE.md`.
- Installed identity/workflow/handoff skills pin:
  `439404f7342f4e324147efb6b0276f698fbf2bdb`; no skills were relinked.
- Startup identified separate product REC-04 / PR #459 as needing review.
  That assignment was not executed or changed; this run is scoped to #636.

## Outcome and review disposition

Consumed formal review **5120223205**, `tticomgov-code`, CHANGES_REQUESTED,
submitted `2026-09-05T06:52:31Z` on the reviewed predecessor above.

- Removed the unused worker askpass mount/export; kept host publication and
  GitHub API token access. Controller and worker tests assert its absence.
- Assigned startup now returns 69 for a missing launcher or image; new tests
  verify failure status and that the launcher was not run. Idle behavior stays.
- Added direct `worker.py` execution tests for both engines, both roles,
  argument/prompt construction, plugin-install failure and exit propagation.
  These execute the Python entrypoint and stub client subprocesses, not agents.
- Added executable temporary-directory selection when default temp is noexec;
  preserved explicit caller basetemp. Verified under a real Docker noexec mount.
- Matched every negative assignment case to its expected rejection and
  distinguished scope/concurrency errors in checkpoint tests.
- Named proxy limits/timeouts and renamed worker arguments to `worker_argv`.
- All four inline threads remain unresolved for the independent reviewer;
  the author does not dismiss the predecessor verdict or self-approve.

## Evidence and limits

- Full suite with `SCORE2GP_DOCKER_TESTS=1` and
  `SCORE2GP_TEST_IMAGE=score2gp-codex:disposable-cycles`: **222 passed**.
- Runtime modules inside the Codex image, network disabled, non-root,
  read-only root and `/tmp` mounted noexec: **57 passed, 2 skipped**.
  The skips are explicit nested-Docker tests, exercised separately on the host.
- Real Docker boundary module against `score2gp-agent:disposable-cycles`:
  **13 passed**. Both runs mount this checkout's updated proxy/controller code.
- Ruff on changed Python files, shell syntax and Git whitespace checks passed.
- Initial noexec probe failed because its working directory was a host linked
  worktree whose `.git` target was not mounted. Repeating from neutral `/tmp`
  passed; shared host Git metadata was never mounted to bypass that boundary.
- Generic `agent_verify.py` and `artifact_audit.py` are absent in AgentOps;
  no successful execution of those tools is claimed. Changed paths contain
  source, tests and documentation, not private inputs or raw logs.
- Author-executed evidence only. Live provider authentication/streaming,
  production rollout, image publication and independent re-review are unrun.

## Scope and next gate

Changed runtime files and related tests only, plus this durable run record.
Product source, task authority, Lesson 3 plan, production settings, credentials
and existing image tags are unchanged. Next action: independent exact-head
re-review of #636, then the separately bounded live-provider staging gate.
No deployment or merge is authorized by this handoff.
