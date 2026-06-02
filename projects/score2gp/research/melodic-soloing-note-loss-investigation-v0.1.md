# Melodic Soloing Note Loss Investigation v0.1

## Verdict
First failing stage identified: **C. Candidate-to-TAB association loss** (driven primarily by upstream layout/system grouping failure and incorrect barlines-based skip criteria).

Specifically, the middle TAB system is completely missed due to greedy line-grouping logic that gets trapped by fragmented horizontal segments (broken by fret digit printouts) and fails the overlap check. The first TAB system is successfully grouped but skipped entirely during IR construction because an informational double-barline warning is incorrectly classified as a rejected barline. Only the third system is processed, which is recovered as a single measure and mapped to Bar 7 of the MusicXML template, matching only 16 notes out of 82 total.

---

## Evidence

* **Product repo branch**: `main`
* **Product repo commit hash**: `1097c43659e806e3c6a2a8e348cc8ffd6923d473`
* **Agentops repo branch**: `research/melodic-soloing-note-loss-investigation-v0.1`
* **Agentops repo commit hash**: `2ae32f9e8fb647a39a7255e8bea1cf61c6a60ed5`
* **Commands run**:
  - `PYTHONPATH=. .venv/bin/python3 -m pytest`
  - `PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py`
  - `git ls-files fixtures/private work`
  - `git status --ignored --short`
  - `git diff --check`
* **Public test result**: `447 passed in 21.86s` (No regressions)
* **Private audit result**: Passed (Lesson 3: 451 matched, Lesson 4: 546 matched, Lesson 5: 295 matched, Lesson 6: 115 matched, Lesson 7: 624 matched, Melodic Soloing: 16 matched with category `gp_output_fret_matching_suspect`)
* **Private-safety output**: `fixtures/private/.gitkeep` (No private or generated assets tracked in git)
* **Working tree status**: Clean on both repositories

---

## Baseline Comparison Table

| Input Label | Status | Quality Category | Playable Candidates | Matched Candidates | Unmatched Candidates | Matched Ratio | ScoreIR Notes | GPIF Notes | Warning Code Categories |
|---|---|---|---|---|---|---|---|---|---|
| `private_input_custom_lesson_3` | pass | `gp_output_technique_loss_expected` | 454 | 451 | 3 | 99.3% | 451 | 451 | Layout details, Double-barline ignore, Unsafe grouping, Tab-extraction-incomplete |
| `private_input_custom_lesson_4` | pass | `gp_output_technique_loss_expected` | 549 | 546 | 3 | 99.5% | 546 | 546 | Layout details, Double-barline ignore, Unsafe grouping, Tab-extraction-incomplete |
| `private_input_custom_lesson_5` | pass | `gp_output_technique_loss_expected` | 297 | 295 | 2 | 99.3% | 295 | 295 | Layout details, Double-barline ignore, Unsafe grouping, Tab-extraction-incomplete |
| `private_input_custom_lesson_6` | pass | `gp_output_technique_loss_expected` | 115 | 115 | 0 | 100.0% | 115 | 115 | Layout details, Double-barline ignore, System/geometry unresolved, Tab-extraction-incomplete |
| `private_input_custom_lesson_7` | pass | `gp_output_technique_loss_expected` | 624 | 624 | 0 | 100.0% | 624 | 624 | Layout details, Double-barline ignore, Unsafe grouping, Tab-extraction-incomplete |
| `private_input_custom_melodic_soloing` | pass | `gp_output_fret_matching_suspect` | 59 | 16 | 43 | 27.1% | 16 | 16 | Layout details, Double-barline ignore, Barbox construction fail, Barbox too narrow, Large tab staff spacing, Tab-extraction-incomplete |

---

## Melodic Soloing Stage-Loss Table

