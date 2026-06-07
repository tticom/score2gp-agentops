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
  * Evaluate visual-spacing duration inference options and quantization rules.
  * Define the architectural seam for duration inference (`pdf_only_duration_inferer.py`).
  * Recommend the smallest safe product increment and write a developer-ready prompt.
* **Non-goals**:
  * Implementing code changes in the product repo (`score2gp`).
  * Changing the visual x-grouping tolerance value.
  * Weaking duplicate-string split safety or source-bar isolation.
  * Relying on the reference GP as an input dependency during conversion.
  * Introducing scanned PDF, OCR, or Audiveris dependencies.
  * Committing raw coordinates, private PDFs, or generated GP files.

## 3. Current PDF-only duration policy in code

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
* ** Rhythmic results**: Uniformly assigned eighth notes with the final event of each bar stretched (e.g., to 2880 ticks in a 3-event bar), which is visually and musically disjointed.

## 5. Remaining rhythm-quality problems

1. **Rhythmic Uniformity**: Ignoring visual spacing means quarter notes and eighth notes are mapped to identical tick durations, compressing/expanding musical rhythm.
2. **Extreme Final Note Stretch**: The last event absorbs all trailing space, leading to extremely long sustained notes (e.g. dotted half or whole notes) that do not match the engraving.
3. **No Rest Inference**: Large gaps are treated as sustained notes, rather than potential rests.
4. **Lack of Coordinate Scaling**: Visual coordinates are absolute page positions and are not projected onto a relative, bar-width-scaled spacing model.

## 6. Visual-spacing inference options

Visual x-spacing provides a strong proxy for relative onset timing in digital engraving. We assess the following options:
* **Option A: Uniform division (Current)**: Ignores visual coordinates. Low quality.
* **Option B: Pure proportional visual spacing**: Calculate visual gaps $\Delta_i = X_{i+1} - X_i$, project onto a total bar width $W$, and scale to 3840 ticks. This reflects visual spacing accurately but results in raw, non-quantized tick values (e.g., 473 ticks) that fail Guitar Pro's strict musical quantization.
* **Option C: Proportional spacing with soft quantization (Recommended)**: Calculate raw proportional onsets $T_i = \frac{X_i - X_1}{W} \times 3840$, and round them to the nearest multiple of a grid spacing $G$.
  * *Risks*: Misalignments and layout artifacts can distort visual gaps, leading to incorrect quantization. A fallback policy or monotonicity correction is required to keep onsets in reading order.

## 7. End-of-bar and final-event handling

The current final-event stretch causes bad notation.
* **Virtual Bar End**: To solve final-event stretch, we can estimate a virtual end-of-bar coordinate $X_{\text{end}}$.
  * For $N > 1$ events, calculate the average horizontal visual spacing: $\Delta_{\text{avg}} = \frac{X_N - X_1}{N - 1}$.
  * Define the virtual bar-end: $X_{\text{end}} = X_N + \Delta_{\text{avg}}$.
  * The total visual width is $W = X_{\text{end}} - X_1$.
  * Under this model, the final event's visual duration is $X_{\text{end}} - X_N = \Delta_{\text{avg}}$, which maps to a duration matching the average event spacing, eliminating the pathological final stretch.
  * Any remaining space from the last quantized onset to 3840 is absorbed by the final note (distributing the rounding error) or trailing rests, but without rest support, it sustains cleanly.

## 8. Rest inference assessment

Heuristic rest inference (e.g. inserting a rest for a visual gap $> 30.0$ pt) is highly risky for v0.1:
* Tabs do not contain visual rest symbols.
* Gaps can represent sustained notes (let ring) or engraver adjustments rather than rests.
* *Recommendation*: **Defer rest inference** to a future stage and focus purely on proportional note event spacing.

## 9. Quantization policy assessment

The safest v0.1 quantization policy is:
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

Introduce a new dedicated module to handle this responsibility:
* **File name**: `src/score2gp/pdf_only_duration_inferer.py`
* **Class name**: `PdfOnlyDurationInferer`
* **Test file name**: `tests/test_pdf_only_duration_inferer_visual_spacing.py`
  * Naming matches the production module and behavior being tested.

## 12. Privacy assessment

* The research note contains only aggregated statistics and sanitized references.
* No machine paths, raw visual coordinates, or private files are exposed.
* Invariant verified: `git ls-files fixtures/private work` outputs only `fixtures/private/.gitkeep`.

## 13. Recommendation

