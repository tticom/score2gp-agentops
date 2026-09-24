# WIN-04 Reorder Promotion Handoff

## Authority

- Promoted task: `WIN-04` - Post-migration governance hygiene and test decoupling (`PROMOTED`)
- Next proposal: `L3-01` - Paired-staff barline acceptance for the Lesson 3 first system
  (`PROMOTED` -> `PROPOSED`, otherwise unchanged)
- Authority source: `projects/score2gp/ORCHESTRATION_STATE.json` (authority revision 41 -> 42)
- Base: `main` at `c8207b545e6da8371e216f1ef75cbfa1502bd5cd`. That is #686, which promoted L3-01 and
  set `merge_policy.minimum_approvals` to 1, merged at reviewed head
  `194f3ba083956a78eb2a0467541b0a4feda79311`.
- Ordering: on 2026-09-24 the maintainer `tticom` directed that WIN-04 goes before L3-01.
  L3-01 had no branch, PR or work started, so returning it to `PROPOSED` discards nothing.
- Governance publisher: `tticomgov-code` from `worktrees/gov`

## Outcome and scope

- Swapped `task` and `next_task_proposal`: WIN-04 is `PROMOTED` and L3-01 is `PROPOSED`.
- Merge authority is removed from WIN-04. The #685 proposal had WIN-04 restate the live merge
  rules. Reviews `5304697361` and `5304867520` showed that about 18 live documents encode
  human-only or non-LLM merging, including:
  - `.agents/rules/pr_standards.md`
  - `AGENT_CONTROL.md` (`READY_FOR_HUMAN_MERGE`, and `DONE` only after a human merge)
  - `ORCA_WORKFLOW.md` (a dedicated non-LLM merge controller)
  - several skills and templates
  On 2026-09-24 the maintainer therefore directed that agent merge authority become a **separate
  governance task**, with a complete inventory and agents merging only through the mechanical gate.
- WIN-04's scope is frozen at promotion as: `docs/agy-cycle.md`,
  `projects/score2gp/prompts/next/go-dispatch.md`, `tests/test_governance_audit.py` and
  `tests/test_score2gp_dispatch.py`. Its title, objective, acceptance and validation are narrowed
  to match, and it has an explicit acceptance criterion that no statement of merge authority changes.
- Governance aligned WIN-04's live prompt with this promotion and scope.
- `merge_policy` is unchanged here; #686 already set it to 1. `roles.merge_controller` is unchanged (empty).
- Changed paths: `ORCHESTRATION_STATE.json`, `ACTIVE_TASK.md`,
  `prompts/next/win-04-post-migration-governance-hygiene.md`, this handoff.

## Notes carried forward for L3-01

- H1 (require a TAB-staff stroke at the same x) conflicts with
  `tests/test_barline_recovery.py::test_notation_to_tab_barline_inheritance`, whose internal
  barlines cross only the notation staff. Record that as H1's counterexample and take the prompt's
  H2 pivot, unless H1 can be met by a TAB-staff stroke that the TAB filter rejected.
- Local test runs on this Windows host need `python -m pytest --capture=sys`. Under the default fd
  capture, subprocess-based tests fail with `WinError 6`, which is a host artifact.

## Next authorised action

- Action: `tticom-automation` implements WIN-04 on `feat/win-04-post-migration-governance-hygiene`
  in `tticom/score2gp-agentops`. A non-author reviewer then publishes an exact-head APPROVE or
  REQUEST_CHANGES, and the maintainer `tticom` merges.
- Separately, an architect proposes the agent merge-authority governance task. It is not promoted
  by this PR.
- Stop condition: any WIN-04 stop condition; the governance audit failing on `main`.
