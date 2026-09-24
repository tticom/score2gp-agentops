# WIN-04 — Post-migration governance hygiene and test decoupling

- **Status**: PROMOTED (the `task` in `ORCHESTRATION_STATE.json`, authority revision 42). Executable by the implementation role.
- **Repository**: `tticom/score2gp-agentops`
- **Branch**: `feat/win-04-post-migration-governance-hygiene`
- **Owner Role**: `implementation`
- **Reviewer Role**: `reviewer`
- **Delivery Action**: `pull_request`
- **Prerequisites**: `WIN-03`

## 1. Authority

- These are non-blocking review findings carried over from WIN-01 (review `5299557145`) and WIN-02 (review `5300426043`), listed in `reports/2026-09-24-win-01-win-02-out-of-policy-merges.md`. The CI failure on #684 adds one more.
- On 2026-09-24 the maintainer ordered WIN-04 before L3-01. Governance promoted it in #687; see `handoffs/2026-09-24-win-04-reorder-promotion.md`.
- **Agent merge authority is out of scope.** On 2026-09-24 the maintainer directed that it become a separate governance task. That task needs a complete inventory of every live human-only merge rule, and agents merge only through the mechanical merge gate. Until it lands, the maintainer `tticom` merges. This task must not change any statement of merge authority.

## 2. Objectives

1. `docs/agy-cycle.md` documents the deleted `scripts/agy-cycle` wrapper. Replace each command with its `python scripts/agy_cycle.py …` equivalent, or delete the document if `agy_cycle.py` is no longer used.
2. `projects/score2gp/prompts/next/go-dispatch.md:23` still names `agy-skills/main` as the skills source. Point it at `agentops-claude-skills`, following `SKILLS_LOCK.md`.
3. `tests/test_governance_audit.py::test_repository_tooling_is_python_only` (line 468) walks the filesystem with `rglob`, so untracked leftovers such as a local `agent-runtime/` directory make it fail. Make it check tracked files (`git ls-files`) instead. Add a negative control: a tracked `.sh` file still fails the test.
4. `tests/test_score2gp_dispatch.py::orca_checkout` (line 219) copies the repository's
   live `ORCHESTRATION_STATE.json` and `ACTIVE_TASK.md` into its fixture. As a result,
   the three `test_orca_path_*` tests fail whenever live authority has no promoted
   implementation task: on 2026-09-24, CI failed on #684 with
   `resolver requires role <none>, not implementation; state=COMPLETE`. Give those
   tests a self-contained fixture authority with a promoted implementation task. Add
   a check that they pass when the live task is `COMPLETED`.

## 3. Allowed Paths and Acceptance

As listed for the `WIN-04` `task` in `ORCHESTRATION_STATE.json` (authoritative).
Historical records (`handoffs/`, `reports/`, `decisions/`,
`docs/cycle-preparation-history/`) are not rewritten.
