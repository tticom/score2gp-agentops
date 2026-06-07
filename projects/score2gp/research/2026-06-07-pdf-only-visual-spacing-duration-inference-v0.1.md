# PDF-only visual-spacing duration inference v0.1

## 1. Current verified state

The product path for converting born-digital PDF guitar tablature to Guitar Pro `.gp` format operates without a mandatory MusicXML/MXL sidecar.
The milestone history includes:
* **PR #176**: Integrated the PDF-only tab-to-GP MVP path.
* **PR #177**: Corrected page/system reading order and resolved false chord stacking across page/system/local-bar boundaries.
* **PR #178**: Established a named fixed visual grouping tolerance of `PDF_ONLY_CHORD_X_TOLERANCE_PT = 10.0`.
* **PR #179**: Extracted visual chord grouping logic from `src/score2gp/build_ir.py` into `src/score2gp/pdf_only_chord_event_grouper.py`, introducing the `PdfOnlyChordEventGrouper` class.

All 503 tests are currently passing, confirming structural validation success.

## 2. Scope and non-goals

This task is purely research, diagnostic, and architectural.
* **Goals**:
  * Analyze the code-level logic for PDF-only duration assignment.
  * Identify remaining rhythm readability issues after visual chord grouping improvements.
  * Evaluate visual-spacing duration inference options and their limitations as fallback timing models.
  * Define the conceptual boundaries between visual spacing and standard staff timing extraction.
  * Recommend the next correct architectural timing model and author a follow-up investigation prompt.
* **Non-goals**:
  * Implementing code changes in the product repo (`score2gp`).
  * Changing the visual x-grouping tolerance value.
  * Weaking duplicate-string split safety or source-bar isolation.
  * Relying on the reference GP as an input dependency during conversion.
  * Introducing scanned PDF, OCR, or Audiveris dependencies.
  * Committing raw coordinates, private PDFs, or generated GP files.

## 3. Current PDF-only rhythm policy in code

In `src/score2gp/build_ir.py` (lines 1769-1825), the current duration policy in the PDF-only path operates as follows:
1. **Grid Density Selection**: The number of visual event subgroups $N$ in a bar determines a uniform grid spacing $G$ and notated duration name:
   * $N \le 8$: $G = 480$ ticks (eighth note grid)
   * $N \le 16$: $G = 240$ ticks (16th note grid)
   * $N \le 32$: $G = 120$ ticks (32nd note grid)
   * $N > 32$: $G = 60$ ticks (64th note grid)
2. **Onset Assignment**: Onsets are spaced uniformly: $\text{onset}_i = i \times G$.
3. **Duration Assignment**: 
   * For all events $i < N - 1$, the duration is fixed to the grid spacing: $\text{duration}_i = G$.
   * For the final event in the bar ($i = N - 1$), the duration is stretched to fill the remainder of the bar to ensure a total bar duration of 3840 ticks: $\text{duration}_{N-1} = 3840 - (N - 1) \times G$.
4. **Rests and Chords**: No rests are inferred. Chords and single notes share the same onset/duration mapping.

## 4. Sanitized duration and spacing evidence

Sanitized metrics for a full Lesson 3 PDF-only conversion show:
* **Output Bars**: 64
* **Playable fret candidates**: 461
* **Generated notes**: 461
* **Events generated**: 461
* **Inferred timing warning**: Present (`pdf_only_tab_inferred_timing`)
* **Visual distances**: All event pairs inside bars have visual horizontal gaps $\ge 15.33$ pt, indicating sequential single-note lines (arpeggios).
* **Rhythmic results**: Uniformly assigned eighth notes with the final event of each bar stretched (e.g., to 2880 ticks in a 3-event bar), which is visually and musically disjointed.

## 5. Remaining rhythm-quality problems

