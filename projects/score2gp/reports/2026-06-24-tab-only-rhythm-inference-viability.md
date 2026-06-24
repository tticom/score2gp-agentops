# Architect Report: Tab-Only Rhythm Inference Viability

## Context
Following the completion of Product PR #323 and Governance PR #202, the baseline supports tab-only quarter-rest candidate extraction. The active blocker is to determine whether Score2GP can deterministically infer rhythm (durations, ties, full rest vocabulary, syncopation) for tab-only PDF input with sufficient reliability to justify Developer implementation.

## Verified Baseline
* **Governance PR #202**: Merged (`738d32f025f114e3b315cac75a373efc11392c1f`)
* **Product PR #323**: Merged (`bcbad586b8d9e28cf4ad130db0c0532db783b020`)
* **Product Baseline**: `6afdd3195f37eca6e319caf33dbeccfbbf1d4b5c`

## Outcome: Outcome C
**No credible deterministic or non-ML path is currently viable. The project must stop or pivot.**

## Summary of Evidence

### Fact
* **Quarter Rest Narrowness**: The existing quarter-rest extraction (`src/score2gp/quarter_rest_recogniser.py`) relies on identifying a unique cluster of 30+ vector fragments with a specific width/height ratio. It does not generalize to whole, half, eighth, or sixteenth rests.
* **Lack of Tab Stem/Beam Extraction**: The current vector pipeline (`src/score2gp/pdf_staff_geometry.py` and `whole_note_recogniser.py`) extracts `flag_beam_candidates` and stem bboxes *only* for standard notation staves. Tab staves are not processed for stems or beams.
* **Naive Rhythm Fallback**: The `--pdf-only-tab` rhythm assignment in `src/score2gp/build_ir.py` (`build_ir_from_tabraw_only`) assigns durations based purely on `N`, the number of horizontal candidate groups in the measure (e.g., if `N <= 8`, all notes are given `grid_spacing = 480` / eighth notes).
* **Available Fixtures**: Existing public fixtures for tab-only (`fixtures/public/generated_simple/simple/TabOnlySingleNote.pdf`, `TabOnlyTwoNotes.pdf`, `TabOnlyQuarterNoteRests.pdf`, `TabOnlyThreeBarsOfRests.pdf`) only test extremely simple or single-duration geometries.

### Inference
* **Underdetermined Spacing**: Without explicit rhythmic markers (stems/beams) or a full rest vocabulary, horizontal proportional spacing is fundamentally ambiguous. A large horizontal gap could be a held whole note or a quarter note followed by rests. Furthermore, spacing in typical PDFs is elastic due to typesetting constraints (lyrics, ties, minimum widths).
* **High Cost of Deterministic Extraction**: To support deterministic rhythm for Guitar Pro-style tabs, Score2GP would need to build a massive new pipeline to extract tab-specific stems, beams, and dots, which are often embedded inside or below the staff lines.

### Hypothesis
* **Pivot to MusicXML Sidecar**: Score2GP already possesses a robust MusicXML sidecar alignment pipeline (`pdf_staff_tab_timing_aligner.py`). Tab-only processing should remain a fallback with approximate durations (as it currently warns: `pdf_only_tab_inferred_timing`), and accurate rhythm must rely on standard notation or MusicXML.
* **Pivot to ML-Assisted Recognition**: If tab-only PDFs must be supported with accurate rhythm, an ML vision model is required to segment the elastic spatial context and recognize diverse rest/rhythm markers natively.

### Unknown
* Whether the userbase will accept `--pdf-only-tab` emitting default quarter/eighth notes without rhythm inference, or if true rhythm extraction is a hard product requirement for tab-only mode.

## Source Paths Inspected
* `src/score2gp/build_ir.py` (rhythm assignment logic)
* `src/score2gp/quarter_rest_recogniser.py` (rest extraction shape logic)
* `src/score2gp/pdf_staff_geometry.py` (flag/beam geometry extraction scope)
* `src/score2gp/whole_note_recogniser.py` (interaction with stems/beams)
* `src/score2gp/pdf_only_chord_event_grouper.py` (horizontal candidate grouping)
* `tests/test_pdf_only_tab.py` (rhythm inference policy tests)

## Fixture Set
* `fixtures/public/generated_simple/simple/TabOnlySingleNote.pdf` (Tests minimal bar logic)
* `fixtures/public/generated_simple/simple/TabOnlyTwoNotes.pdf` (Tests minimal bar division)
* `fixtures/public/generated_simple/simple/TabOnlyQuarterNoteRests.pdf` (Tests the narrow quarter-rest implementation)
* `fixtures/public/generated_simple/simple/TabOnlyThreeBarsOfRests.pdf` (Tests negative extraction limits)

*Reasoning for limited set:* These fixtures confirm the current behavior. No fixtures exist that can prove complex tab rhythm inference because the capability does not exist and the input domain (tab without stems) is often mathematically underdetermined.

## Viability Criteria
1. **Bar segmentation**: Can segment bars deterministically via barlines. (Pass)
2. **Event ordering**: Can order events within a bar horizontally. (Pass)
3. **Duration evidence**: Must be able to extract precise durations from stems, beams, full rests, or spacing. (Fail. Stems/beams not extracted for tab. Rests limited to quarter. Spacing is elastic and ambiguous).
4. **Acceptance threshold**: Must reconstruct syncopated tab rhythms accurately without MusicXML. (Fail).

## Stop/Pivot Triggers Activated
* Deterministic path is unviable due to underdetermined spatial evidence and lack of tab stem/beam primitives.
* Task is stopped (Outcome C).
* Recommended Pivot: Treat tab-only PDF support as inherently approximate rhythmically (relying on the existing fallback), or authorise ML-assisted extraction.

## Developer Implementation Authorised
No.

## Reviewer Architecture Verification Required
No. (Outcome C requires supervisor pivot decision, not Reviewer approval of an architecture).
