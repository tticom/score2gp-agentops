# PDF-only staff-to-TAB timing extraction and alignment v0.1

## 1. Current verified state

The product path for converting born-digital PDF guitar tablature to Guitar Pro `.gp` format operates without a mandatory MusicXML/MXL sidecar.
The milestone history includes:
* **PR #176**: Integrated the PDF-only tab-to-GP MVP path.
* **PR #177**: Corrected page/system reading order and resolved false chord stacking across page/system/local-bar boundaries.
* **PR #178**: Established a named fixed visual grouping tolerance of `PDF_ONLY_CHORD_X_TOLERANCE_PT = 10.0`.
* **PR #179**: Extracted visual chord grouping logic from `src/score2gp/build_ir.py` into `src/score2gp/pdf_only_chord_event_grouper.py`, introducing the `PdfOnlyChordEventGrouper` class.
* **Governance PR #54**: Reframed visual-spacing duration inference as a weak fallback model, not an authoritative timing model.

All 503 tests are currently passing, confirming structural validation success.

## 2. Correct timing model

In dual-staff scores (standard notation staff + TAB staff), TAB does not reliably provide note durations, rests, rhythmic subdivisions, time signatures, tuplets, or ties. Visual horizontal spacing in TAB is not authoritative timing and should only serve as a weak fallback when no standard staff timing can be recovered.
The authoritative timing evidence must come from standard staff notation:
* Time signatures
* Barlines and measure structures
* Noteheads (whole, half, quarter/eighth shapes)
* Stems, flags, and beams
* Augmentation dots
* Ties and tuplets
* Rest symbols

The architectural target is to **extract standard-staff timing evidence from the PDF and align it to TAB event groups**.

## 3. Scope and non-goals

This task is purely research, diagnostic, and architectural.
* **Goals**:
  * Investigate the current PDF extraction pipeline for standard staff elements.
  * Audit standard staff timing glyph/coordinate availability.
  * Design the staff-to-TAB alignment strategy and fallback/refusal policies.
  * Define the next architecture seam and author a developer-ready prompt.
* **Non-goals**:
  * Implementing staff timing extraction code in this task.
  * Modifying product code in `score2gp`.
  * Using visual gaps/spacing in TAB as authoritative timing.
  * Requiring MusicXML/MXL or external OMR.
  * Introducing OCR or scanned PDF support.
  * Committing private PDFs, generated files, or raw diagnostics.

## 4. Current PDF extraction pipeline

Inspecting `src/score2gp/pdf.py` reveals:
* PyMuPDF is used to parse text characters, text blocks, and vector graphics (`rect`, `line`, and paths).
* **TAB Staff Lines**: Detected by finding clusters of 6 horizontal vector lines.
* **Standard Notation Staff Lines**: Detected as clusters of 5 horizontal lines with gap spacing ~7.8 to 9.2 pt. Inside `classify_staff_line_group`, these groups are classified as `"notation"`.
* **Standard Staff Line Discarding**: Inside `_detect_tab_systems` (lines 3833-3835), if a line group is classified as `"notation"`, the parser executes a `continue` and discards it from system building:
  ```python
  for group in _tab_line_groups(horizontal):
      classification = classify_staff_line_group(group, page)
      if classification in ("notation", "ambiguous"):
          continue
  ```
* **Barlines**: Vertical vector segments are filtered for TAB staves. Standard staff barlines are only referenced briefly during notation-to-TAB barline inheritance to resolve missing TAB barlines on system boundaries.
* **Timing Glyphs**: The parser does **not** extract standard staff noteheads, stems, beams, flags, rests, augmentation dots, ties, tuplets, time signatures, clefs, or key signatures. They are completely ignored vector paths or text blocks.

## 5. Current TabRaw evidence model

Inspecting `src/score2gp/tabraw.py` shows:
* `TabRaw` and `TabCandidate` model only TAB-relevant evidence.
* Available kinds are: `fret`, `chord-symbol`, `technique-text`, and generic `candidate-text`.
* There are no classes, structures, or fields representing standard staff noteheads, stems, beams, flags, or rests.
* Candidates preserve page, system, staff, bar, and coordinate (`x`, `y`, `bbox`) identities, which is sufficient horizontally to align with standard staff elements, but the standard staff elements themselves are currently discarded.

## 6. Standard staff timing evidence availability

Born-digital PDFs contain standard notation staff vector paths (stems, beams, barlines, ties) and font glyphs (noteheads, rests, flags, time signatures, key signatures, accidentals, clefs).
In practice, the current `score2gp` codebase extracts **none** of this. It does not parse standard staff glyph names, standard note coordinates, or beam vector lines. The raw data exists in the PDF binary, but is ignored by the parser.

## 7. Minimum viable staff timing model

Before full notation parsing is written, a small internal timing model should be introduced to align timing to TAB events:
* **Model**: Introduce a `PdfStaffTimingEvent` class representing standard staff elements.
* **Fields**: `id`, `onset_ticks` (relative to bar start), `duration_ticks`, `is_rest`, `x` (visual horizontal coordinate), `bar_index`.
* **Scope**: Support 4/4 time signature fallbacks, basic notes, and rests, refusing tuplets or complex structures during initial validation.

## 8. Staff-to-TAB alignment strategy

