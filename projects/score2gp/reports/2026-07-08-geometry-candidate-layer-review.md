# Geometry Candidate Layer Review

Date: 2026-07-08
Reviewer role: Reviewer
Task: Req-110 / Task 33
Product repo: `tticom/score2gp`
Governance repo: `tticom/score2gp-agentops`

## Verdict

`approve architecture`, scoped narrowly.

Epic B now provides a safe, semantic-free geometry diagnostics boundary for future interpretation research. The product code exposes primitive geometry and read-only candidate fields without mapping them into ScoreIR, pitch, duration, voice, or other semantic outputs.

This verdict does not approve semantic implementation work. It approves only proceeding to a research or backlog-refresh step that explicitly accounts for the current gap: the public `geometry_candidates` export path still returns empty `GeometryCandidateSet` objects, even though populated candidate fields exist inside `NotationStaffDiagnostics`.

## Evidence Reviewed

Product baseline:

- `score2gp` main at `a021a9c9 feat(pdf): expose primitive geometry in diagnostics (#345)`.
- Recent merged product PRs reviewed by commit history: #341, #342, #343, #344, and #345.

Governance baseline:

- `score2gp-agentops` main at `c1a29841 docs(governance): authorise Req-110 geometry candidate layer review (#259)`.
- Active task: `projects/score2gp/ACTIVE_TASK.md`, Req-110 / Task 33.
- Backlog references: `projects/score2gp/APPROVED_TASK_QUEUE.md`, Tasks 33-35.

Product files inspected:

- `src/score2gp/pdf_geometry_candidates.py`
- `src/score2gp/pdf_geometry_candidate_extraction.py`
- `src/score2gp/pdf_geometry_candidate_extractor.py`
- `src/score2gp/pdf_staff_geometry.py`
- `src/score2gp/pdf_staff_notation_diagnostics.py`
- `src/score2gp/pdf.py`
- `tests/test_pdf_geometry_candidate_extractor.py`
- `tests/test_candidate_diagnostics_integration.py`
- `tests/test_pdf_geometry_candidate_extraction.py`
- `tests/test_pdf_geometry_candidate_snapshots.py`
- `tests/test_pdf_geometry_candidate_reporting.py`
- `tests/test_pdf_diagnostics_backcompat.py`
- `tests/test_pdf_candidate_semantic_gate.py`
- `fixtures/public/expected_geometry_candidates_*.json`

Validation commands:

- `git diff --check HEAD`
- `.venv/bin/python -m pytest -q tests/test_pdf_geometry_candidate_extractor.py tests/test_candidate_diagnostics_integration.py tests/test_pdf_geometry_candidate_extraction.py tests/test_pdf_geometry_candidate_snapshots.py tests/test_pdf_geometry_candidate_reporting.py tests/test_pdf_diagnostics_backcompat.py tests/test_pdf_candidate_semantic_gate.py`
- `.venv/bin/python scripts/artifact_audit.py`

Validation result:

- Whitespace check: passed.
- Targeted tests: `26 passed in 0.65s`.
- Artifact audit: passed.

## Claim-by-Claim Verification

### Claim 1: The candidate model boundary is semantic-free

Status: verified.

`GeometryCandidateSet`, `PrimitiveEvidenceCandidate`, `LeftMarginPrimitiveCandidate`, and `XAlignedPrimitiveClusterCandidate` expose geometry, source, primitive kind, staff identity, and optional font metadata. The schema guard tests reject terms such as pitch, duration, clef, voice, chord, key signature, time signature, beat, rhythm, ScoreIR, and notehead.

The model names still include "candidate", but the candidate layer itself does not name musical interpretation classes. This supports Epic B as a pre-semantic geometry layer.

### Claim 2: Primitive geometries are now available with exact coordinates

Status: verified with one caveat.

`LocalPrimitivesSummary` now includes `geometries: list[PrimitiveGeometryEvidence] | None`, and diagnostics snapshots were regenerated around this payload. This is the right evidence base for future extraction work because it preserves primitive coordinates instead of only aggregate counts.

Caveat: `LocalPrimitivesSummary.geometries` stores raw internal primitive kind strings in one code path, while clustering and left-margin evidence use mapped candidate-friendly kinds through `_to_evidence()`. This is acceptable for diagnostics, but any future task that consumes `primitives.geometries` directly must normalise kind names intentionally.

