# CP-15: Merge gate: a COMMENTED review must not displace the same reviewer's earlier APPROVE at the head

- **Repository:** `tticom/score2gp-agentops`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Branch:** `feat/cp-15-commented-review-keeps-earlier-approve`
- **Depends on:** none

## Goal

This task is gate-adjacent. It may only make the gate read the evidence it already reads more correctly; no review, merge or audit check may be removed, loosened or reordered, and anything that was denied for a real reason stays denied. Seen 2026-09-27 on tticom/score2gp#466: current_head_review keeps only each author's latest review state at the head, so the reviewer's thread reply (a COMMENTED review after its APPROVE) replaced the APPROVE; with no APPROVED or CHANGES_REQUESTED verdict left it returned NONE, and verify_merge_gate denied (current_head_not_approved and dependants) until the reviewer republished APPROVE. Fix: skip COMMENTED reviews when taking each author's latest verdict, keeping a later CHANGES_REQUESTED or DISMISSED decisive; test all three.

## Acceptance

1. Measure first: reproduce on the base that a reviewer's APPROVE followed by a COMMENTED review at the same head makes current_head_review return NONE and verify_merge_gate deny; quote the function and the denial codes.
2. Change only how each reviewer's latest verdict is chosen: COMMENTED reviews are skipped, while a later CHANGES_REQUESTED or DISMISSED from that reviewer stays decisive. An APPROVE at an older head, an APPROVE from the author, and a head with no APPROVE at all are denied exactly as before.
3. Tests cover APPROVE then COMMENTED (allowed), APPROVE then CHANGES_REQUESTED (denied), APPROVE then DISMISSED (denied), COMMENTED only (denied), and APPROVE at a stale head then COMMENTED (denied); each is shown failing on the base where behaviour changes, and the named mutants (treat COMMENTED as APPROVE, drop the head check, let CHANGES_REQUESTED be skipped) are rejected.
4. List every other caller of the verdict selection and show it is unchanged or equally correct. No gate, role or stop-condition changes.
5. Validation commands pass; handback complete.

## Rules

- Do not weaken, skip or reorder any merge, review or audit gate. The only permitted behaviour change is the one in the acceptance: how a reviewer's latest verdict is chosen (COMMENTED skipped; CHANGES_REQUESTED and DISMISSED stay decisive). Everything else a gate accepts or denies is unchanged.
- Tests must be able to fail: for each new test, name the wrong implementation it rejects and show that mutant failing.
- Never edit CI, private fixtures, agent instruction files or `ORCHESTRATION_STATE.json`.
- Stop and say so if the task needs any gate change beyond the one the acceptance names.
