# Req-118 Implementation Conformance Review

Date: 2026-07-08
Reviewer role: Reviewer
Task: Req-118 / Task 37
Product PR: `tticom/score2gp` #346
Product main SHA after merge: `feefbb9d`

## Implementation Conformance Verdict

`approve implementation`

The product implementation satisfies Req-118. It makes the page-level `geometry_candidates` export transfer populated diagnostic candidate fields into `GeometryCandidateSet` without adding semantic interpretation, ScoreIR generation, or new heuristic mapping.

## PR Readiness Status

`READY`

PR #346 was merged after GitHub checks passed and after local validation completed.

## Evidence Reviewed

Product files changed:

- `src/score2gp/pdf_geometry_candidate_extraction.py`
- `tests/test_pdf_geometry_candidate_extraction.py`
- `fixtures/public/expected_geometry_candidates_complex_cluster.json`
- `fixtures/public/expected_geometry_candidates_dense_margin.json`
- `fixtures/public/expected_geometry_candidates_sparse.json`
- `fixtures/public/expected_geometry_candidates_wide_curves.json`

Validation reviewed:

- `git diff --check`: passed
- focused tests: `9 passed in 0.53s`
- artifact audit: passed
- full suite: `886 passed, 1 skipped in 41.89s`
- GitHub checks on PR #346: passed

Snapshot counts after implementation:

- `complex_cluster`: `left_margin=1`, `x_clusters=5`, `cluster_primitives=9`
- `dense_margin`: `left_margin=7`, `x_clusters=4`, `cluster_primitives=8`
- `sparse`: `left_margin=1`, `x_clusters=2`, `cluster_primitives=2`
- `wide_curves`: `left_margin=2`, `x_clusters=4`, `cluster_primitives=4`

## Claim-by-Claim Verification

### Claim 1: `extract_geometry_candidates()` no longer returns unconditional empty output

Status: verified.

The function now returns `GeometryCandidateSet(left_margin_primitives=list(diagnostics.left_margin_candidates or []), x_aligned_clusters=list(diagnostics.x_aligned_cluster_candidates or []))`.

### Claim 2: Tests prove populated transfer

Status: verified.

`tests/test_pdf_geometry_candidate_extraction.py` constructs populated `LeftMarginPrimitiveCandidate` and `XAlignedPrimitiveClusterCandidate` values, calls `extract_geometry_candidates()`, and asserts exact transfer into the serialized `GeometryCandidateSet`.

### Claim 3: Public snapshots are no longer empty when fixtures produce candidates

Status: verified.

All four public geometry candidate snapshots were regenerated and now contain candidate output. The snapshot test passed after regeneration.

### Claim 4: Semantic boundaries remain intact

Status: verified.

The implementation transfers existing geometry candidates only. It does not introduce pitch, duration, voice, rhythm, clef, key signature, time signature, chord, notehead, rest, or ScoreIR mapping. The anti-semantic gate passed.

### Claim 5: Artifact and privacy boundaries remain safe

Status: verified.

`scripts/artifact_audit.py` passed. Only public expected JSON snapshots were changed.

## Tests Prove Wanted Behaviour

Yes. The new unit test proves non-empty transfer. The snapshot tests prove public fixture outputs are now non-empty and stable. The reporting test continues to verify page-level exposure, while the regenerated snapshots now prevent the previous false success mode where the export existed but carried empty data.

## Unsupported Claims

- This does not prove any semantic recognition capability.
- This does not approve pitch, duration, clef, rhythm, voice, or ScoreIR event generation.
- This does not prove scanned/OCR PDF support.

## Risk of Wasted Work

Low for the next research step. The previously ambiguous candidate surface is now materially improved: Architect work can inspect the page-level export rather than choosing between an empty public export and populated internal diagnostic fields.

## Privacy and Artifact Assessment

Passed. No private fixtures or generated private artifacts were added.

## Required Fixes

None.

## Suggested Next Action

Promote Req-111 / Task 34 as an Architect-first, research-only semantic boundary proposal. The next task must still stop before semantic implementation.
