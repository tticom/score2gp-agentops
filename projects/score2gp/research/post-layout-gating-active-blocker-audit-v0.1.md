# Research Report: Post-Layout-Gating Active Blocker Audit v0.1

Durable record of the active blocker audit executed from product `main` branch after merging Product PR #169 and Agentops PR #35.

## Verdict
`private_input_1 milestone achieved under default flow`

All remaining failures for other private inputs are now cleanly classified and refused by explicit, structured safety gates rather than failing downstream with generic grouping/alignment errors.

---

## Current milestone status
- **`private_input_1`**: **Milestone Achieved**. Successfully compiles to ScoreIR and writes a validated, playable `.gp` file with **137 / 137 matched notes** (representing 100% of non-grace notes parsed from MusicXML).
- **Lessons 3–7 & Melodic Soloing**: **100% Stable**. Stable note counts are maintained across all custom private inputs.
- **Other Inputs**: Cleanly and explicitly refused by safety gates during inspection/orchestration.

---

## Private input summary table

| Input Label | Input Type | Page Count | Playable Candidates | Status | Matched | Unmatched | First Blocker / Refusal Code | Suitability / Recommendation |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| `private_input_1` (Derek Trucks) | pdf-tab-musicxml | 2 | 153 | `pass` | 137 | 16 | None | Milestone achieved. |
| `private_input_2` (CAGED shapes) | pdf-tab-only (ASCII) | 1 | 54 | `fail` | 0 | 54 | `pdf_input_class_ascii_tab_requires_alignment` / `pdf_input_class_missing_musicxml_sidecar` | `provide-matching-musicxml-before-build-ir` |
| `private_input_custom` (Rock Ballads) | pdf-tab-only (Scanned) | 177 | 0 | `fail` | 0 | 0 | `pdf_input_class_scanned_pdf_unsupported` | `provide-extractable-vector-pdf` |
| `private_input_custom` (Chord Melody) | pdf-tab-only (Scanned) | 105 | 0 | `fail` | 0 | 0 | `pdf_input_class_scanned_pdf_unsupported` | `provide-extractable-vector-pdf` |
| `private_input_custom` (Practice Lick) | pdf-tab-only (Drawn) | 2 | 61 | `fail` | 0 | 61 | `pdf_input_class_missing_musicxml_sidecar` | `provide-matching-musicxml-before-build-ir` |
| `private_input_custom` (Legato Licks) | pdf-tab-only (Drawn) | 1 | 0 | `fail` | 0 | 0 | `pdf_input_class_missing_musicxml_sidecar` | `provide-matching-musicxml-before-build-ir` |
| `private_input_custom_lesson_3` | pdf-tab-musicxml | 4 | 461 | `pass` | 459 | 2 | None | Stable. |
| `private_input_custom_lesson_4` | pdf-tab-musicxml | 5 | 549 | `pass` | 546 | 3 | None | Stable. |
| `private_input_custom_lesson_5` | pdf-tab-musicxml | 3 | 297 | `pass` | 295 | 2 | None | Stable. |
| `private_input_custom_lesson_6` | pdf-tab-musicxml | 6 | 238 | `pass` | 235 | 3 | None | Stable. |
| `private_input_custom_lesson_7` | pdf-tab-musicxml | 5 | 624 | `pass` | 624 | 0 | None | Stable. |
| `private_input_custom_melodic_soloing` | pdf-tab-musicxml | 1 | 82 | `pass` | 82 | 0 | None | Stable. |

---

## Next highest-value blocker
The **residual candidate loss (16 unmatched candidates)** in our milestone target, `private_input_1`.
Specifically:
- **15 candidates** correspond to grace notes that are currently skipped during MusicXML parsing (`musicxml-grace-skipped`).
- **1 candidate** is a slight pitch/alignment delta in a complex bar.

---

## Why it is higher priority
- **Primary Target Completeness**: Grace notes are the final blocker preventing `private_input_1` from achieving **100% fret candidate alignment** (currently at 137/137 matched notes from MusicXML, but leaving 15 visual fret numbers on the TAB staff unused).
- **Core Product Value**: Addressing grace notes represents a concrete, high-value product implementation opportunity in our MusicXML parsing (`musicxml.py`), alignment orchestration (`build_ir.py`), and GPIF serialization (`gpif.py`) pipelines.
- **Other Failures are Non-Product Issues**:
  - Scanned PDF failures (`Rock Ballads`, `Chord Melody`) are due to unsupported layouts (OCR is out of scope).
  - ASCII tab and drawn TAB failures (`private_input_2`, `Practice Lick`, `Legato Licks`) are blocked by missing data (missing MusicXML sidecars or ASCII alignment files). Resolving them is an input-acquisition issue rather than a code/algorithm limitation.

---

## Recommended smallest next task
- **Task**: **MusicXML and Relational GPIF Grace Note Support v0.1**.
- **Scope**:
  - Implement parsing of grace notes (e.g. `<grace/>` tag and attributes such as grace-steal or slash) in `src/score2gp/musicxml.py`.
  - Propagate grace note attributes into `ScoreIR` and map them during alignment.
  - Implement relational GPIF serialization for grace notes in `src/score2gp/gpif.py` to correctly map visual grace notes to the generated `.gp` file.
  - Verify that `private_input_1` unmatched count reduces from 16 to 1.

---

## Commands run
```bash
git switch main
git pull --ff-only origin main
PYTHONPATH=. .venv/bin/python3 -m pytest
PYTHONPATH=. .venv/bin/python3 scripts/private_e2e_smoke.py
PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py
git ls-files fixtures/private work
git diff --check
```

---

## Test results
- **Public Tests**: `466 passed` successfully.
- **E2E Private Smoke**: Successfully generated reports for all inputs.
- **Quality Audit**:
  - `private_input_1` status: `pass` (Matched: 137, Playable: 153).
  - Lessons 3–7: Stable status `pass` (all notes matched).
  - Melodic Soloing: Stable status `pass` (82 notes matched).

---

## Private-safety result
Running `git ls-files fixtures/private work` outputs exactly:
```text
fixtures/private/.gitkeep
```
No private or generated assets are tracked.

---

## Known limitations
- **No OCR Support**: Scanned PDFs are explicitly rejected.
- **No Pure ASCII Tab Parsing**: ASCII tabs require an explicit MusicXML sidecar and an alignment file.
- **Grace Notes skipped**: Currently, 15 fret candidates in `private_input_1` are unused due to missing grace note support.