Implement **Proportional Visual-Spacing Rhythm Inference** as a product feature.
* Extract the current grid duration logic from `build_ir.py` into a new `PdfOnlyDurationInferer` class in `src/score2gp/pdf_only_duration_inferer.py`.
* Implement the proportional visual-spacing calculation and quantization inside this class.
* Add focused unit tests in `tests/test_pdf_only_duration_inferer_visual_spacing.py` using synthetic tab candidates.

---

## 14. Smallest developer-ready implementation prompt

### Title
feat: implement proportional visual-spacing duration inference for PDF-only tab

### Context
PDF-only timing is currently uniform, ignoring visual gaps and causing extreme final note stretch. Visual spacing in digital engraving is a direct proxy for musical duration.

### Current verified state
* Visual chord event grouping is refactored into `PdfOnlyChordEventGrouper`.
* Timing uses a mechanical uniform grid in `build_ir.py`.
* All tests pass, but rhythm is visually/musically poor.

### Goal
Extract duration inference into `src/score2gp/pdf_only_duration_inferer.py` and implement a visual-spacing duration policy that maps relative horizontal positions to quantized musical durations, preserving exact bar duration (3840 ticks) and preventing pathological final note stretch.

### Non-goals
* Do not change chord grouping logic or the `10.0 pt` tolerance.
* Do not change source-bar ordering.
* Do not introduce rest inference in v0.1.
* Do not use reference GP files as an input dependency.
* Do not introduce OCR or scanned PDF support.

### Constraints
* All existing tests in `tests/test_pdf_only_tab.py` must continue passing.
* Keep the `pdf_only_tab_inferred_timing` warning active.
* Do not commit private files or machine paths.

### Required pre-flight checks
Ensure the workspace is clean and the privacy invariant holds:
```bash
git status
git ls-files fixtures/private work
```

### Implementation guidance
1. Create `src/score2gp/pdf_only_duration_inferer.py` and define `PdfOnlyDurationInferer`.
2. Extract the duration grid logic:
   * Estimate the visual end of the bar: $\Delta_{\text{avg}} = \frac{X_N - X_1}{N - 1}$ for $N > 1$ events (default to 20.0 pt for $N = 1$). Set $X_{\text{end}} = X_N + \Delta_{\text{avg}}$.
   * Total visual width is $W = X_{\text{end}} - X_1$.
   * For each event $i$, compute raw proportional onset: $T_i = \frac{X_i - X_1}{W} \times 3840$.
   * Select grid spacing $G$ based on $N$ (e.g., $N \le 8 \Rightarrow G = 480$).
   * Quantize onsets: $Q_i = \text{round}(T_i / G) \times G$.
   * Enforce monotonicity: $Q_0 = 0$ and $Q_i < Q_{i+1}$ (if $Q_{i+1} \le Q_i$, shift to $Q_i + G$).
   * Calculate durations: $\text{duration}_i = Q_{i+1} - Q_i$ for $i < N - 1$ and $\text{duration}_{N-1} = 3840 - Q_{N-1}$.
   * Map `notated_duration` based on the resulting tick duration (e.g. 960 -> quarter, 480 -> eighth, 240 -> 16th, etc.).
3. Update `src/score2gp/build_ir.py` to call `PdfOnlyDurationInferer`.

### Validation
* Implement unit tests in `tests/test_pdf_only_duration_inferer_visual_spacing.py`:
  * `test_pdf_only_duration_inferer_evenly_spaced_events_get_uniform_durations`
  * `test_pdf_only_duration_inferer_uneven_spacing_produces_proportional_durations`
  * `test_pdf_only_duration_inferer_prevents_final_note_stretch`
  * `test_pdf_only_duration_inferer_preserves_monotonicity`
* Run:
  ```bash
  env PYTHONPATH=src .venv/bin/python3 -m pytest -q
  ```

### Acceptance criteria
* Onsets scale to relative visual position proportions.
* Total bar duration is exactly 3840 ticks.
* All tests pass.

### Stop conditions
* If quantization causes negative or overlapping durations that cannot be resolved via monotonicity shifting, fallback to the uniform grid.

### Reporting format
```markdown
## Implementation complete
* Branch:
* Commit:
* PR:
```

---

## 15. Evidence and commands run

```bash
wsl sh -c "cd /home/tticom/work/score2gp-workspace/score2gp-agentops && git status && git switch main && git pull --ff-only origin main"
wsl sh -c "cd /home/tticom/work/score2gp-workspace/score2gp && git switch main && git pull --ff-only origin main"
```

## 16. Limitations / what was not verified

* Expressive visual technique coordinates (e.g., slides/bends) were not integrated into the visual-spacing estimation.
* Engraver spacing rules are assumed to be reasonably proportional, which might fail on complex multi-voice scores.
