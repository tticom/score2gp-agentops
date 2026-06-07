# PDF-only inferred rhythm quality v0.1

## 1. Current verified state
The project goal is to convert born-digital PDF guitar tablatures into playable Guitar Pro `.gp` packages without requiring a MusicXML/MXL sidecar.
The PDF-only MVP pathway (PR #176) and its subsequent ordering and duplicate-string splitting correction (PR #177) have successfully merged and verified.
The current verified state includes:
* Bypassing of the MusicXML preflight and validation safety gates.
* Visual staff, system, and bar assignment from TabRaw candidate geometries.
* Assignment of global output bars preserving correct page-system-bar reading order.
* Splitting of duplicate strings in horizontal x-groups to prevent false chord stacking.
* Structural GP packages generated for Lesson 3 are completely valid under the Guitar Pro validation engine (`validate_gp`).

## 2. Scope and non-goals
This task is purely research, diagnostic, and architectural.
* **Goals**:
  * Analyze the code-level logic for PDF-only event grouping and duration assignment.
  * Diagnose why Lesson 3 converts 461 notes to 461 events.
  * Formulate the smallest safe product increment to improve inferred rhythm quality.
  * Author a developer-ready prompt for the subsequent task.
* **Non-Goals**:
  * Changing any product codebase file.
  * Committing or copying private artifacts (PDFs, raw JSON diagnostics, raw score content, private fixture paths).
  * Introducing OCR or scanned PDF support.
  * Relying on the reference GP as an input dependency during conversion.

## 3. Current PDF-only rhythm policy in code
Inspecting `src/score2gp/build_ir.py` reveals the following rhythm inference steps:
1. **Visual Grouping**: Candidates are sorted by x-coordinates and grouped into visual columns using `_candidate_x_groups` with a fixed tolerance of `1.5` points:
   ```python
   abs(float(candidate.x) - _mean_x(groups[-1])) <= tolerance
   ```
2. **Duplicate-String Splitting**: Inside each visual group, if any candidates share a string index, they are split into sequential adjacent subgroups via `split_duplicate_strings`.
3. **Grid Density Selection**: The number of resulting event subgroups $N$ in a bar dictates the uniform rhythmic grid:
   * $N \le 8$: `eighth` notes (grid spacing = 480 ticks)
   * $N \le 16$: `16th` notes (grid spacing = 240 ticks)
   * $N \le 32$: `32nd` notes (grid spacing = 120 ticks)
   * $N > 32$: `64th` notes (grid spacing = 60 ticks)
4. **Onset and Duration Assignment**: Onsets are spaced uniformly: `onset_ticks = i * grid_spacing`. Durations are identical (`duration_ticks = grid_spacing`) for all events $i < N - 1$.
5. **Bar Filling (Sustain-to-Bar-End)**: The last event in the bar is assigned a stretched duration to fill the remainder of the 3840-tick bar: `duration_ticks = 3840 - onset_ticks`. No rests are ever inferred.

## 4. Sanitized Lesson 3 full-score metrics
The sanitized metrics for the full Lesson 3 PDF-only conversion after PR #177 are:
* **Status**: Success
* **GP Validate**: Pass (0 errors)
* **Output Bars**: 64
* **Playable fret candidates**: 461
* **Generated notes**: 461
* **Events generated**: 461
* **Duplicate-string events**: 0
* **Mixed page / system / local bar events**: 0
* **Inferred timing warning present**: True (`pdf_only_tab_inferred_timing`)

## 5. What appears musically wrong
* **Uniform Durations**: Since the visual spacing of notes is completely ignored during duration assignment, all notes in a bar (except the final note) receive the exact same duration. Visually wider gaps (e.g. representing quarter notes) are compressed to the same grid duration as narrow gaps (representing eighth notes).
* **Final Note Stretch**: The last event in a bar sustains all the way to the bar end, which can lead to extreme, musically incorrect durations (e.g., 3360 ticks) that do not match their visual spacing or actual musical value.
* **Notation Discrepancy**: The final event's `notated_duration` field is assigned the same value as the uniform grid (e.g., `eighth`), even though its actual tick duration might span a half or whole note. This mismatch is musically misleading.

## 6. Root-cause hypotheses checked
**Hypothesis**: *The production of 461 events for 461 notes is caused by an over-strict x-grouping tolerance (1.5 points) splitting simultaneous chords into separate events.*
* **Method**: Local analysis of `tab_raw.json` visual coordinates for Lesson 3 staves was performed.
* **Findings**:
  * The minimum horizontal visual distance between any two adjacent fret candidates inside the same bar across all 64 bars of Lesson 3 is **15.33 points**. The maximum distance is 44.98 points.
  * There are **zero** candidate pairs with a visual distance $\le 15.0$ points.
  * Consequently, even if the tolerance were increased from 1.5 to 15.0, the grouping results would be identical.
  * This score consists entirely of sequential single-note runs (arpeggiated triads). The count of 461 events for 461 notes is correct because there are no visual chords in the source score.

## 7. Reference GP comparison as evaluation-only evidence
Comparing the generated GP package to the reference GP (`fixtures/private/Lesson-3.gp`) yields:
* **Reference GP Note Count**: 30 (Wait, the reference GP only contains 30 notes across its bars, whereas the PDF score contains 461 notes. This indicates the reference GP is an incomplete validation stub or partial template and is not a suitable target for full-note count matching.)
* **Comparison Usefulness**:
  * Semantic GP comparisons (`compare_gp`) should be used to verify track layouts, tempo, and time signatures.
  * We must not enforce note/event count matching against this specific reference GP due to its partial nature.

## 8. Specific rhythm-quality gaps
1. **Lack of Layout-Aware Spacing**: Visual distance is a direct proxy for duration in born-digital engraving, but the code ignores it.
2. **Fixed 1.5 Point Tolerance**: A fixed coordinate tolerance is simple but needs to remain untouched for this first rhythmic increment to avoid regressing PR #177.
3. **No Minimum Quantization Threshold**: Visual noises or misalignments can force a bar into a dense 64th grid, causing chaotic rhythm notation.

## 9. Privacy assessment
* No private PDFs, generated `.gp` packages, raw JSON coordinates, or local machine paths are committed.
* The privacy invariant holds: `git ls-files fixtures/private work` outputs only `fixtures/private/.gitkeep`.

## 10. Recommendation
We recommend **Proportional Visual-Spacing Rhythm Inference** as the smallest safe product increment:
* Rather than spacing onsets uniformly, the visual horizontal distances (x-coordinates) of events inside a bar should determine their proportional onset times.
* The visual bar width can be estimated by extending the notes' bounding boxes by the average visual note distance.
* Visual onsets are mapped to raw ticks and then quantized to the nearest step on the grid (eighth, 16th, 32nd).
* **Scope Guardrail**: Preserve the current source-ordering and grouping behavior from PR #177. Do not change the fixed 1.5-point x-group/chord tolerance in the first rhythm PR.
* **Warning Policy**: Keep the `pdf_only_tab_inferred_timing` warning because rhythm remains layout-inferred rather than authoritatively annotated.
* **Diagnostics**: Add duration distribution diagnostics (e.g. counts of generated durations per category) to the JSON execution report.

---

## 11. Smallest developer-ready implementation prompt

### Title
feat: implement proportional visual-spacing rhythm inference for PDF-only conversion

### Context
In the PDF-only tab conversion pathway, event durations and onsets are currently spaced uniformly based on the count of events in each bar, completely ignoring visual horizontal layout gaps. This results in poor musical readability.

### Current verified state
* Direct PDF conversion without MusicXML is active via the `--pdf-only-tab` flag.
* Reading order and bar structure are correctly preserved.
* GP output validation passes, but rhythmic structures are musically uniform.

### Goal
Implement a layout-aware rhythm inference policy that estimates event onsets proportionally to their visual x-positions inside the bar, and quantizes them to a clean musical grid. Preserve the current source-ordering and grouping behavior from PR #177, including the fixed 1.5-point x-group tolerance.

### Non-goals
* Do not change the visual x-group tolerance of 1.5 points.
* Do not introduce any dependency on MusicXML or external OMR libraries.
* Do not change the CLI interface.
* Do not use reference GP files as an input dependency.

### Constraints
* Ensure that all public regression tests in `tests/test_pdf_only_tab.py` continue to pass.
* Keep the `pdf_only_tab_inferred_timing` warning active.
* Do not commit or expose any private score contents or paths.

### Required pre-flight checks
Confirm that the working tree is clean and that the privacy invariant holds:
```bash
git status
git ls-files fixtures/private work
```
Ensure only `fixtures/private/.gitkeep` is tracked.

### Implementation guidance
Modify `src/score2gp/build_ir.py` inside `build_ir_from_tabraw_only`:
1. **Bar Width Estimation**:
   * For a bar containing event subgroups at visual positions $X_1, X_2, \dots, X_N$:
   * Estimate the average horizontal spacing: $\Delta_{avg} = \frac{X_N - X_1}{N - 1}$ if $N > 1$, else a default visual gap (e.g., 20.0 points).
   * Define a virtual bar end position: $X_{end} = X_N + \Delta_{avg}$.
   * The total visual width is $W = X_{end} - X_1$.
2. **Proportional Onsets**:
   * Calculate the relative position of each event $i$: $R_i = \frac{X_i - X_1}{W}$.
   * Calculate the raw onset in ticks: $T_i = R_i \times 3840$.
3. **Quantization**:
   * Choose the grid spacing $G$ based on the event count $N$ as currently implemented.
   * Quantize each $T_i$ to the nearest multiple of $G$: $Q_i = \text{round}(T_i / G) \times G$.
   * Enforce boundary conditions: $Q_0 = 0$, and $Q_i < Q_{i+1}$ (adjusting or collapsing if necessary to prevent overlapping/out-of-order onsets).
4. **Duration Assignment**:
   * Set `duration_ticks` of event $i$ to $Q_{i+1} - Q_i$, and the last event to $3840 - Q_{N-1}$.
   * Ensure `notated_duration` is assigned to match the quantized duration value (e.g. if duration is 960 ticks, assign "quarter"; if 480 ticks, assign "eighth", etc.).
5. **Diagnostics**:
   * Report duration distribution metrics (histogram of generated note values) in the `pdf_only_diagnostics` block of the JSON execution report.

### Validation
* Write a new unit test `test_pdf_only_proportional_rhythm` in `tests/test_pdf_only_tab.py` using a mock TabRaw with non-uniform visual spacings (e.g. a wide gap followed by narrow gaps) to assert that the generated event onsets correspond to proportional tick values (e.g. a quarter note followed by eighth notes).
* Assert that the current grouping behavior and 1.5-point tolerances are untouched.
* Execute the test suite:
  ```bash
  PYTHONPATH=src .venv/bin/python3 -m pytest tests/test_pdf_only_tab.py
  ```

### Acceptance criteria
* The generated onsets reflect visual coordinate proportions.
* No events have overlapping onsets or zero/negative durations.
* All unit tests pass.

### Stop conditions
* If the layout-aware onsets violate the Guitar Pro bar duration boundaries, stop and fallback to the uniform grid spacing.

### Reporting format
```markdown
## Implementation complete
* Branch:
* Commit:
* Tests run:
```

---

## 12. Evidence and commands run
* Checked WSL version and python packages:
  ```bash
  wsl python3 --version
  wsl env PYTHONPATH=src .venv/bin/python3 scratch/analyze_rhythm_lesson3.py
  wsl env PYTHONPATH=src .venv/bin/python3 -m score2gp.cli inspect-gp fixtures/private/Lesson-3.gp
  ```
* Output of coordinates check inside `Lesson-3` tab_raw:
  * Minimum visual horizontal distance: 15.334 points.
  * Distance $\le$ 15.0: 0 pairs.

## 13. Limitations / what was not verified
* We did not verify the alignment of expressive techniques (slides, bends) under proportional rhythm.
* The bar width estimation assumes engraver spacing is visual and monotonic, which may fail if there are complex multi-voice structures or overlapping text elements.
