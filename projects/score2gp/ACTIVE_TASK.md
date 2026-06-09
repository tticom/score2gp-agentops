## Current Active Task

## Task 42 — Extract left-margin primitive evidence candidates

Status: ACTIVE

Owning repo: score2gp

Branch:
`feature/left-margin-primitive-evidence-candidates-v0.1`

PR title:
`feat(pdf): extract left-margin primitive evidence candidates`

Context:
Product PR #231 (`feat(pdf): add primitive-evidence extractor skeleton`) was merged on 2026-06-09.

Verified baseline for this task:
- PR #231 head SHA: `ed1fb54a5b177c408b953ff7de6fdda4bf4f82b9`
- PR #231 merge commit: `20571ca76f6a3aaeee520294e3322ec506495686`
- `PdfGeometryCandidateExtractor` exists and currently returns empty candidate lists.

Goal:
Implement only left-margin primitive evidence candidate extraction.

`extract_left_margin_candidates()` must map each `PrimitiveGeometryEvidence` item to exactly one `LeftMarginPrimitiveCandidate`, preserving the source geometry and provenance exactly.

Non-goals:
- Do not implement x-aligned cluster candidate extraction.
- Do not modify `extract_x_aligned_cluster_candidates()` except to keep it safely returning `[]`.
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
- One input evidence item produces one candidate.
- Multiple input evidence items preserve input order.
- Preserve exactly: `page_index`, `system_index`, `staff_index`, `x0`, `y0`, `x1`, `y1`, `kind`, `font_name`, and `font_size`.
- Set `source="left_margin"`.
- Let validation errors fail visibly. Do not swallow them.
- `extract_x_aligned_cluster_candidates()` remains `[]`.

Validation:
- `git diff --check`
- `.venv/bin/python -m pytest tests/test_pdf_geometry_candidate_extractor.py`
- `.venv/bin/python -m pytest tests/test_pdf_geometry_candidates.py`
- `.venv/bin/python -m pytest tests/test_pdf_candidate_semantic_gate.py`

Stop conditions:
- Product PR #231 is not present on product `main`.
- Product repo is dirty before work.
- Implementation requires semantic naming or musical interpretation.
- Implementation would require x-aligned cluster extraction.
- Implementation would require diagnostics or reporting integration.
- Any candidate would need synthesized coordinates.
- Validation fails.
