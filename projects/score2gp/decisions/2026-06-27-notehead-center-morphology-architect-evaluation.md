# 2026-06-27 Architect Evaluation: Notehead Center Morphology Viability

## Baseline Context

- **Product PR**: #330 (Merge Commit `dc511e6f663c08c180e1beae473c5b0d31f31bc4`)
- **Governance PR**: #224 (Merge Commit `b78c9c306d41ee5b045ae7bb308807be5555a787`)
- **Governance PR**: #225 (Merge Commit `c46dba9a53d95b4b2ebc6cc950ed1932cc24e4eb`)
- **Previous Outcome**: Raw bounding-box geometry is useful but insufficient alone due to stem offset (quarter/half notes) and alignment offsets (whole notes), leading to ambiguous statuses.

## Fixture Set Evaluated

The evaluation was performed against committed safe public fixtures:

- `tests/fixtures/pdf/generated_standard_staff_quarter_note.pdf`: evaluated
- `tests/fixtures/pdf/generated_standard_staff_half_note.pdf`: evaluated
- `tests/fixtures/pdf/generated_standard_staff_whole_note.pdf`: evaluated
- `tests/fixtures/pdf/generated_standard_staff_ledger_lines.pdf`: evaluated
- `tests/fixtures/pdf/generated_standard_staff_multi_staff.pdf`: evaluated

## Diagnostic Method

- **Method**: Horizontal projection density profile.
- **Process**: Rendered the PDF page raster (using `fitz.Pixmap` at 4.0x scale) specifically clipped to the candidate's bounding box. For each row in the crop, counted the dark pixels (`< 128` intensity). 
- **Center Extraction**: Identified the peak density (thickest horizontal cross-section, representing the notehead mass). Calculated the local Y-center of all rows with density $\ge 0.8 \times$ peak density, and mapped it back to staff grid step index.

## Metrics Summary

- **Total fixtures evaluated**: 5
- **Total candidate records**: 8
- **Ambiguous before morphology**: 6
- **Resolved after morphology**: 4 (2 half notes, 2 whole notes)
- **Still ambiguous after morphology**: 2 (2 quarter notes)
- **Morphology extraction failures**: 0
- **Mean residual before morphology**: 0.338 steps
- **Mean residual after morphology**: 0.140 steps
- **Candidate types improved**: half_note, whole_note
- **Candidate types not improved**: quarter_note (in this specific synthetic fixture)
- **False-confidence risks observed**: None. The method correctly preserved ambiguity for the quarter notes, which were discovered to be drawn as synthetic solid blocks precisely halfway off-grid.

## Analysis

### Facts
- The morphology method resolved 100% of the half notes and whole notes, snapping their residuals down from >0.4 (and >0.3) to 0.029, a near-perfect on-grid fit.
- The 2 quarter notes remained ambiguous (residual 0.471) because their candidate bounding boxes in the synthetic fixture are small 15x10 solid rectangles centered precisely at an off-grid Y coordinate (cy=215.0).
- The overall resolution rate of previously ambiguous candidates was 66.6% (4 out of 6).

### Inferences
- Horizontal density projection is a highly effective, purely deterministic diagnostic for recovering true optical notehead centers from bounding boxes containing stems (half notes) or padding offsets (whole notes).
- The remaining 33.3% ambiguity is an artifact of the synthetic quarter-note fixture intentionally presenting off-grid, stem-less blocks to test diagnostic safety constraints. Morphology safely preserved this ambiguity without forcing a false-positive on-grid snap.

### Hypotheses
- If tested on a natural (non-synthetic) musical score, this morphology method will exceed the 70% resolution threshold for quarter notes, as natural quarter notes have stems and distinct notehead ovals.

### Unknowns
- Whether this simple horizontal projection method will be confused by complex chords, closely-spaced beaming, or dense polyphony without further vertical/connected-component isolation.

## Architect Outcome

**Outcome B — Useful but insufficient alone**

## Outcome Justification

The morphology method provided highly useful and successful evidence, effectively solving the stem-offset and padding problems for half and whole notes. However, because the resolution rate was exactly 66.6% (missing the 70% Outcome A threshold due to the synthetic off-grid quarter-note fixture anomalies), direct product implementation cannot yet be authorised. Another bounded research step is required to confirm if natural quarter notes resolve successfully.

## Next Recommended Task

**Task**: Architect fixture-safety-gated diagnostic task: evaluate the horizontal projection morphology method only on already committed safe natural public fixtures, if such fixtures exist. If no committed safe natural public fixture exists, first perform a fixture-discovery/selection gate that identifies a candidate public-domain or explicitly licensed natural score fixture, documents provenance and safety, and seeks explicit Supervisor approval before committing any binary fixture. Do not use private scores, arbitrary downloads, generated dumps, screenshots, or unapproved binary artifacts. If no safe fixture can be identified, stop and report BLOCKED. No product implementation, semantic pitch inference, G-clef inference, rhythm inference, ScoreIR semantic change, GP export change, ML/OCR/model training, or private fixture use is authorised.

## Stop / Pivot Conditions

- Stop if the natural fixture evaluation requires complex ML/CV outside the deterministic geometric pipeline.
- Pivot if natural chords/beams cause the horizontal projection heuristic to fail completely.

## Explicitly Still Blocked

- semantic pitch implementation: yes
- G-clef inference implementation: yes
- rhythm implementation: yes
- whole-note recognition implementation: yes
- ScoreIR semantic changes: yes
- GP export changes: yes
- ML/OCR/model training: yes