1. **Rhythmic Uniformity**: Ignoring visual spacing means quarter notes and eighth notes are mapped to identical tick durations, compressing/expanding musical rhythm.
2. **Extreme Final Note Stretch**: The last event absorbs all trailing space, leading to extremely long sustained notes (e.g. dotted half or whole notes) that do not match the engraving.
3. **No Rest Inference**: Large gaps are treated as sustained notes, rather than potential rests.
4. **Lack of Coordinate Scaling**: Visual coordinates are absolute page positions and are not projected onto a relative, bar-width-scaled spacing model.

## 6. Visual-spacing inference options

We assess how visual horizontal spacing should be treated:
* **Limitations of Visual Spacing**: Visual spacing is **NOT** a reliable or authoritatively correct timing model. In born-digital engravers, horizontal spacing is adjusted for visual readability (fret numbers, fingerings, margins) and does not map linearly to musical durations. Relying on visual spacing as a primary duration proxy is musically incorrect.
* **Role as Fallback Evidence**: Visual spacing should only be treated as a weak fallback model when no standard staff notation can be extracted. In dual-staff scores (standard staff + TAB), the authoritative source of timing is the standard notation: time signature, note/rest symbols, beams, dots, ties, and tuplets.
* **Option A: Uniform division (Current)**: Low quality fallback.
* **Option B: Proportional visual spacing**: Calculate raw proportional onsets $T_i = \frac{X_i - X_1}{W} \times 3840$, and round them to the nearest multiple of a grid spacing $G$. Useful only as a weak fallback timing model when standard staff elements are entirely missing.

## 7. End-of-bar and final-event handling

The current final-event stretch causes bad notation.
* **Virtual Bar End**: To solve final-event stretch, we can estimate a virtual end-of-bar coordinate $X_{\text{end}}$.
  * For $N > 1$ events, calculate the average horizontal visual spacing: $\Delta_{\text{avg}} = \frac{X_N - X_1}{N - 1}$.
  * Define the virtual bar-end: $X_{\text{end}} = X_N + \Delta_{\text{avg}}$.
  * The total visual width is $W = X_{\text{end}} - X_1$.
  * Under this model, the final event's visual duration is $X_{\text{end}} - X_N = \Delta_{\text{avg}}$, which maps to a duration matching the average event spacing, eliminating the pathological final stretch.
  * Any remaining space from the last quantized onset to 3840 is absorbed by the final note (distributing the rounding error) or trailing rests, but without rest support, it sustains cleanly.

## 8. Rest inference assessment

Heuristic rest inference (e.g. inserting a rest for a visual gap $> 30.0$ pt) is highly risky:
* Tabs do not contain visual rest symbols.
* Gaps can represent sustained notes (let ring) or engraver adjustments rather than rests.
* *Recommendation*: Defer rest inference in the fallback pathway. True rests must be extracted from the standard staff notation.

## 9. Quantization policy assessment

The safest fallback quantization policy is:
1. Distribute raw proportional onsets: $T_i = \frac{X_i - X_1}{W} \times 3840$.
2. Choose a grid spacing $G$ (e.g., $120$ ticks for 32nd notes, or select $G$ based on $N$ as currently done).
3. Quantize each onset: $Q_i = \text{round}(T_i / G) \times G$.
4. Enforce monotonicity: $Q_0 = 0$, and $Q_i < Q_{i+1}$ (if $Q_{i+1} \le Q_i$, shift $Q_{i+1} = Q_i + G$).
5. Compute event durations: $\text{duration}_i = Q_{i+1} - Q_i$ for $i < N - 1$, and $\text{duration}_{N-1} = 3840 - Q_{N-1}$.
6. Map `notated_duration` fields directly to the resulting quantized tick values.
7. Keep `pdf_only_tab_inferred_timing` active.

## 10. Diagnostics needed

We recommend adding the following to the JSON diagnostics:
* `shortest_duration_ticks`: Min duration generated.
* `max_visual_gap_pt`: Maximum visual coordinate gap.
* `total_quantization_error`: RMS error of $Q_i - T_i$.
* `monotonicity_shifts_applied`: Count of forced onset adjustments.