| Stage | Observed Count | Expected Relationship | Loss Signal | Evidence Path | Interpretation |
|---|---|---|---|---|---|
| **Extraction (OMR)** | 164 total candidates (59 playable fret, 51 technique text, 54 non-playable) | Matches visual PDF contents | 1 full TAB system missed during OMR grouping | `summary.json` (`extraction`), `pdf.py` (`_tab_line_groups`) | The PDF has standard notation + TAB staves. 3 notation systems are found, but only 2 TAB systems are grouped. The middle TAB system is missed because the greedy grouping algorithm cannot handle staff lines broken by fret numbers and fails the overlap check. |
| **Candidate Filtering** | 23 playable candidates evaluated | 59 playable candidates -> 59 evaluated | 36 playable candidates discarded (System 1) | `summary.json` (`extraction`), `build_ir.py` (`_synchronize_skipped_system_measures`) | System 1 is skipped entirely because a double-barline warning (`pdf_barline_double_secondary`) starting with `pdf_barline_` is incorrectly treated as a rejected barline, setting `has_rejected_barlines = True`. |
| **Candidate-to-IR Matching** | 16 matched, 7 unmatched | 23 evaluated candidates matched to MusicXML measures | 7 unmatched candidates | `summary.json` (`build_ir`), `score.ir.json` | System 2 is recovered as a single measure. Because the start barline and final double barline are detected, notation-to-TAB barline inheritance is skipped (requires `< 2` barlines), so it has no internal measures. It is aligned to Bar 7 of the MusicXML template, matching 16 of its 23 candidates. Bars 1-6 and 8 receive 0 candidates. |
| **ScoreIR Construction** | 8 bars, 16 events, 16 notes | Equals matched candidates | 0 notes lost | `score.ir.json` (`score_ir`) | ScoreIR notes match the 16 matched candidates exactly. No notes are lost during ScoreIR object creation. |
| **GPIF Serialization** | 8 measures, 16 beats, 16 notes | Equals ScoreIR notes | 0 notes lost | `smoke.gp` (audit summary) | The relational/classic GPIF writers serialize all 16 notes. No loss during writing. |

---

## Root-Cause Hypothesis

We identify three overlapping root causes that combine to cause the major note loss:

1. **Greedy Grouping with Fragmented Lines (OMR Line Grouping)**:
   - In guitar tabs, horizontal staff lines are broken where fret digit characters are drawn. This creates collinear segments on the same Y coordinates (e.g., left, middle, right fragments).
   - The grouping function `_tab_line_groups` is purely greedy and ranks candidate segments by absolute overlap width with the first line. Because it does not backtrack, it mixes left and right segments from different strings. This creates a low-overlap 6-line combination that fails the overlap ratio check (`_is_coherent_large_tab_group` requires `overlap_ratio >= 0.80`) and is discarded, completely missing the middle TAB system.
2. **Double-Barline Classification & Clustering Limitation (OMR Barlines)**:
   - At the rightmost edge of a TAB system, double barlines are drawn (thin + thick vertical lines) spaced ~9-10 points apart.
   - The OMR barline candidate filter `filter_tab_barline_candidates` only clusters barlines within 6.0 points. Because the double-barline lines are spaced ~9 points apart, they are treated as two separate barlines.
   - This creates a tiny, invalid bar box of width ~9-10 points at the rightmost edge of the systems, triggering `pdf_bar_box_too_narrow` and `pdf_bar_box_construction_not_enough_for_build_ir` on every detected system.
3. **Incorrect Skipped System Decision (Build-IR)**:
   - `build_ir.py` filters out and skips systems with rejected barlines by checking if any warning starts with `pdf_barline_`.
   - The double-barline representative logic correctly chooses one line and discards the duplicate, logging `pdf_barline_double_secondary` with `severity: info`.
   - Because this starts with `pdf_barline_`, `build_ir.py` flags the system as having rejected barlines, causing System 1 to be skipped entirely, discarding 36 playable candidates.
4. **Notation-to-TAB Inheritance Bypass**:
   - TAB staves only inherit internal barlines from their partner notation staff if `len(valid_barlines) < 2`.
   - Because the start barline and the rightmost double barlines are both successfully detected, the TAB staves have 3 valid barlines, meaning the internal barlines are never inherited. This causes the systems to be recovered as single measures instead of 4 separate measures.

### Weak/Alternative Hypotheses Considered
- *Speculative OCR Thresholds / Low-Confidence digits*: We considered whether fret digits were filtered out during extraction. However, `tabraw` contains 59 playable fret candidates with good confidence (mean 0.451), showing extraction is successful. The loss occurs post-extraction due to layout/grouping failures.
- *GPIF writer note-dropping*: We checked if notes were dropped during serialization. However, ScoreIR note count (16) matches GPIF note count (16), showing the writer is stable.

