# Decision Record — Product PR #338 Completion and Single-Prompt Cycle Architecture Authorisation

- **Status**: COMPLETED & AUTHORISED
- **Product PR**: [PR #338](https://github.com/tticom/score2gp/pull/338)
- **Product Merge**:
  - Merge commit: `ff241fbc0c714eb62acc14f5171f61cefa9c30ea`
  - Merged timestamp: `2026-07-07T14:22:43Z`
- **Baselines**:
  - Product PR #338: merged at `ff241fbc0c714eb62acc14f5171f61cefa9c30ea`
  - Governance PR #247: merged at `c3b129a9514dd0e137d627f4a89fd1e81d081cf8`

## 1. Implemented Capability (Product PR #338)
- Bounded multi-staff bridge timing in `src/score2gp/notation_bridge.py`.
- Map each unique `staff_index` in outcomes to a separate `Track` in `ScoreIR`.
- Track `current_onset_ticks` independently for each staff/track, allowing parallel progression of time.
- Preserve same-onset chord grouping from PR #337.
- Coordinate-less/context-less candidates retain single-staff sequential behaviour.

## 2. Files Changed in Product PR #338
- `src/score2gp/notation_bridge.py`
- `tests/test_notation_bridge.py`

## 3. Product PR Validation & Conformance
- PR URL: https://github.com/tticom/score2gp/pull/338
- Checked mergeability and merge status (Merged, mergeable state clean).
- CI checks: All checks green.
- Conformance reviewed and approved by tticom.
- All 876 pytest tests passed at the time of PR #338 merge (current post-automation main suite has 880 tests, all passing).
- Artifact hygiene: verified clean (no private PDFs, `.gp` files, logs, or scratch dumps committed to git).
- Known limitations preserved: no true polyphony, no same-staff multi-voice support, no voice separation, no OMR extraction changes, no staff geometry changes, no GP writer changes, no real-world score support claim.

## 4. Supervisor Priority Override
- Task 14 — Add diagnostics snapshot regeneration helper remains in the approved queue (`APPROVED` status).
- The Supervisor has changed immediate execution priority to workflow turnaround speed and automation safety.
- Therefore, Task 14 is NOT promoted to active at this time.

## 5. New Active Task Authorisation
- **Role Authorised**: Architect only
- **Active Task**: `single-prompt autonomous cycle v0.1 architecture`
- **Developer Authorised**: No
- **Product Work Authorised**: No
- **Reviewer Authorised**: Reviewer only (only for later architecture report verification)

## 6. Architecture Task Requirements
The Architect must produce a design for a single-human-prompt workflow that:
- Runs bootstrap first as a mandatory startup summary;
- Classifies task type as Tier A or Tier B;
- Sequences Architect, Reviewer, Developer, Reviewer, PR readiness, merge, and governance recording as appropriate;
- Preserves role boundaries;
- Prevents self-approval (Reviewer must remain independent);
- Stops on failed evidence (fails closed);
- Carries evidence between stages automatically without human copy-pasting;
- Handles both product and governance repositories;
- Handles PR creation, review, merge, expected-head protection, and post-merge recording;
- Defines when Supervisor approval is required;
- Defines when automatic continuation is allowed;
- Defines exact stop/pivot triggers;
- Proposes the smallest safe implementation path.

## 7. Required Architect Outcomes
Architect must choose exactly one:
- **Outcome A**: Single-prompt cycle is viable for Tier B only, with Tier A pauses.
- **Outcome B**: Single-prompt cycle is viable for both Tier A and Tier B with explicit stop gates.
- **Outcome C**: Full single-prompt cycle is not safe; propose a smaller assistant/orchestrator improvement.

## 8. Measurable Acceptance Criteria
The Architect's output must be an architecture proposal (`projects/score2gp/research/2026-07-08-single-prompt-autonomous-cycle-architecture.md`) that:
- Separates fact, inference, hypothesis, and unknown;
- Identifies files, policies, and scripts likely to change;
- Defines the safety and verification model;
- Proposes a concrete workflow contract and evidence handoff;
- Defines exact stop/pivot triggers;
- Recommends or rejects implementation;
- Authorises no Developer work or product changes.

## 9. Next Steps
- Required next review: PR readiness review for this governance PR.
- After merge, the Architect research task begins.
