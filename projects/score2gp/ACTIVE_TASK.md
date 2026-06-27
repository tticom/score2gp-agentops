# Active Task

**Task**: Reviewer architecture verification of the Architect's proposal to evaluate optical/morphological notehead center extraction as a resolution for `StaffPositionDiagnostics` ambiguity.
**Authorised Role**: Reviewer
**Repository**: `tticom/score2gp-agentops`

## 1. Baseline
- Architect diagnostic evaluation of `StaffPositionDiagnostics` is complete.
- Fixture evidence proved that raw bounding box geometric centers are strictly insufficient to authorise semantic pitch inference (0% `positioned` success rate on basic standard staff fixtures due to stem offset and glyph padding).
- Architect selected **Outcome B**: Useful but insufficient alone.
- Architect proposed a new read-only diagnostic phase to extract optical/morphological notehead centers.

## 2. Active Blocker
The previous blocker (absence of diagnostic evidence for `StaffPositionDiagnostics`) is closed.
The new blocker is that the Architect's proposal for morphology-based notehead center extraction must pass Reviewer architecture verification before any Developer implementation or further Architect diagnostic can proceed.

## 3. Authorised Scope
The Reviewer is authorised to:
- evaluate the Architect's report in `projects/score2gp/decisions/2026-06-27-staff-position-diagnostics-architect-evaluation.md`;
- verify whether morphology extraction aligns with the deterministic geometric pipeline principles;
- authorise the next Architect or Developer task if the proposal is sound;
- reject or amend the proposal if it risks unbounded CV/ML approaches.

The Reviewer must not:
- implement product code;
- implement semantic pitch, clef, rhythm, or whole-note recognition;
- change ScoreIR semantics;
- change GP export.

## 4. Required Outcomes
The next task must force one of these outcomes:
- **Outcome A**: The morphology extraction proposal is verified and the next Architect/Developer task is authorised.
- **Outcome B**: The proposal needs revision to meet architectural constraints.
- **Outcome C**: The proposal is rejected, forcing a pivot to a different approach.
