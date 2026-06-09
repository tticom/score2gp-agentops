## Current Active Task

## Task 45 — Implement read-only candidate diagnostics integration

Status: ACTIVE

Owning repo: score2gp

Branch:
`feature/read-only-candidate-diagnostics-integration-v0.1`

PR title:
`feat(pdf): expose read-only primitive candidate diagnostics`

Context:
Product PRs #231, #232, and #233 are merged. They introduced the primitive evidence candidate extractor boundary and implemented left-margin plus x-aligned primitive cluster candidate extraction on product `main`.

Governance PR #97 is merged. It completed Task 44 and established the read-only candidate diagnostics integration design. The design requires candidate diagnostics to remain supplementary, geometry-preserving, and non-semantic. It also fixes the extraction-state contract: `None` means "not run or evidence unavailable"; `[]` means "run but no candidates found".

Goal:
Implement the smallest product change that exposes primitive evidence candidates as read-only supplementary diagnostics in the existing `inspect_pdf` diagnostics payload.

The implementation must invoke `PdfGeometryCandidateExtractor` from the diagnostics-building path, using existing staff context and real evidence arrays only. It must preserve existing morphology and clustering diagnostics unchanged.

Non-goals:
- Do not infer musical meaning.
- Do not classify notes, chords, stems, clefs, rests, rhythm, pitch, or voices.
- Do not convert candidates to ScoreIR.
- Do not replace primitive diagnostics, morphology diagnostics, or clustering diagnostics.
- Do not synthesize candidate coordinates.
- Do not derive candidates from aggregate counts.
- Do not add scanned/OCR PDF support.
- Do not use private PDFs, GP files, screenshots, logs, generated debug dumps, or local work artifacts.
- Do not make unrelated refactors or documentation churn.
- Do not modify governance files from the product implementation branch unless explicitly instructed by the human maintainer.

Required pre-flight checks:
From the governance repo:
```bash
cd /home/tticom/work/score2gp-workspace/score2gp-agentops
git status --short
git branch --show-current
git fetch --all --prune
gh pr view 97 --json state,merged,mergeCommit,headRefOid,baseRefName
```

From the product repo:
```bash
cd /home/tticom/work/score2gp-workspace/score2gp
git status --short
git branch --show-current
git fetch --all --prune
git switch main
git pull --ff-only
git log --oneline --decorate --graph --max-count=20
gh pr view 231 --json state,merged,mergeCommit,headRefOid,baseRefName
gh pr view 232 --json state,merged,mergeCommit,headRefOid,baseRefName
gh pr view 233 --json state,merged,mergeCommit,headRefOid,baseRefName
```

Required inspection before edits:
```bash
rg "class .*Diagnostics|NotationStaffDiagnostics|PdfStaffNotationGeometryDiagnostics|build_notation_diagnostics|PdfGeometryCandidateExtractor" src tests
rg "evidence" src/score2gp tests
```

Implementation guidance:
- Create the product branch `feature/read-only-candidate-diagnostics-integration-v0.1` from current product `main`.
- Verify the exact diagnostics model before editing. The Task 44 design mentioned `NotationStaffDiagnostics`, but the implementation agent must confirm the actual current product model name and location.
- Add two read-only optional candidate fields to the appropriate staff diagnostics model:
  - `left_margin_candidates: list[LeftMarginPrimitiveCandidate] | None = None`
  - `x_aligned_cluster_candidates: list[XAlignedPrimitiveClusterCandidate] | None = None`
