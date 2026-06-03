# Melodic Soloing Timing / Onset Mapping Blocker Investigation v0.1

## Verdict
First failing timing/onset stage: **C. Candidate-to-bar assignment loss (driven by internal ambiguous double-barline rejection)**.

The remaining 26 candidates are NOT blocked by a missing timing or onset mapping engine, as the pipeline successfully utilizes the MusicXML file as the rhythm and voice authority. Instead, the loss is caused by the OMR barline recovery stage, where multiple internal double-barlines (thin/thick vertical lines spaced ~2.8 points apart) are grouped into clusters of size 2 and rejected as `pdf_barline_ambiguous`. 

Because these internal barlines are rejected, only 5 bar boxes are constructed across the 3 systems (instead of the expected 8 measures). The dynamic programming alignment maps these 5 boxes to measures 1, 2, 5, 6, 7 of the MusicXML, leaving measures 3, 4, 8 completely unaligned (skipped as alignment gaps). Consequently, candidates belong to incorrect measure pools during the sequential note matching pass, leaving 26 playable candidates unused and 26 MusicXML notes unmatched.

---

## Evidence

* **Product branch**: `main`
* **Product commit hash**: `1f00c7c1063bef7477d917b067fc2d9b00386579`
* **Agentops branch**: `research/melodic-soloing-timing-onset-mapping-v0.1`
* **Agentops commit hash**: `e5c06aa34a320dfda80780d1e19c6a4ac867384a`
* **Commands run**:
  - `wsl PYTHONPATH=. .venv/bin/python3 -m pytest`
  - `wsl PYTHONPATH=. .venv/bin/python3 scripts/private_e2e_smoke.py`
  - `wsl PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py`
  - `git ls-files fixtures/private work`
  - `git diff --check`
  - `git status --short`
* **Public test result**: `455 passed in 18.52s`
* **Private audit result**: 
  - Lessons 3–7 stable (`pass | gp_output_technique_loss_expected`)
  - Melodic Soloing: `pass | gp_output_note_coverage_low | 56 matched | 56 notes`
* **Private-safety output**:
  ```text
  fixtures/private/.gitkeep
  ```
* **Working tree status**: Clean (except for `.antigravitycli` metadata files)

---

