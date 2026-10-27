# CP-12: Remove the stale promotion rule from the CR-04D refactor-sequence plan and close the oracle gap

- **Repository:** `tticom/score2gp-agentops`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Branch:** `feat/cp-12-remove-stale-promotion-rule`
- **Depends on:** none

## Goal

Remove the stale promotion rule from the CR-04D refactor-sequence plan and close the oracle gap. Source: authority item CP-12. Found 2026-09-26 after PLAN-01 merged (the 'Promotion Rule' section, line 42). tests/test_single_backlog.py did not flag it because the line uses no planning-container word; the fix should also close that oracle gap or record why it is out of scope.

## Acceptance

1. Measure first: quote the 'Promotion Rule' section of projects/score2gp/plans/2026-07-26-cr04d-pdf-tab-measure-assembly-refactor-sequence.md (about line 42) and search projects/score2gp (outside the dated-record exemptions in tests/test_single_backlog.py) for any other live line that says prompts/NEXT.md or a plan selects executable work; list every hit.
2. The stale rule is removed or rewritten to point at ORCHESTRATION_STATE.json as the only task authority; no other content of the plan changes.
3. tests/test_single_backlog.py (or a new tests/test_cp_12_*.py) gains a check that fails on a live line directing work selection to prompts/NEXT.md; shown failing on the base and under a named mutant (reintroduce the line). If closing the gap is out of scope, the handback records why.
4. No gate, role or stop-condition changes; the governance audit passes; validation commands pass; handback complete.

## Rules

- Do not weaken, skip or reorder any merge, review or audit gate.
- Tests must be able to fail: name the wrong implementation each new test rejects and show that mutant failing.
- Never edit CI, private fixtures, agent instruction files or `ORCHESTRATION_STATE.json`.
- Stop and say so if a change outside the allowed paths is needed.