---

## Recommended Architecture

We propose the following design-level fixes:

1. **Ignore Informational Warnings in Skip Logic** (`src/score2gp/build_ir.py`):
   - Refine the loop in `build_ir.py` that populates `skipped_systems`. Ignore warning codes starting with `pdf_barline_` if their severity is `"info"` (such as `pdf_barline_double_secondary`), or only trigger skips on severe warnings like `pdf_barline_candidates_present_but_invalid` or explicit errors.
2. **Increase Barline Clustering Threshold** (`src/score2gp/pdf.py`):
   - Increase the barline clustering distance in `filter_tab_barline_candidates` from `6.0` to `12.0` points. This will correctly group thin/thick double barline lines at the end of systems into a single logical barline, preventing the creation of tiny, invalid rightmost bar boxes.
3. **Allow Notation-to-TAB Inheritance for Internal Barlines** (`src/score2gp/pdf.py`):
   - Adjust the condition `len(valid_barlines) < 2` for notation-to-TAB barline inheritance. If the TAB staff has barlines but lacks internal ones compared to its partner notation staff, inherit the internal barlines.
4. **Backtracking / Global Search in Grouping** (`src/score2gp/pdf.py`):
   - Enhance the greedy grouping loop in `_tab_line_groups` to evaluate multiple combinations (or backtrack) when ranking candidate segments, selecting the 6-line combination that maximizes overlap ratio rather than getting stuck on the first greedy choice.

---

## Next Developer Prompt

```text
# Antigravity Task: Melodic Soloing Note Loss Remediation v0.1

## Role
You are the Developer.

## Goal
Resolve the note-loss blockers for `private_input_custom_melodic_soloing` by improving final double-barline clustering, notation-to-TAB barline inheritance conditions, informational warning skip logic, and line grouping fragment handling in the OMR and IR build pipeline.

## Non-goals
- Do not hardcode specific coordinates for melodic soloing.
- Do not speculatively modify OCR digit confidence thresholds.
- Do not alter the MusicXML schema or representation.
- Do not commit private PDFs or generated musical assets.

## Constraints
- Keep Lessons 3–7 stable. All existing test cases must pass with zero regressions.
- Ensure the private-safety invariant is maintained: `git ls-files fixtures/private work` must output exactly `fixtures/private/.gitkeep`.

## Likely Affected Files
- `src/score2gp/pdf.py`
- `src/score2gp/build_ir.py`

## Implementation Approach
1. **Double-Barline Clustering**: In `src/score2gp/pdf.py` (`filter_tab_barline_candidates`), increase the clustering distance for vertical line segments from `6.0` to `12.0` points. This ensures thin/thick final double barlines are grouped as a single logical barline rather than creating tiny rightmost bar boxes.
2. **Ignored Informational Warnings during IR construction**: In `src/score2gp/build_ir.py` (`build_ir`), refine the loop that builds `skipped_systems` from `tabraw.warnings`. Ensure informational warnings (severity: `"info"`, e.g. `pdf_barline_double_secondary`) do not flag `has_rejected_barlines = True` and cause the system to be skipped.
3. **Notation-to-TAB Barline Inheritance**: Modify the trigger for notation-to-TAB barline inheritance in `src/score2gp/pdf.py`. Instead of checking if `len(valid_barlines) < 2`, check if the partner notation staff has more barlines than the TAB staff, and inherit the internal ones.
4. **Coherent Line Grouping**: Refine `_tab_line_groups` in `src/score2gp/pdf.py` to handle segmented staff lines (interrupted by fret digits) by evaluating alternative segment selections instead of a purely greedy choice, ensuring the middle system is grouped successfully.

## Validation Commands
Run and report the results of:
- `python -m pytest` (Must pass all public tests, currently 447)
- `python scripts/private_gp_quality_audit.py`
- `git ls-files fixtures/private work` (Must only output `fixtures/private/.gitkeep`)
- `git status --short`
- `git diff --check`

## Acceptance Criteria
- `private_input_custom_melodic_soloing` status must be `pass` with matched notes close to 82 (100% of TAB notes on the page).
- Lessons 3–7 remain stable with no regressions.
- No private/generated artifacts are tracked in Git.
```
