# Supervisor Stop/Pivot Decision: Mutopia A4 Whole-Note Diagnostic

## 1. Diagnostic Result
- **Repository:** `tticom/score2gp`
- **Branch:** `main`
- **Head SHA:** `b38c0acc9c284379dcd0f82316db08c3fc6211ec`
- **Exact Fixture URL:** `https://www.mutopiaproject.org/ftp/BachJS/BWVAnh120/BWV-120/BWV-120-a4.pdf`
- **Exact Command:** `.venv/bin/python scripts/whole_note_diagnostics_report.py scratch/BWV-120-a4.pdf`
- **Exit Status:** 0
- **Pages Processed:** 1
- **Candidate Count:** 0
- **Artifact Hygiene:** Clean (no tracked files changed, PDF not committed)
- **Known Limitation:** Governance PR #230 merge status could not be independently verified by the diagnostic operator due to `gh` permissions.

## 2. Decision
- The **current vector-path geometric whole-note heuristic is stopped** for this fixture class.
- The diagnostic produced zero candidates, which means **no meaningful candidate evidence**.
- Zero false positives is not considered a success because no candidates were produced in the first place.
- The diagnostic **does not prove text/font, raster, or OMR/CV viability**; it only proves that the current heuristic is unviable for this PDF.

## 3. Authorised Next Task
- **Bounded Architect research only.**
- **Investigation Goal:** Determine whether the approved Mutopia A4 PDF encodes noteheads or whole-note symbols as text/font glyphs, vector paths outside current geometric bounds, raster-like content, or another representation format.
- **Architectural Goal:** Determine whether a bounded whole-note detection architecture is viable for this fixture class.

## 4. Explicitly Blocked
- Developer implementation.
- Product code changes.
- Test changes.
- Fixture additions.
- OMR/CV implementation.
- Broad OMR/CV Architecture Research beyond what is needed to classify representation.
- Private/local artifacts.
- Letter variants.
- Unpinned URLs.
- Treating prior diagnostic evidence as a product capability.

## 5. Required Architect Outcomes
The Architect must conclude their research with exactly one of the following outcomes:
- **Outcome A:** text/font-based detection appears viable for the approved fixture and should proceed to Reviewer architecture verification.
- **Outcome B:** text/font-based detection is not viable, but another bounded non-implementation approach appears viable and should proceed to Reviewer architecture verification.
- **Outcome C:** no viable approach found; no Developer work authorised.

## 6. Required Reviewer Architecture Verification
Once Architect research is completed, a Reviewer must:
- Verify facts vs inferences.
- Verify fixture boundary.
- Verify no product implementation occurred.
- Verify whether the proposed architecture actually follows from inspected PDF evidence.
- Produce a verdict: approve, reject, return to Architect, or stop/pivot.