## Why Previous Barline/Grouping Fixes Are No Longer the Active Blocker
Previous work successfully resolved the fragmented staff-line grouping issue (merged in PR #163), allowing the middle TAB system to be grouped and recovering 56 matched notes (up from 41). 
PR #164 successfully introduced defensive inherited barline filtering (`MIN_INHERITED_INTERNAL_BAR_WIDTH = 130.0`) to reject notation-staff tuplet hooks from splitting TAB measures. However, since the true internal TAB barlines are explicit (drawn directly on the TAB staff as double barlines) and are not inherited, the 130.0 width check did not interact with them. The active blocker is now the OMR barline ambiguity filter completely rejecting internal double barlines.

---

## Timing Warning Analysis

* **Exact source of warning**: `src/score2gp/pdf.py` (Line 1265, inside `_detect_tab_systems`).
* **Trigger condition**: Triggered unconditionally when the text `"standard tuning"` is parsed on the page.
* **Interpretation**: The warning `pdf_timing_mapping_not_implemented` is purely diagnostic and informational (severity `"info"`). It does not block the build-ir phase. The timing alignment utilizes the paired MusicXML file as the source of rhythm/timing authority, sequentially mapping X-sorted candidates to the MusicXML note events within each successfully aligned measure. Therefore, the lack of visual timing layout mapping is not the cause of the note loss.

---

## Melodic Soloing Stage-Loss Table

| Stage | Observed Count | Expected Relationship | Loss Signal | Evidence Path under `work/` | Interpretation |
|---|---|---|---|---|---|
| **PDF extraction** | 166 total candidates (82 playable fret, 51 technique text, 33 non-playable) | Matches visual contents | 0 candidates lost | `private_e2e_smoke_v0_1/private_input_custom_melodic_soloing/extracted.tabraw.json` | All 82 playable fret candidates are successfully extracted from the PDF. |
| **staff/system grouping** | 3 TAB systems grouped | 3 systems expected | 0 systems lost | `private_e2e_smoke_v0_1/private_input_custom_melodic_soloing/warnings.json` | Fragmentation grouping successfully recovers the 3 TAB systems. |
| **barline/bar-box construction** | 5 bar boxes constructed | 8 measures expected | 3 bar boxes missing | `private_e2e_smoke_v0_1/private_input_custom_melodic_soloing/warnings.json` | Double barlines at x=804, x=1415, x=1919 (Sys 1), x=1064 (Sys 2), and x=1250 (Sys 3) are rejected as `pdf_barline_ambiguous`. |
| **candidate-to-system assignment** | 82 playable candidates | 82 playables -> 82 assigned | 0 candidates lost | `private_e2e_smoke_v0_1/private_input_custom_melodic_soloing/extracted.tabraw.json` | All 82 candidates are assigned to the 3 systems. |
| **candidate-to-bar assignment** | 82 playable candidates | 82 playables -> 82 assigned | 0 candidates lost | `private_e2e_smoke_v0_1/private_input_custom_melodic_soloing/extracted.tabraw.json` | All 82 candidates are assigned to the 5 constructed bar boxes. |
| **candidate-to-string/fret assignment** | 82 playable candidates | 82 playables -> 82 assigned | 0 candidates lost | `private_e2e_smoke_v0_1/private_input_custom_melodic_soloing/extracted.tabraw.json` | All 82 candidates have valid string and fret assignments. |
| **candidate-to-onset assignment** | 56 candidates matched | 82 playables -> 56 matched | 26 unmatched candidates | `private_e2e_smoke_v0_1/private_input_custom_melodic_soloing/score.ir.json` | 56 notes matched to aligned measures 1, 2, 5, 6, 7. 26 candidates in skipped measures 3, 4, 8 remain unmatched. |
| **ScoreIR construction** | 8 measures, 56 notes | Equals matched candidates | 0 notes lost | `private_e2e_smoke_v0_1/private_input_custom_melodic_soloing/score.ir.json` | ScoreIR is successfully constructed with the 56 matched notes. |
| **GPIF serialization** | 8 measures, 56 notes | Equals ScoreIR notes | 0 notes lost | `private_gp_quality_audit_v0_1/summary.json` | GPIF successfully serializes all 56 notes. |

---

## Comparison Table

| Metric / Track | Melodic Soloing | Lesson 3 | Lesson 4 | Lesson 5 | Lesson 6 | Lesson 7 |
|---|---|---|---|---|---|---|
| **Playable Candidates** | 82 | 461 | 549 | 297 | 238 | 624 |
| **Matched Notes (GPIF)** | 56 | 459 | 546 | 295 | 235 | 624 |
| **ScoreIR Notes** | 56 | 459 | 546 | 295 | 235 | 624 |
| **Inferred Systems** | 3 | 7 | 7 | 5 | 3 | 6 |
| **Bar Boxes** | 5 | 23 | 29 | 11 | 10 | 25 |
| **Barline Ambiguous Warnings**| 3 | 0 | 0 | 0 | 0 | 0 |
| **Timing Warnings** | 1 | 1 | 1 | 1 | 1 | 1 |

---

## Architecture Recommendation

### Recommended Next Developer Task
Implement a conservative representative selection mechanism for internal clusters of close barlines in `src/score2gp/pdf.py`.

#### Affected Files
- `src/score2gp/pdf.py`

#### Proposed Design
1. In `filter_tab_barline_candidates` (around line 3612), when an internal cluster of close barlines is found (length > 1 and not at the leftmost/rightmost system edges), do not reject all candidates in the cluster as `pdf_barline_ambiguous`.
2. Instead, select the leftmost candidate (`cluster[0]`) as the representative and mark its decision as accepted (`True, None`).
3. Mark all other candidates in the cluster as `pdf_barline_double_secondary` (rejected, but with a safe/info warning reason that does not flag the system as dirty or skip it).
4. This resolves double barlines internally on the TAB staff without merging measures, matching the way leftmost/rightmost double barlines are already successfully resolved.

#### Why This Design is Safe
- It is coordinate-independent and generalizes across all scores.
- It does not affect Lessons 3–7, as they do not have any internal close clusters (and thus zero `pdf_barline_ambiguous` warnings).
- It prevents the dynamic programming alignment from skipping measures due to merged bar boxes.

#### Validation Plan
- Run `python -m pytest` to verify all 455 public tests pass.
- Run `python scripts/private_gp_quality_audit.py` to confirm that Melodic Soloing note matching increases to 82 (100% yield) and Lessons 3–7 remain stable.

#### Acceptance Criteria
- `private_input_custom_melodic_soloing` matched notes count increases from 56 to 82.
- Zero regressions in Lessons 3–7.
- Private-safety invariant is maintained.

#### Stop Conditions
- Any public test fails.
- Performance or note count regresses in Lessons 3–7.
- Private-safety invariant outputs anything other than `fixtures/private/.gitkeep`.
