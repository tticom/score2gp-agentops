## Current Active Task

## Task 43 — Extract x-aligned primitive cluster evidence candidates

Status: ACTIVE

Owning repo: score2gp

Branch:
`feature/x-aligned-primitive-evidence-candidates-v0.1`

PR title:
`feat(pdf): extract x-aligned primitive evidence candidates`

Context:
Product PR #232 (`feat(pdf): extract left-margin primitive evidence candidates`) was merged on 2026-06-09.

Verified baseline for this task:
- PR #232 head SHA: `9f8ce275f08446ed53bbe6e0540ed59110561ac3`
- PR #232 merge commit: `fa355584ef46ab83a8a3ec9392b0a2b71b44e57d`
- `extract_left_margin_candidates()` directly maps left-margin primitive evidence to geometry-only candidates.
- `extract_x_aligned_cluster_candidates()` currently remains safely empty.

Goal:
Implement only x-aligned primitive cluster evidence candidate extraction.

`extract_x_aligned_cluster_candidates()` must map each `XAlignedPrimitiveClusterEvidence` item to exactly one `XAlignedPrimitiveClusterCandidate`, preserving source cluster bounds, primitive count, primitive evidence bounds, primitive order, staff identity, and provenance.

Non-goals:
- Do not modify left-margin candidate extraction except for import or formatting fixes required by tests.
- Do not integrate with `inspect_pdf`.
- Do not modify diagnostics output.
- Do not modify fixtures or snapshots.
- Do not add reporting output.
- Do not infer musical semantics.
- Do not filter, group, transform, or synthesize candidate geometry.
- Do not use aggregate counts.
- Do not use private PDFs, GP files, screenshots, logs, private outputs, or local work artifacts.

Required behaviour:
- Empty input returns `[]`.
- One input cluster evidence item produces one `XAlignedPrimitiveClusterCandidate`.
- Multiple input clusters preserve input order.
- Preserve cluster `x0`, `x1`, and `primitive_count` exactly.
- Preserve every source primitive evidence item as a `PrimitiveEvidenceCandidate` with `source="x_aligned_cluster"`.
- Preserve each primitive's `x0`, `y0`, `x1`, `y1`, `kind`, `font_name`, and `font_size` exactly.
- Assign cluster-level `page_index`, `system_index`, and `staff_index` from caller-supplied staff context, because `XAlignedPrimitiveClusterEvidence` and `PrimitiveGeometryEvidence` do not carry staff identity.
- All primitives in a returned cluster candidate must use the same caller-supplied staff identity as the cluster candidate.
- Let validation errors fail visibly. Do not swallow them.
- `extract_left_margin_candidates()` behaviour from Task 42 must remain unchanged.

Validation:
- `git diff --check`
- `.venv/bin/python -m pytest tests/test_pdf_geometry_candidate_extractor.py`
- `.venv/bin/python -m pytest tests/test_pdf_geometry_candidates.py`
- `.venv/bin/python -m pytest tests/test_pdf_candidate_semantic_gate.py`

Stop conditions:
- Product PR #232 is not present on product `main`.
- Product repo is dirty before work.
- Implementation requires semantic naming or musical interpretation.
- Implementation would require diagnostics or reporting integration.
- Any candidate would need synthesized coordinates.
- Implementation would need aggregate counts instead of evidence arrays.
- Validation fails.
