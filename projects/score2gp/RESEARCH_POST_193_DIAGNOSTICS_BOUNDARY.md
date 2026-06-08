# Post-PR #193 Architecture Review: Diagnostics Boundary Strictness

**Date:** 2026-06-08
**Author:** Antigravity-Architect

## 1. Context and Objective
Following the merge of PR #193 (Left-Margin Font/Text Density Diagnostics) and PR #192 (Primitive Clustering), an architecture review was required to evaluate the strictness of the `score2gp` diagnostics boundary. The goal is to determine if the "Semantic Firewall" (geometry-only, no music theory terms) is too narrow, appropriate, or too permissive for the overarching "PDF-Only Tab-to-GP" active plan.

## 2. Findings: The Semantic Firewall is Functioning as Intended
An inspection of `src/score2gp/pdf_staff_geometry.py` and `tests/test_pdf_staff_left_margin_diagnostics.py` confirms that the boundary is exceptionally strict:
- **No Music Theory Leaks:** The schema strictly models primitives (`curve_candidate`, `vertical_stroke_candidate`, `text_span_by_font`) rather than musical concepts (`clef`, `pitch`, `notehead`).
- **Enforced via Tests:** `test_schema_does_not_contain_semantic_names` mathematically guarantees that parsing logic does not hallucinate semantic structures prematurely.

**Conclusion:** The boundary is **not too narrow**. It is correct and essential. By refusing to map primitives to semantic concepts (like classifying a G-clef), we force the rhythm-inference algorithm (Milestone F) to rely purely on spatial positioning (X-aligned clusters) rather than fragile Optical Music Recognition (OMR) techniques.

## 3. Left-Margin Filtering Enables OMR-Free Rhythm Grids
A critical blocker for layout-inferred timing was differentiating between "rhythmic onsets" and "margin metadata" (clefs, key signatures, time signatures). 
PR #193 provides `StaffLeftMarginAggregateDiagnostics`, including `margin_x_threshold_staff_spaces`. 
This is an architectural breakthrough for the project: **We can now isolate rhythmic onsets simply by taking all X-Aligned Clusters (PR #192) that occur to the right of the `margin_x_threshold`**, without ever needing to know *what* the margin primitives are.

## 4. Risks and Open Questions
While the geometry extraction boundary is perfectly strict, the downstream consumption of these diagnostics lacks versioning.
- **Risk:** As we expand to process more diverse PDF fixtures, changes to the diagnostics schema (e.g., adding `diagonal_stroke` or refining clustering algorithms) might break downstream rhythm inference.
- **Mitigation:** We need to establish schema versioning for the geometry diagnostics before we wire them directly into the `build_ir` rhythm inference path.

## 5. Architectural Decision (To be formalized in ADR)
**ADR Recommendation:** Maintain the absolute prohibition on semantic naming within PDF extraction/diagnostics. The path to rhythm inference must remain strictly spatial (X-coordinates and spatial density).

## 6. Next Steps
The immediate next step is to formalize the schema stability and versioning for these new diagnostics, ensuring that future expansions (like import boundary hardening) do not break the strict contracts established in PRs 191-193.
