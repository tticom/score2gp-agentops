# Primitive Evidence Candidate Extraction Design Review

Date: 2026-06-09
Reviewer: AI Agent
Verdict: ready for extractor skeleton

## Verification Evidence
- **Product `main` SHA:** `ac9f78f5b71f977cfeaa13e7eebcf7520a1705ee`
- **Task 37 PR:** https://github.com/tticom/score2gp/pull/228 (Merge commit: `98ebce7221ad8186bd116ed6a5e113e3ccab78f7`)
- **Task 38 PR:** https://github.com/tticom/score2gp/pull/229 (Merge commit: `c2c5d0e11c3cf862c54a1268cd0aae2f799fdeac`)
- **Task 39 PR:** https://github.com/tticom/score2gp/pull/230 (Merge commit: `ac9f78f5b71f977cfeaa13e7eebcf7520a1705ee`)

## Code Inspection
- **Exact Files Inspected:**
  - `docs/testing/primitive-evidence-candidate-boundary.md`
  - `src/score2gp/pdf_geometry_candidates.py`
  - `tests/test_pdf_geometry_candidates.py`
  - `tests/test_pdf_candidate_semantic_gate.py`
- **Exact Commands Run:**
  - `pytest tests/test_pdf_candidate_semantic_gate.py`
  - `pytest tests/test_pdf_geometry_candidates.py`
  - `git ls-files | grep -Ei "(private|scratch|tmp|\.pdf$|\.gp$|\.log$|screenshot|output)"`
  - `find . -path "./.git" -prune -o -type f -size +10M -print`
- **Exact Tests Run & Summaries:**
  - `tests/test_pdf_geometry_candidates.py` (10 passed): Validates candidate model initialization, explicit bounds constraints (x0 <= x1, y0 <= y1), valid clusters, mixed-staff/count-mismatched cluster rejection, and missing font metadata enforcement on non-text elements.
  - `tests/test_pdf_candidate_semantic_gate.py` (4 passed): Validates semantic boundaries using word-boundary scans against schemas, public names (`dir()`), source code file content, and docstrings.
- **Schema Status:** All new Pydantic models are marked `frozen=True`. No semantic names exist in public fields.
- **Anti-Semantic Gate Result:** Passed. Zero leakage of terms like "notehead", "pitch", "clef", "duration", "voice", "chord", "key_signature", "time_signature", "beat", "rhythm", or "scoreir".
- **Privacy/Artifact Check Result:** Passed. Ignored files correctly identified; no tracked private files (`.pdf`, `.gp`, or logs) were added or modified. The privacy check commands returned only pre-existing mock PDFs in `tests/fixtures/pdf/` and `work/` directories.

## What Was Not Tested
- Extraction rules are not implemented and therefore not tested.
- Integration into `inspect_pdf` or aggregation into diagnostics is entirely absent.
- ScoreIR output generation is untouched.

## Explicit Stop Conditions for Task 41
- Task 41 MUST BE a **skeleton-only** PR.
- No real left-margin or x-aligned candidate extraction logic may be implemented.
- No extraction rules or heuristic reporting integration.
- No inference of musical semantics.
- Only safe structure instantiation that accepts real PR #227 arrays and emits empty lists.

## Conclusion
The foundation for extraction is completely decoupled from semantic terminology and isolated to pure geometry derived from primitive evidence diagnostics. The repository state meets the rigorous conditions for the extractor skeleton.

## Next Step
- Promote `ACTIVE_TASK.md` to **Task 41 — Add primitive-evidence extractor skeleton**.
