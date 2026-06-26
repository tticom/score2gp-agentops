# Active Task

**Task**: Supervisor Decision Gate: Select next post-MeasureBucketDiagnostics task
**Authorised Role**: Supervisor
**Repository**: `tticom/score2gp-agentops`

## 1. Completed baseline
- Product PR #329 merged.
- Product PR #329 merge commit: 8af3518633f02cd9bcaf0e1413238eb093513f5e.
- Reviewed head SHA: 3deb24dd825190989a1aea9f4ecd95f1532aa2f7.
- Capability merged: read-only MeasureBucketDiagnostics.
- Governance PR #221 authorised the Developer implementation.
- Product PR #328 remains the candidate-to-measure assignment baseline.

## 2. Merged capability
The product now has read-only diagnostics that:
- consume candidate-to-measure assignment diagnostics;
- group only assigned candidates;
- group by page/system/staff/measure;
- emit ordered, empty, center_x_ambiguous, and upstream failure behaviour;
- preserve diagnostic-only scope.

## 3. Known limitations
- no rhythm inference;
- no duration inference;
- no playback order inference;
- no musical sequence inference;
- no ScoreIR/GP output changes;
- no semantic note/rest recognition;
- no whole-note recognition;
- no OCR/MusicXML/ML/training;
- double-barline fixture test remains absent because the specific public fixture is not available.

## 4. Active decision needed
The supervisor must decide the next smallest valid task. Candidate options (not authorisations):
1. Architect task: define the next post-measure-bucket diagnostic step.
2. Diagnostic task: prove what new decision-useful evidence `MeasureBucketDiagnostics` can produce on public fixtures.
3. Governance task: update project roadmap/blocker state before further product work.
4. Stop/pivot task: if measure-bucket diagnostics do not materially reduce the current blocker.

## 5. Explicit block
No Developer implementation is authorised until the supervisor chooses the next task and the requirement contract is written.
