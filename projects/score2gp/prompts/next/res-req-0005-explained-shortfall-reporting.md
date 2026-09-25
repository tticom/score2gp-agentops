# RES-REQ-0005 — Research to take REQ-0005 to ACCEPTED

- **Kind:** research (backlog item `RES-REQ-0005`; promote to a task before execution)
- **Repository:** `tticom/score2gp-agentops` (records), with read-only inspection of `tticom/score2gp` and the private corpus
- **Requirement:** [REQ-0005](../../requirements/REQ-0005-explained-shortfall-reporting.md), currently `PROPOSED`

## Goal

Answer REQ-0005's open questions with evidence, and turn its draft acceptance criteria into testable ones.

## Deliverables

1. **Current-state map.** Every place the product today refuses, degrades or drops a feature: the stage, the code emitted, and whether the location and reason reach the user. Take it from the code and from real runs on the corpus (Lessons 3-7, Ex 2 Hands Up, Can't Find My Way Home). Name each silent gap.
2. **Reason-code taxonomy.** A proposal that builds on `docs/diagnostics_failure_taxonomy.md`, with a user-facing layer and stable codes.
3. **Best-effort design options.** At least two options for delivering partial output without an unlabelled wrong result (for example a strict/partial mode, per-measure gating, or a separate partial artifact). Evaluate each against the fail-closed rules.
4. **Shortfall record and aggregation design.** Include privacy: counts and codes only in anything committed.
5. **Report mock-up.** What the user sees, from a real run's records.
6. **Status proposal.** Recommend `ACCEPTED`, with the decisions left to the maintainer.

## Constraints

- No product code change.
- No private musical content committed.
