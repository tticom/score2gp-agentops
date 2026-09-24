# WIN-04 — Post-migration governance hygiene and merge-rule alignment

- **Status**: PROPOSED (in `queued_task_proposals`). Not executable until governance promotes it.
- **Repository**: `tticom/score2gp-agentops`
- **Branch**: `feat/win-04-post-migration-governance-hygiene`
- **Owner Role**: `implementation`
- **Reviewer Role**: `reviewer`
- **Delivery Action**: `pull_request`
- **Prerequisites**: `WIN-03`

## 1. Authority

- These are non-blocking review findings carried over from WIN-01 (review `5299557145`) and WIN-02 (review `5300426043`), listed in `reports/2026-09-24-win-01-win-02-out-of-policy-merges.md`.
- The maintainer's merge decision of 2026-09-24 is recorded in the same report:
  - `tticom-codex` and `tticomgov-code` may merge. `tticom-automation` may not.
  - Every task PR needs a formal APPROVE at the exact head from a non-author.
  - One approval is enough. The GitHub rulesets on both repositories now require 1.

## 2. Objectives

1. `docs/agy-cycle.md` documents the deleted `scripts/agy-cycle` wrapper. Replace each command with its `python scripts/agy_cycle.py …` equivalent, or delete the document if `agy_cycle.py` is no longer used.
2. `projects/score2gp/prompts/next/go-dispatch.md:23` still names `agy-skills/main` as the skills source. Point it at `agentops-claude-skills`, following `SKILLS_LOCK.md`.
3. The merge rules in `AGENTS.md:86`, `CLAUDE.md:84`, and `projects/score2gp/AGENT_CONTROL.md:186-188` and `:530-532` say `tticom-gov` never merges and `tticom-codex` needs a per-PR instruction. Restate them to match the maintainer decision:
   - Only `tticom-automation` never merges.
   - A merge needs a non-author APPROVE at the exact head.
   - `AGENT-RULES.md:63` ("Must never merge to main") stays, because it describes the automation role.
4. `tests/test_governance_audit.py::test_repository_tooling_is_python_only` (line 468) walks the filesystem with `rglob`, so untracked leftovers such as a local `agent-runtime/` directory make it fail. Make it check tracked files (`git ls-files`) instead. Add a negative control: a tracked `.sh` file still fails the test.

5. `tests/test_score2gp_dispatch.py::orca_checkout` (line 219) copies the repository's
   live `ORCHESTRATION_STATE.json` and `ACTIVE_TASK.md` into its fixture. As a result,
   the three `test_orca_path_*` tests fail whenever live authority has no promoted
   implementation task: on 2026-09-24, CI failed on #684 with
   `resolver requires role <none>, not implementation; state=COMPLETE`. Give those
   tests a self-contained fixture authority with a promoted implementation task. Add
   a check that they pass when the live task is `COMPLETED`.

`merge_policy` and `roles.merge_controller` in `ORCHESTRATION_STATE.json` are
authority, not task scope. Governance aligns them when it promotes this task.

## 3. Allowed Paths and Acceptance

As listed for `WIN-04` in `queued_task_proposals` in
`ORCHESTRATION_STATE.json` (authoritative). Historical records (`handoffs/`,
`reports/`, `decisions/`, `docs/cycle-preparation-history/`) are not rewritten.