- Import candidate model types only where needed. Avoid broad import churn.
- Instantiate `PdfGeometryCandidateExtractor` inside the existing diagnostics-building path, likely near `build_notation_diagnostics` in `src/score2gp/pdf_staff_notation_diagnostics.py`, after verifying the actual code structure.
- Use the already-computed `page_index`, `system_index`, and `staff_index` values from the current staff context. Do not invent or recalculate staff identity unless current code already does so.
- If `left_margin_diags` exists and its real `evidence` array is available, call `extract_left_margin_candidates(page_index, system_index, staff_index, left_margin_diags.evidence)`.
- If `clustering_diags` exists and its real `evidence` array is available, call `extract_x_aligned_cluster_candidates(page_index, system_index, staff_index, clustering_diags.evidence)`.
- If the relevant diagnostics or evidence array is unavailable, set the corresponding candidate field to `None`.
- If the extractor runs against a real empty evidence array, preserve the resulting empty list `[]`.
- Preserve source geometry, input order, primitive kind, font name, font size, source labels, and staff identity exactly as returned by the extractor.
- Let validation errors fail visibly. Do not swallow candidate validation errors or silently produce empty output.
- Do not modify `extract_left_margin_candidates()` or `extract_x_aligned_cluster_candidates()` unless an interface mismatch is empirically proven and reported first.

Validation:
Run the smallest meaningful targeted tests first, then the wider suite:
```bash
.venv/bin/python -m pytest tests/test_pdf_geometry_candidate_extractor.py
.venv/bin/python -m pytest tests/test_pdf_geometry_candidates.py
.venv/bin/python -m pytest tests/test_pdf_candidate_semantic_gate.py
.venv/bin/python -m pytest tests/test_pdf_staff_geometry_diagnostics.py
.venv/bin/python -m pytest
```

Add or update tests to prove:
- Candidate fields default to `None` when extraction is not run or evidence is unavailable.
- Candidate fields are `[]` when extraction runs against a real empty evidence array.
- Left-margin candidates are populated from real `left_margin_diags.evidence` without geometry changes.
- X-aligned cluster candidates are populated from real `clustering_diags.evidence` without geometry changes.
- Existing morphology and clustering diagnostics are preserved unchanged.
- No semantic terms leak into candidate model names, public interfaces, source strings, or docs.

Empirical smoke requirement:
Use an existing public fixture or public generated fixture already tracked in the product repo to run a realistic diagnostics/`inspect_pdf` smoke check. The report must show whether candidate fields are `None`, `[]`, or populated from real evidence. If no existing public fixture can exercise the evidence arrays needed for this task, stop and report that a prerequisite public fixture/diagnostics task is required. Do not fabricate geometry or create private fixture inputs.

Privacy and artifact checks:
```bash
git status --short
git status --ignored
git ls-files | grep -Ei "(private|scratch|tmp|\.pdf$|\.gp$|\.log$|screenshot|output)" || true
find . -path "./.git" -prune -o -type f -size +10M -print
```

Acceptance criteria:
- A product PR is opened from `feature/read-only-candidate-diagnostics-integration-v0.1` to `main`.
- The PR implements read-only candidate diagnostics only.
- Existing diagnostics remain backward-compatible except for optional supplementary candidate fields.
- `None` and `[]` semantics are implemented exactly as defined above.
- Candidate data is created only from real evidence arrays.
- No semantic inference, grouping, or ScoreIR integration is introduced.
- Targeted tests and the full pytest suite pass, or any unrelated failures are clearly identified with evidence.
- Privacy/artifact checks show no new private or generated artifacts committed.

Stop conditions:
- Product repo is dirty before work starts.
- Governance PR #97 is not present on governance `main`.
- Product PRs #231, #232, or #233 are not present on product `main`.
- The diagnostics evidence arrays required for candidate extraction are unavailable.
- Implementation would require synthesizing candidate bounds or deriving candidates from aggregate counts.
- Implementation would require semantic grouping, musical object recognition, or ScoreIR integration.
- The actual product model differs from the design note and the safe attachment point is unclear.
- Existing public fixtures cannot support an empirical smoke check.
- Private input files, generated PDFs, GP files, screenshots, logs, or diagnostic dumps would need to be committed.
- Required tests fail for reasons that are not understood.
- The branch contains unrelated changes.

Reporting format:
The product implementation agent must report:
- Product branch name.
- Product PR link.
- Exact files changed.
- Commit hash.
- Commands run.
- Targeted test results.
- Full test-suite result.
- Empirical smoke result, including whether fields are `None`, `[]`, or populated.
- Privacy/artifact check results.
- Known limitations.
- Whether the product branch was pushed and whether the PR is ready for review.