Standard staff timing events and TAB fret event groups can be aligned horizontally within each bar:
1. Group `PdfStaffTimingEvent`s and TAB event groups (`subgroup_candidates` returned by `PdfOnlyChordEventGrouper`) by page, system, and bar index.
2. Sort both lists horizontally by `x`.
3. Match each `PdfStaffTimingEvent` to the nearest TAB event group by horizontal position within a tolerance (e.g., `15.0 pt`).
4. **Handling Rests**: If a standard staff event is marked as a rest (`is_rest = True`), it is generated as a rest event in the bar and does not consume any TAB fret candidates.
5. **Handling Notes/Chords**: The aligned TAB event group receives the exact onset and duration ticks from the `PdfStaffTimingEvent`.
6. **Mismatch Diagnostics**: Warning/refusal is triggered if TAB candidates exist with no matching standard staff timing events, or if a standard staff note has no TAB numbers.

## 9. Fallback and refusal policy

* **Missing Staff timing**: Fallback to uniform grid division or visual spacing fallback, keeping the warning `pdf_only_tab_inferred_timing` active.
* **Extraction Failures**: If standard staff lines are detected but timing elements (noteheads/stems) fail to parse, raise a warning/refusal category indicating incomplete notation parsing rather than guessing.

## 10. Diagnostics needed

We recommend adding the following private-safe metrics:
* `notation_staff_lines_detected`
* `parsed_notation_timing_events_count`
* `aligned_timing_events_count`
* `unaligned_tab_events_count`
* `unaligned_notation_events_count`
* `average_alignment_distance_pt`

## 11. Architecture seam

To decouple timing alignment from standard parsing, introduce two new modules:
1. `src/score2gp/pdf_staff_timing.py`
   * Class: `PdfStaffTimingEvent`
2. `src/score2gp/pdf_staff_tab_timing_aligner.py`
   * Class: `PdfStaffTabTimingAligner`
3. `tests/test_pdf_staff_tab_timing_aligner_alignment.py`
   * Focused test file naming production modules and behaviors.

## 12. Public synthetic test strategy

Create mock lists of `PdfStaffTimingEvent`s and `TabCandidate`s to test alignment without private PDFs:
* `test_pdf_staff_tab_timing_aligner_aligns_fret_to_notation_event`
* `test_pdf_staff_tab_timing_aligner_keeps_unaligned_separate`
* `test_pdf_staff_tab_timing_aligner_respects_bar_boundaries`
* `test_pdf_staff_tab_timing_aligner_handles_rests`

## 13. Privacy assessment

* Invariant verified: `git ls-files fixtures/private work` outputs only `fixtures/private/.gitkeep`.
* No private coordinates, paths, or scores are exposed.

## 14. Recommendation

Implement **Option A: staff timing model and synthetic aligner first**.
* Create `PdfStaffTimingEvent` and `PdfStaffTabTimingAligner` to prove the alignment algorithm and bar boundaries using synthetic test data before writing PyMuPDF code to parse standard noteheads/beams from real PDFs.
* Defer full PDF standard staff parsing to a later stage.

---

## 15. Smallest developer-ready implementation prompt

### Title
feat: implement standard-staff timing model and TAB alignment

### Context
Rhythm in PDF guitar scores is defined by the standard staff notation. The TAB staff only provides fret, string, and visual grouping. We need to introduce an alignment layer that maps standard staff timing to grouped TAB events.

### Current verified state
* Visual chord event grouping is refactored into `PdfOnlyChordEventGrouper`.
* Current timing uses a uniform grid in `build_ir.py`.

### Goal
Implement `PdfStaffTimingEvent` and `PdfStaffTabTimingAligner` to support horizontal alignment of standard staff timing events with TAB candidates by source bar and x-position using synthetic test data.

### Non-goals
* Do not extract standard staff vector shapes or text glyphs from real PDFs yet.
* Do not change chord grouping logic or source-bar ordering.
* Do not use TAB visual spacing as authoritative timing.

### Constraints
* Existing unit tests must pass.
* Keep `pdf_only_tab_inferred_timing` active for fallback timing.

### Required pre-flight checks
Confirm clean working tree and privacy status:
```bash
git status
git ls-files fixtures/private work
```

### Implementation guidance
1. **Timing Event Model**:
   * Create `src/score2gp/pdf_staff_timing.py`.
   * Implement `PdfStaffTimingEvent(id, onset_ticks, duration_ticks, is_rest, x, bar_index)`.
2. **Aligner**:
   * Create `src/score2gp/pdf_staff_tab_timing_aligner.py`.
   * Implement `PdfStaffTabTimingAligner` that takes a list of `PdfStaffTimingEvent`s and aligns them to TAB event groups (grouped by `PdfOnlyChordEventGrouper`) within the same bar by nearest visual `x` position (tolerance 15.0 pt).
   * Map the onset and duration of the matched staff events directly to the TAB event groups.
   * If a matched staff event has `is_rest = True`, emit it as a rest event in ScoreIR without notes.
3. **Integration**:
   * Wire `PdfStaffTabTimingAligner` into `build_ir.py` as an optional timing provider when timing events are provided.

### Validation
Implement tests in `tests/test_pdf_staff_tab_timing_aligner_alignment.py`:
* `test_pdf_staff_tab_timing_aligner_aligns_fret_to_notation_event`
* `test_pdf_staff_tab_timing_aligner_keeps_unaligned_separate`
* `test_pdf_staff_tab_timing_aligner_respects_bar_boundaries`
* `test_pdf_staff_tab_timing_aligner_handles_rests`

### Acceptance criteria
* Synthetic standard staff timing aligns correctly to TAB events.
* Rest events are created correctly without notes.
* Tests pass.

### Reporting format
```markdown
## Implementation complete
* Branch:
* Commit:
* PR:
```

---

## 16. Evidence and commands run

```bash
wsl sh -c "cd /home/tticom/work/score2gp-workspace/score2gp-agentops && git status && git switch main && git pull --ff-only origin main"
```

## 17. Limitations / what was not verified

* PDF standard staff parsing (noteheads, beams, rests) remains unverified and not implemented in this phase.
