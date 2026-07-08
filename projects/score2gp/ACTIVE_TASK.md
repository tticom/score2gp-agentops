# Active Task

**Task**: Req-118 / Task 37: Populate page-level geometry candidate export
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## Status
APPROVED

## Executable Task
Yes

## Completion Evidence
Developer must implement the product change in `tticom/score2gp`, commit it, push the branch, and open a PR. The implementation must make the page-level `geometry_candidates` export in `inspect_pdf()` reflect the already-populated diagnostic candidate fields rather than always returning empty `GeometryCandidateSet` objects.

## 1. Baseline
- Req-110 / Task 33 review was merged in governance PR #260.
- The review approved the semantic-free geometry boundary only in a narrow scope.
- The review found that `NotationStaffDiagnostics.left_margin_candidates` and `NotationStaffDiagnostics.x_aligned_cluster_candidates` can be populated from evidence.
- The review also found that `src/score2gp/pdf_geometry_candidate_extraction.py::extract_geometry_candidates()` still returns an empty `GeometryCandidateSet()` unconditionally, causing public geometry candidate snapshots to prove only schema stability, not populated export behavior.

## 2. Goal
Populate `GeometryCandidateSet` from the existing read-only candidate fields on `NotationStaffDiagnostics`:

- copy `left_margin_candidates` into `GeometryCandidateSet.left_margin_primitives`;
- copy `x_aligned_cluster_candidates` into `GeometryCandidateSet.x_aligned_clusters`;
- preserve geometry, source, primitive kind, page/system/staff identity, and optional font metadata;
- keep the layer geometry-only and semantic-free.

## 3. Non-goals
- No pitch, duration, voice, rhythm, clef, key signature, time signature, chord, notehead, rest, or ScoreIR mapping.
- No changes to conversion into playable output.
- No private or copyrighted fixtures.
- No broad OCR/scanned PDF work.
- No new heuristics beyond transferring already-computed diagnostic candidates into the page-level export.

## 4. Product Scope
Allowed likely files:

- `src/score2gp/pdf_geometry_candidate_extraction.py`
- `tests/test_pdf_geometry_candidate_extraction.py`
- `tests/test_pdf_geometry_candidate_snapshots.py`
- `tests/fixtures/pdf/make_geometry_candidate_snapshots.py`
- `fixtures/public/expected_geometry_candidates_*.json`

Allowed if needed for focused validation:

- `tests/test_pdf_geometry_candidate_reporting.py`
- `tests/test_pdf_candidate_semantic_gate.py`

Stop before changing:

- `score2gp-agentops` governance queue files;
- ScoreIR generation;
- whole-note, pitch, duration, or playback logic;
- private fixture paths.

## 5. Branch Suggestion
`feature/populate-geometry-candidate-export-v0.1`

## 6. Required Tests
Run at minimum:

```bash
cd /home/tticom/work/score2gp-workspace/score2gp
git diff --check
.venv/bin/python -m pytest -q tests/test_pdf_geometry_candidate_extraction.py tests/test_pdf_geometry_candidate_snapshots.py tests/test_pdf_geometry_candidate_reporting.py tests/test_pdf_candidate_semantic_gate.py
.venv/bin/python scripts/artifact_audit.py
```

If snapshots change, regenerate them intentionally with the existing helper and include only public expected JSON outputs.

## 7. Acceptance Criteria
- `extract_geometry_candidates()` no longer returns an unconditional empty `GeometryCandidateSet`.
- Tests prove populated diagnostic candidate fields are transferred into the page-level `GeometryCandidateSet`.
- Public fixture snapshots are updated if the fixtures produce candidates.
- Anti-semantic leakage tests remain green.
- Artifact audit passes.
- PR report explicitly states whether public snapshots are now non-empty, and if any remain empty, why.

## 8. Incremental Progress Check
- **What new evidence will this task produce?**: Page-level geometry candidate export contains real geometry candidate data when diagnostics have candidate evidence.
- **Which prior result must it not merely repeat?**: It must not only assert that `geometry_candidates` exists as a list; it must validate content transfer.
- **How will we know the task moved the project forward?**: The public export path becomes a usable geometry-only boundary for the next research task.
- **What is the smallest next decision this task enables?**: Whether Req-111 semantic boundary research should consume the page-level export directly.

## 9. Next Steps
- After product PR merge, run a Reviewer implementation conformance check.
- Then promote Req-111 / Task 34 as research-only semantic boundary proposal if the export is populated and tests are green.
