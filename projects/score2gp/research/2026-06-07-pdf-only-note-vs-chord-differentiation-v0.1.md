# PDF-only note-vs-chord differentiation v0.1

## 1. Current verified state
The project goal is to convert born-digital PDF guitar tablatures into playable Guitar Pro `.gp` packages without requiring a MusicXML/MXL sidecar.
The PDF-only MVP pathway (PR #176) and its subsequent ordering and duplicate-string splitting correction (PR #177) have successfully merged and verified.
* Bypassing of the MusicXML preflight and validation safety gates is verified.
* Assignment of global output bars preserving correct page-system-bar reading order is verified.
* Splitting of duplicate strings in horizontal x-groups to prevent false chord stacking is verified.
* The current full-score Lesson 3 smoke test successfully generates a valid GP file with no duplicate strings or cross-page/system/local-bar event mixing.

## 2. Scope and non-goals
This task is purely research, diagnostic, and architectural.
* **Goals**:
  * Inspect the current PDF-only event grouping behavior to understand how sequential notes and chords are distinguished.
  * Identify why visually simultaneous chord notes may be emitted as separate single-note events.
  * Formulate the smallest safe product increment to improve chord/event formation.
  * Author a developer-ready prompt for the subsequent task.
* **Non-Goals**:
  * Implementing any product codebase changes immediately.
  * Committing or copying private artifacts (PDFs, raw JSON coordinates, generated GP files, private work paths).
  * Introducing OCR or scanned PDF support.
  * Modifying the duration policy or inferring rests in this task.
  * Weakening the source bar ordering and duplicate-string safeguards from PR #177.

## 3. Current PDF-only event grouping policy in code
Inspecting `src/score2gp/build_ir.py` inside `build_ir_from_tabraw_only` shows the current event grouping policy:
1. **Fret Filtering**: Fret candidates are filtered per output bar:
   ```python
   bar_frets = [c for c in fret_candidates if ...]
   ```
2. **Visual X-Column Grouping**: Fret candidates are grouped using `_candidate_x_groups` with a fixed tolerance of `1.5` points. The function sorts candidates by x-coordinate and groups those whose distance to the mean x-coordinate of the current group is $\le 1.5$ points:
   ```python
   abs(float(candidate.x) - _mean_x(groups[-1])) <= tolerance
   ```
3. **Duplicate-String Splitting**: Inside each visual group, if any candidates share a string index, they are split into sequential adjacent subgroups via `split_duplicate_strings` to prevent false chord stacking.
4. **Event Generation**: Each resulting subgroup becomes an `Event` object containing one or more `Note` objects.

## 4. Current definition of a chord event
The product currently defines a chord event implicitly as:
* **Multiple fret candidates grouped into the same visual x-group (tolerance $\le 1.5$ points) that do not share the same string index.**
This definition is implicit in the visual column grouping and subsequent duplicate-string split logic.

## 5. Sanitized Lesson 3 grouping evidence
In the full Lesson 3 PDF-only conversion:
* **Fret Candidates**: 461
* **Events Generated**: 461
* **Notes per Event**: 1 note per event for all 461 events (0 chords generated).
* **Adjacent Spacing Coordinates Check**:
  * Total adjacent candidate pairs inside bars: 397
  * Minimum x-distance between adjacent candidates: **15.334 points**
  * Maximum x-distance: 44.983 points
  * Pairs with distance $\le 15.0$ points: 0
* **Interpretation**: There are no visually simultaneous chord notes in the Lesson 3 PDF. Every note is horizontally separated by at least 15.33 points. The generated 461 single-note events are correct because Lesson 3 consists entirely of sequential single-note arpeggiated triads.

## 6. Evidence for visually chordal material being split
Extraction and spacing analysis on adjacent private lesson PDFs reveals that visually chordal material is being split under the current policy:
* **Lesson 4**: 549 fret candidates. Min distance: 11.666 points. Chords at Tol 1.5: 0. Chords at Tol 15.0: 1 (false chord stack of adjacent arpeggio notes in Bar 2, 3, 1, 6).
* **Lesson 5**: 297 fret candidates. Min distance: 9.520 points.
  * **Chords at Tol 1.5**: 0
  * **Chords at Tol 10.0**: 10
  * **Chords at Tol 15.0**: 66
  * **Inspected Example**: Bar (1, 1, 1, 1) contains a triad chord with frets `10` (string 6, x=102.29), `8` (string 5, x=111.88), and `7` (string 4, x=121.47). The horizontal visual distance between adjacent notes is **9.59 points**.
  * **Cause**: In digital guitar tab engraving, chord notes are vertically aligned but can have slight horizontal offsets (up to 10 points) due to double-digit numbers (`10`), font glyph widths, or slight visual slant.
  * **Consequence**: Under the current 1.5-point tolerance, these simultaneous chord notes are split into separate sequential events, creating a musically incorrect arpeggio instead of a chord.
* **Lesson 6 & 7**: Contain chords with exact vertical alignment (min distance 0.0 points), which successfully group as chords at all tolerances (1.5 to 15.0 points).

## 7. Fixed tolerance versus adaptive tolerance assessment
* **Current Fixed Tolerance (1.5 points)**: Too narrow. It fails to group chord notes with minor horizontal offsets (like the 9.59 pt offsets in Lesson 5).
* **Too Wide Fixed Tolerance (e.g. 15.0 points)**: Too wide. It introduces false chord grouping for fast arpeggiated runs (like the 11.66 pt adjacent notes in Lesson 4).
* **Adaptive / Layout-Aware Spacing**:
  * Chord offset gaps are typically $\le 10.0$ points.
  * Sequential note gaps are typically $\ge 11.5$ points.
  * Therefore, a layout-aware fixed threshold of **10.0 points** is the optimal boundary to successfully group offset chords in Lesson 5 while preserving sequential notes in Lesson 4.
  * Making the threshold relative to the staff size (e.g., `0.2 * staff_height` or `1.5 * staff_line_spacing`) is even more robust against PDF scaling.

## 8. Duplicate-string and false-chord regression risks
Any updated chord-grouping policy must protect the regression tests added in PR #177:
* **No Same-String Chords**: Two notes on the same string must never form a chord. If a wider visual tolerance groups two candidates on the same string, they must be split into sequential events.
* **No Cross-Boundary Grouping**: Candidates must never group across pages, systems, or local bars. Grouping must be strictly isolated to the source bar.
* **Preserve Source Identity**: Candidate top-level page, system, and bar identities must be preserved.

## 9. Reference GP comparison as evaluation-only evidence
* **Reference GP**: The reference GP package is used strictly for evaluation comparison (e.g. checking note and chord counts) and must not be an input dependency.
* **Lesson 3 Reference**: Confirmed to contain only 30 notes total (an incomplete validation stub) and is not a target for note/event count matching.

## 10. Specific event-formation gaps
1. **Visual Column Grouping is Over-Strict**: The 1.5-point tolerance splits offset chord notes into separate events.
2. **Lack of Layout Scale Sensitivity**: A fixed coordinate value does not adapt to PDF resolution or scaling.

## 11. Privacy assessment
* No private files, generated `.gp` packages, raw coordinates, or local machine paths are committed.
* Privacy invariant holds: `git ls-files fixtures/private work` outputs only `fixtures/private/.gitkeep`.

## 12. Recommendation
We recommend implementing **Layout-Aware Visual Column Grouping for Chord Formation**:
* Increase the visual grouping tolerance in `_candidate_x_groups` from `1.5` to a configurable chord grouping threshold of **10.0 points** (or `0.2 * staff_height` if staff height is available).
* Strictly preserve the duplicate-string splitting logic (`split_duplicate_strings`) and source-bar isolation. This ensures that any candidates on the same string within the 10.0-point group are safely split into adjacent sequential events.
* Preserve all page-system-bar ordering safeguards from PR #177.

---

## 13. Smallest developer-ready implementation prompt

### Title
feat: implement layout-aware chord event grouping for PDF-only conversion

### Context
In the PDF-only tab conversion pathway, simultaneous notes in a chord are sometimes split into separate sequential events because their visual x-coordinates have minor horizontal offsets (up to 10 points) due to double-digit numbers or font widths, exceeding the current strict 1.5-point tolerance.

### Current verified state
* The PDF-only pathway compiles structurally valid GP files.
* Fret candidates are isolated by source bar and ordered by page, system, and bar.
* Duplicate strings inside visual columns are split sequentially.

### Goal
Allow fret candidates on different strings within the same source bar to group into a single chord event when their visual x-distance is within a layout-aware chord grouping threshold of **10.0 points**, while preserving sequential arpeggio notes and duplicate-string splitting.

### Non-goals
* Do not change the duration/rhythm policy.
* Do not infer rests.
* Do not use reference GP as an input dependency.
* Do not change the CLI interface.

### Constraints
* The 1.5-point grouping behavior for same-string candidates must be preserved via duplicate-string splitting.
* All source-ordering and page/system boundary protections from PR #177 must continue to pass.
* The `pdf_only_tab_inferred_timing` warning must remain active.
* Do not commit private fixture files or generated artifacts.

### Required pre-flight checks
Confirm that the working tree is clean and that the privacy invariant holds:
```bash
git status
git ls-files fixtures/private work
```
Ensure only `fixtures/private/.gitkeep` is tracked.

### Implementation guidance
Modify `src/score2gp/build_ir.py`:
1. In `build_ir_from_tabraw_only`, when calling `_candidate_x_groups`, change the `tolerance` argument from `1.5` to `10.0` points:
   ```python
   x_groups = _candidate_x_groups(bar_frets, tolerance=10.0)
   ```
2. Ensure `split_duplicate_strings` is executed on the resulting groups. This splits any candidates sharing a string index into sequential subgroups, protecting duplicate-string safety.
3. Verify that `_candidate_x_groups` logic correctly sorts candidates by x-coordinate and groups them against the mean x of the current group.

### Validation
* Write new public unit tests in `tests/test_pdf_only_tab.py`:
  * `test_pdf_only_groups_small_x_offsets_across_strings_as_chord`: Assert that candidates on different strings with an x-distance of 9.0 points form a single chord event.
  * `test_pdf_only_keeps_sequential_notes_separate_when_x_gap_is_large`: Assert that candidates with an x-distance of 12.0 points are split into separate events.
  * `test_pdf_only_does_not_group_duplicate_string_candidates_as_chord`: Assert that two candidates on the same string within 10.0 points are split sequentially.
* Execute the test suite:
  ```bash
  PYTHONPATH=src .venv/bin/python3 -m pytest tests/test_pdf_only_tab.py
  ```

### Acceptance criteria
* Visually simultaneous notes on different strings with spacing $\le 10.0$ points form chord events.
* Sequential notes with spacing $\ge 11.0$ points remain separate events.
* Duplicate strings in the same group are split.
* No cross-page, cross-system, or cross-bar events are generated.
* All unit tests pass.

### Stop conditions
* If the 10.0-point grouping collapses sequential notes of different strings inside the same bar into false chords, stop and roll back the tolerance to a narrower value (e.g. 5.0 or 8.0 points).

### Reporting format
```markdown
## Implementation complete
* Branch:
* Commit:
* Tests run:
```

---

## 14. Evidence and commands run
* Extracted tabraw for Lessons 3, 4, 5, 6, 7:
  ```bash
  wsl env PYTHONPATH=src .venv/bin/python3 -m score2gp.cli extract-tab fixtures/private/Lesson-4.pdf --out work/private/lesson4_tab_raw.json
  wsl env PYTHONPATH=src .venv/bin/python3 scratch/find_chords_all_lessons.py
  ```
* Distance analysis summary:
  * **Lesson 3**: Min distance 15.33 pt. Chords at all tolerances = 0.
  * **Lesson 4**: Min distance 11.66 pt. Chords at Tol 10.0 = 0. Chords at Tol 15.0 = 1.
  * **Lesson 5**: Min distance 9.52 pt. Chords at Tol 1.5 = 0. Chords at Tol 10.0 = 10. Chords at Tol 15.0 = 66.
  * **Lesson 6 & 7**: Chords at Tol 1.5 = 1 & 50 respectively (due to exact 0.0 pt visual alignment).

## 15. Limitations / what was not verified
* We did not verify chord grouping on sheets with custom tuning or staves containing more than 6 strings.
* Staff height relative tolerance was not implemented because staff height is not directly stored in TabRaw candidate fields.
