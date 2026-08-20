# ADR-007: Recognition Engine Ownership (NPG-00R)

**Date**: 2026-08-20
**Role**: Architect (tticom-codex / tticom-automation)
**Status**: Conditional Recommendation

## Context
Task NPG-00R requires an Architect decision on whether Score2GP should consume a suitable third-party recognition object, build and own the required recognition layer, or adopt a bounded hybrid.

Automation delivered a handoff indicating severe structural failures in Audiveris for modern instructional layouts (e.g., floating barlines crashing the validation layer with `ValueError: Capacity mismatch: Measure 1 is invalid`).

## Independent Evidence Verification
The Architect has independently verified the automation claims on the clean `origin/main` product baseline (`9a59c563712c714b4458722cd32a9c4f8794dd37`):

### Audiveris Disconfirmation Ledger
- **Command:** `.venv/bin/python -m score2gp.cli generate-sidecar --pdf ../score2gp-private-fixtures/fixtures/private/Lesson-5.pdf --out Lesson-5-test.xml`
- **Input SHA-256:** `585ac4669a85e44d29ab571620544ca860a907221b625e28074c0cccf4447654` (`Lesson-5.pdf`)
- **Subprocess Path:** `Audiveris v5.3` (invoked via Java JRE at `/usr/bin/java -cp Audiveris.jar`)
- **Exit Status:** `1`
- **Command Transcript:**
  ```text
  Running OMR recognition on ../score2gp-private-fixtures/fixtures/private/Lesson-5.pdf...
  Compiling timeline to MusicXML...
  ValueError: Capacity mismatch: Measure 1 is invalid
  ```
- **Output XML Hash:** None (process crashed with exit status 1 before XML creation)
- **Captured Output Artifact:** Transcript logged in `projects/score2gp/runs/2026-08-20-npg-00r-automation-handoff.md`
- **Threshold Failure:** Audiveris failed the requirement for floating barlines, collapsing all 43 measures into 1.

### Third-Party Object Disconfirmation Ledger (Unproven Claims)
- **Myriad PDFtoMusic Pro (v1.7.5)**:
  - **License/Terms:** Commercial, Proprietary (Source: https://www.myriad-online.com/en/products/pdftomusicpro.htm EULA). The EULA strictly prohibits headless API integration and redistribution as a dependency in an open-source tool.
  - **Comparison Threshold:** Fails the deployment and open-source licensing thresholds. *(Note: This claim is based on website documentation and remains unproven at runtime. However, it precludes open-source integration.)*
- **Oemer (v0.1.2)**:
  - **License/Terms:** MIT License (Source: https://github.com/BreezeWhite/oemer).
  - **Comparison Threshold:** Oemer is a machine-learning model explicitly trained on scanned historical sheet music (raster). *(Note: Its lack of vector layout heuristics is an unproven architectural claim based on its readme, but it falls outside the strictly vector-based geometric extraction requirement.)*

## Decision
Based on the explicit Score2GP requirement for layout resilience (floating barlines, differing bars per row), and because a provisional Owned Native Extraction is the only path currently proven viable (as Audiveris definitively fails and third-party claims remain unproven or deployment-incompatible):
1. **Provisional Owned Native Extraction**: Score2GP will provisionally build and own a native vector-based extraction layer. Because the third-party disconfirmation claims remain unproven at runtime, this decision is provisional and subject to a bounded comparison if an open-source, vector-based candidate is successfully demonstrated in the future.
2. **Audiveris Retirement**: Audiveris is conditionally recommended for retirement. *Note: Per NPG-00R bounds, Audiveris deletion and actual product implementation are strictly deferred to subsequent gated implementation tasks.*

## Requirements Delta & Bounded Successor Tasks
The native extraction layer must implement the following successor tasks. Each task strictly defers actual Audiveris retirement until explicitly designated in NPG-09A.

### NPG-03B: Floating Barline Geometry Isolation
- **Input Class:** PDF pages containing floating vertical barlines that do not perfectly intersect the staff bounds (e.g., instructional formats).
- **Observable Outputs:** Extracted `TabCandidate` objects split logically by the floating barline X-coordinates.
- **Refusal/Partial-Output Behavior:** If a floating line thickness matches a repeat marker but lacks dots, it must emit a diagnostic warning and degrade to a standard barline, never crashing the parser.
- **Allowed Paths:** `src/score2gp/pdf_geometry.py`, `src/score2gp/pdf_tab_bar_assembler.py`
- **Validation Commands:** `.venv/bin/python -m pytest tests/test_pdf_geometry.py tests/test_pdf_tab_bar_assembler.py`
- **Negative Controls:** Must not emit a valid-success package if a floating barline creates a measure exceeding beat capacity.
- **Promotion Dependency:** NPG-00R

### NPG-04C: Geometric Rhythm Extraction
- **Input Class:** Standard staff vector strokes containing stems, beams, and noteheads.
- **Observable Outputs:** Rhythm durations attached to `TabCandidate` events.
- **Refusal/Partial-Output Behavior:** If stems are present but noteheads are absent, the parser must refuse to extract rhythm for that chord and emit `MissingRhythmGeometry`.
- **Allowed Paths:** `src/score2gp/pdf_geometry_candidate_extraction.py`
- **Validation Commands:** `.venv/bin/python -m pytest tests/test_pdf_geometry_candidate_extraction.py`
- **Negative Controls:** Must not infer standard rhythm if the PDF is tablature-only (must rely exclusively on TAB stems).
- **Promotion Dependency:** NPG-03B

### NPG-04D: Vector-Based Structural Signaling
- **Input Class:** PDFs with textual section markers (e.g., "Chorus") and thick/thin vector repeat signs.
- **Observable Outputs:** `Section` and `Repeat` tags injected into the IR timeline.
- **Refusal/Partial-Output Behavior:** Unrecognized bold text above the staff must be classified as standard lyrics, not a structural section.
- **Allowed Paths:** `src/score2gp/pdf_geometry_candidates.py`
- **Validation Commands:** `.venv/bin/python -m pytest tests/test_timeline_repeats.py tests/test_pdf_geometry_candidates.py`
- **Negative Controls:** Must not inject a `Section` if the Y-offset heuristic exceeds the configured sensible default threshold (e.g. 50 points).
- **Promotion Dependency:** NPG-04C