### Claim 3: Left-margin and x-aligned candidate fields can be populated from diagnostic evidence

Status: verified.

`PdfGeometryCandidateExtractor` maps `StaffLeftMarginAggregateDiagnostics.evidence` into `left_margin_candidates` and maps `XAlignedPrimitiveClusterEvidence` into `x_aligned_cluster_candidates`, preserving geometry and source fields. `tests/test_candidate_diagnostics_integration.py` verifies populated left-margin and x-aligned candidates from mock page evidence.

This supports the architecture claim that candidate extraction can remain read-only and geometry-preserving.

### Claim 4: The public `geometry_candidates` reporting path is functionally populated

Status: contradicted.

`inspect_pdf()` calls `extract_geometry_candidates(staff_diag)` and serializes the result as page-level `geometry_candidates`. However, `src/score2gp/pdf_geometry_candidate_extraction.py` currently returns `GeometryCandidateSet()` unconditionally. The public snapshot fixtures for `expected_geometry_candidates_*.json` therefore contain empty candidate arrays for all synthetic fixtures.

This means the reporting path proves schema stability and anti-semantic leakage, but not useful candidate extraction. Treating the empty snapshots as extraction correctness would be a false positive.

### Claim 5: Backwards compatibility and artifact safety are preserved

Status: verified.

`tests/test_pdf_diagnostics_backcompat.py` compares current diagnostics output against public expected snapshots. The targeted compatibility tests passed. `scripts/artifact_audit.py` also passed, and this review found no private fixture or generated artifact leakage.

## Unsupported Claims

- The project cannot yet claim that `geometry_candidates` in `inspect_pdf()` is a populated product-facing geometry export.
- The project cannot yet claim readiness for semantic implementation. It is ready only for semantic boundary research or backlog refresh.
- The project cannot yet rely on the empty geometry candidate snapshots to prove extraction quality.

## Plausibility Assessment

The architecture is well supported as a staged boundary:

- raw diagnostics collect primitive geometry;
- typed candidate models preserve geometry and staff identity;
- anti-semantic tests prevent premature meaning in candidate schemas;
- diagnostic candidate fields can be populated from evidence;
- ScoreIR conversion remains untouched.

The next semantic step is plausible only as research. A Developer task that implements semantic interpretation now would be premature unless it first resolves whether to consume the populated diagnostic candidate fields, populate the page-level `GeometryCandidateSet`, or deliberately bypass that export with a documented architecture decision.

## Disconfirmation Gate

False success modes checked:

- Empty snapshots mistaken for extraction correctness: found and explicitly rejected.
- Reporting presence mistaken for reporting content: found and explicitly rejected.
- Candidate diagnostics accidentally becoming semantic objects: not found in candidate schemas.
- Private or generated artifacts accidentally tracked: not found by artifact audit.
- Product code modified during review: not modified.

## Risk of Wasted Work

Medium if the next task jumps straight to semantic implementation.

The main risk is building semantics against the wrong boundary. There are two candidate surfaces today:

- populated candidate fields inside `NotationStaffDiagnostics`;
- empty page-level `GeometryCandidateSet` objects under `inspect_pdf()["pages"][...]["geometry_candidates"]`.

Without choosing and documenting the intended surface, agents may implement research, tests, and product code against different payloads.

## Privacy and Artifact Assessment

Passed. The review used public fixtures and repository tests only. No product code, private fixtures, governance queue files, or active task files were modified.

## Required Fixes

No fixes are required before a research-only next step.

Before any semantic implementation task, one of these must happen:

1. Populate `extract_geometry_candidates()` from `NotationStaffDiagnostics.left_margin_candidates` and `NotationStaffDiagnostics.x_aligned_cluster_candidates`, with non-empty public snapshots where fixtures contain evidence.
2. Or document that future semantic research consumes candidate fields inside `pdf_staff_notation_diagnostics` rather than the page-level `geometry_candidates` export.

## Suggested Next Action

Prefer Req-117 / Task 35 first: refresh the governance backlog after this review so the next autonomous loop has the discovered boundary decision written down.

If the team chooses Req-111 / Task 34 instead, it must remain research-only and must explicitly answer which candidate surface is authoritative before proposing semantic implementation acceptance criteria.
