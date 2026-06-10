# Named Treble Clef PDF Diagnostics Mapping Evidence Report

## 1. Status
* `PROPOSED`
* Date: `2026-06-10`

## 2. Purpose
This report maps real diagnostic candidates from a named vector PDF against a visually confirmed treble-clef region. This is strictly an evidence mapping exercise; this is not recogniser implementation.

## 3. Verified baseline
* PR #103 merged.
* PR #104 merged.
* Vector-source material exists under `fixtures/`.
* Treble-clef diagnostic mapping still requires a named PDF smoke.

## 4. Named PDF selection
* **Selected file path:** `fixtures/private/Lesson-3.pdf`
* **Why selected:** Preferred by maintainer; known to have a clear standard-staff opening.
* **Page(s) inspected:** Page 1
* **Treble clef visible:** Yes
* **Key signature visible:** Yes
* **Time signature visible:** Yes
* **Brief visual notes:** The PDF contains standard-staff notation visually confirmed to include opening symbols such as a treble clef at the left margin.

## 5. Visual treble-clef region
* **Page number:** 1
* **Approximate region:** Not available (visual bounds were not extracted by diagnostics)
* **Standard staff or TAB staff:** Standard staff
* **Left-margin/opening-symbol position:** Far-left margin
* **Visual traits:** Ornate G-clef, looped/curled shape, spans multiple staff lines

## 6. Diagnostics entry point discovery
* **Entry point selected:** `scripts/private_diagnostic_smoke.py` (which internally executes `pdf_staff_notation_diagnostics.py` and produces `inspect_pdf.json` containing `pdf_staff_notation_diagnostics`).

## 7. Named PDF diagnostics smoke
* **Exact command:** `python scripts/private_diagnostic_smoke.py --pdf fixtures/private/Lesson-3.pdf --out-dir work/private_diagnostics/Lesson-3`
* **Working directory:** `/home/tticom/work/score2gp-workspace/score2gp`
* **Input file:** `fixtures/private/Lesson-3.pdf`
* **Exit code:** 0
* **Whether diagnostics completed:** Yes
* **Whether output was generated temporarily or printed:** Generated temporarily
* **Where temporary output was written:** `work/private_diagnostics/Lesson-3`
* **Confirmation that temporary output was not committed:** Verified `git status --short` is clean and temporary files remain uncommitted.

## 8. Candidate summary
* **Page index:** 1
* **System index:** None (0 staves detected)
* **Staff index:** None (0 staves detected)
* **`left_margin_candidates`:** `None`
* **`x_aligned_cluster_candidates`:** `None`
* **Candidate count:** 0
* **Candidate kinds:** None
* **Candidate geometry:** None
* **Font metadata:** None
* **Primitive/evidence order:** None

*(Note: The diagnostics command produced `{"staves": [], "system_connectors": [], "status": "success"}`, failing to detect the standard notation staves present on the page.)*

## 9. Candidate-to-visual-region mapping
No candidates were extracted to map. The diagnostics pipeline did not detect the standard notation staves in the PDF, and thus produced no candidate evidence overlapping the visual treble-clef region.

## 10. Sufficiency verdict
**insufficient: diagnostics did not extract candidates in the treble-clef region**

Explanation: While the named PDF was selected and visually confirmed to contain a treble clef, and the diagnostics command ran reproducibly, no extracted candidate evidence exists because the pipeline failed to detect the standard notation staves. Thus, candidate spatial mapping cannot be performed.

## 11. Recommended next task
**Task 51 — Improve candidate extraction to detect notation staves in paired-staff PDFs**

A prerequisite task focusing on candidate extraction improvement is required before mapping can proceed.

## 12. What remains blocked
* Product recogniser implementation remains blocked unless this report explicitly gives a sufficient verdict and governance later authorises implementation.
* ScoreIR emission remains blocked.
* Key signature recognition remains blocked.
* Time signature recognition remains blocked.
* OCR/image recognition remains out of scope.
* Semantic grouping remains blocked until separately designed.
