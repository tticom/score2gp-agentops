# Active Task

**Task**: Req-111 / Task 34: Research-only semantic boundary proposal
**Authorised Role**: Architect
**Repository**: `tticom/score2gp`

## Status
APPROVED

## Executable Task
Yes

## Completion Evidence
Architect must produce a product-owned research document in `docs/testing/standard-staff-semantic-boundary.md`, commit it, push the branch, and open a PR. The document must define the smallest safe semantic interpretation boundary after the populated geometry candidate export landed in product PR #346.

## 1. Baseline
- Req-110 / Task 33 review was merged in governance PR #260.
- Req-117 / Task 35 backlog refresh was merged in governance PR #261.
- Req-118 / Task 37 product implementation was merged in product PR #346.
- Page-level `geometry_candidates` now transfers populated `NotationStaffDiagnostics.left_margin_candidates` and `NotationStaffDiagnostics.x_aligned_cluster_candidates` into `GeometryCandidateSet`.
- Public geometry candidate snapshots are non-empty for all four standard-staff fixtures.
- Reviewer conformance found no required implementation fixes after PR #346.

## 2. Goal
Research and document the smallest safe semantic interpretation boundary that can be attempted after geometry candidate export is populated.

The output must answer:

- which semantic unit, if any, is safe to attempt first;
- which existing geometry candidates and diagnostics are valid inputs;
- which fixtures prove readiness;
- which semantics remain explicitly deferred;
- what measurable acceptance criteria would be needed for a later implementation task;
- whether a stop/pivot is recommended instead of implementation.

## 3. Non-goals
- No implementation.
- No new candidate classes.
- No ScoreIR generation.
- No pitch, duration, voice, rhythm, clef, key signature, time signature, chord, notehead, or rest inference.
- No private or copyrighted fixtures.
- No scanned/OCR PDF support.

## 4. Product Scope
Allowed likely file:

- `docs/testing/standard-staff-semantic-boundary.md`

Allowed if needed for references:

- documentation-only edits under `docs/`

Stop before changing:

- product source code;
- tests;
- fixtures;
- generated snapshots;
- governance files.

## 5. Branch Suggestion
`docs/semantic-boundary-research-v0.1`

## 6. Required Validation

```bash
cd /home/tticom/work/score2gp-workspace/score2gp
git diff --check
```

## 7. Acceptance Criteria
- Document is product-owned.
- Document clearly separates fact, inference, hypothesis, and unknown.
- Document identifies the first safe semantic implementation candidate or explicitly says not ready.
- Document defines continue/stop/pivot evidence gates.
- Document names required validation commands for any later Developer implementation.
- Document does not authorize implementation by itself.

## 8. Incremental Progress Check
- **What new evidence will this task produce?**: A bounded product research artifact that turns populated geometry candidates into a measured semantic proposal or a stop decision.
- **Which prior result must it not merely repeat?**: It must not repeat that geometry candidates exist; it must decide whether they are sufficient for a first semantic task.
- **How will we know the task moved the project forward?**: A Reviewer can approve, return, or reject a specific semantic boundary proposal.
- **What is the smallest next decision this task enables?**: Whether to authorise one narrow semantic implementation task, require more geometry coverage, or stop/pivot.

## 9. Next Steps
- After Architect PR opens, run Reviewer architecture verification before any Developer semantic implementation is authorised.