## 11. Architecture seam for duration inference

Even though the primary rhythm should come from standard staff extraction, a dedicated duration inferer is still valuable to decouple from orchestration:
* **File name**: `src/score2gp/pdf_only_duration_inferer.py`
* **Class name**: `PdfOnlyDurationInferer`
* **Test file name**: `tests/test_pdf_only_duration_inferer_visual_spacing.py`
  * Naming matches the production module and behavior being tested.

## 12. Privacy assessment

* The research note contains only aggregated statistics and sanitized references.
* No machine paths, raw visual coordinates, or private files are exposed.
* Invariant verified: `git ls-files fixtures/private work` outputs only `fixtures/private/.gitkeep`.

## 13. Recommendation

Do not implement proportional visual-spacing duration inference as the primary timing model.
* Visual spacing is not musically correct or authoritative for rhythm. It must remain a weak fallback timing model.
* The authoritative rhythm must come from standard staff notation.
* **Recommended Next Step**: Investigate PDF-only standard staff timing extraction and alignment. We need to analyze how standard staff notation elements (beams, flags, dots, rests, note duration shapes, time signatures) can be extracted directly from the PDF tab coordinate geometries and aligned with the TAB fret candidates.

---

## 14. Smallest developer-ready implementation prompt

### Title
research: investigate PDF-only staff-to-TAB timing extraction and alignment

### Context
Authoritative rhythm in a standard PDF score comes from the standard staff notation (time signature, note and rest heads, flags, beams, dots, tuplets, ties, barlines). The TAB staff only provides fret, string, and visual groupings. Relying on visual spacing is a weak fallback.

### Current verified state
* Visual grouping is refactored into `PdfOnlyChordEventGrouper`.
* Timing uses a uniform grid in `build_ir.py` with a timing warning.

### Goal
Investigate how standard staff notation elements can be extracted from the born-digital PDF TabRaw geometries and aligned with TAB candidates inside the same system.

### Non-goals
* Do not modify product code or change current duration inference.
* Do not introduce OCR or scanned PDF support.
* Do not use reference GP as an input dependency.

### Constraints
* The investigation must be private-safe.
* No private PDFs or Machine paths should be committed.

### Required pre-flight checks
Ensure only `fixtures/private/.gitkeep` is tracked inside private directories:
```bash
git status
git ls-files fixtures/private work
```

### Investigation guidance
1. **Structure Analysis**:
   * Inspect how standard staff lines, noteheads, beams, stems, and flags are represented in `TabRaw` candidate geometries.
   * Determine if the extractor outputs standard staff symbols or if we need to expand `TabRaw` parser support.
2. **Alignment Strategy**:
   * Analyze vertical coordinate alignment (y-positions) to identify standard staff vs. TAB staff.
   * Map standard staff note/rest onsets (using horizontal x-coordinates) to TAB fret candidates.
   * Assess how tuplets, ties, and rests are visually aligned in the standard staff relative to the TAB numbers.
3. **Recommendation**:
   * Formulate a conceptual model to build a timing map from standard staff note/rest durations and assign them to vertical columns of TAB frets.
   * Recommend how the standard staff timing can be parsed and aligned.

### Validation
Produce a research note under `projects/score2gp/research/` detailing:
* PDF standard staff element availability in the active TabRaw extractor.
* Proposed coordinate alignment algorithm.
* Proposed diagnostic metrics.

### Reporting format
```markdown
## Investigation complete
* Branch:
* Commit:
* PR:
```

---

## 15. Evidence and commands run

```bash
wsl sh -c "cd /home/tticom/work/score2gp-workspace/score2gp-agentops && git status && git switch main && git pull --ff-only origin main"
```

## 16. Limitations / what was not verified

* Standard staff element extraction has not been implemented or verified in the current codebase parser; the availability of these layout elements needs audit.
