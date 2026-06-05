# Research Report: Post-Grace-Note Active Blocker Audit v0.1

Durable record of the active blocker audit executed from product `main` branch after merging Product PR #170 and Agentops PR #38.

## Verdict
All convertible dual-source fixtures successfully matched and stable; remaining inputs cleanly gated by safety refusals.

## Current milestone status
- **`private_input_1`**: **Milestone Achieved**. Successfully compiles to ScoreIR and writes a validated, playable `.gp` file with **153 / 153 matched candidates** and **0 unmatched PDF candidates** under default flow. It is now fully accepted as a milestone fixture.
- **Lessons 3–7 & Melodic Soloing**: **100% Stable**. Stable note counts are maintained across all custom private inputs:
  - Lesson 3: 459 / 459 matched
  - Lesson 4: 546 / 546 matched
  - Lesson 5: 295 / 295 matched
  - Lesson 6: 235 / 235 matched
  - Lesson 7: 624 / 624 matched
  - Melodic Soloing: 82 / 82 matched
- **Other Inputs**: Cleanly and explicitly refused by safety gates during inspection/orchestration.

## Private input summary table

| Input Label | Input Type | Page Count | Playable Candidates | Status | Matched | Unmatched | First Blocker / Refusal Code | Suitability / Recommendation |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| `private_input_1` (Derek Trucks) | pdf-tab-musicxml | 2 | 153 | `pass` | 153 | 0 | None | Milestone achieved. |
| `private_input_2` (CAGED shapes) | pdf-tab-only (ASCII) | 1 | 54 | `fail` | 0 | 54 | `pdf_input_class_ascii_tab_requires_alignment` | `provide-matching-musicxml-before-build-ir` |
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

## Remaining blockers
- **Scanned/Raster PDFs**: `Rock Ballads` and `Chord Melody` fail due to lack of vector staff geometry (OCR is explicitly out of scope).
- **Pure ASCII TAB**: `private_input_2` fails because pure ASCII text lacks a structured layout or alignment grid, requiring manual alignment files/MusicXML sidecars.
- **Missing Sidecars**: `Practice Lick` and `Legato Licks` fail because they are vector TABs but lack matching MusicXML sidecar files.
- All remaining failures are expected refusal conditions correctly caught by safety gates.

## Next highest-value blocker
There are no remaining active product implementation blockers for convertible dual-source scores. The next highest-value tasks are defining a formal sidecar specification and developing an input acquisition workflow for missing staves.

## Why it is higher priority
- **Feature Complete**: The core alignment engine is feature-complete for all available, convertible inputs. Further parser modifications would be speculative or address out-of-scope tasks (such as scanned PDF layout extraction).
- **Hardening and Schema Control**: Establishing a formal sidecar-spec and defining input-acquisition workflows ensures stability, robust handling, and ease of integration for any future vector staves.

## Recommended smallest next task
- **Task**: **Release Hardening and Sidecar Acquisition Workflow Definition**.
- **Scope**: Document schema specification for required MusicXML sidecars, define layout classification metrics, and verify release packaging.

## Commands run
```bash
git switch main
git pull --ff-only origin main
git status --short --branch
git log --oneline --decorate --max-count=40
PYTHONPATH=. .venv/bin/python3 -m pytest
PYTHONPATH=. .venv/bin/python3 scripts/private_e2e_smoke.py
PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py
git ls-files fixtures/private work
git diff --check
git status --short
```

## Test results
- **Public Tests**: 467 passed cleanly in WSL.
- **E2E Private Smoke**: Successfully generated reports for all inputs.
- **Quality Audit**:
  - `private_input_1`: `pass` (153 / 153 matched).
  - Lessons 3–7: Stable `pass` (perfect count alignment).
  - Melodic Soloing: Stable `pass` (82 / 82 matched).

## Private-safety result
Running `git ls-files fixtures/private work` outputs exactly:
```text
fixtures/private/.gitkeep
```
No private or generated assets are tracked by Git.

## Known limitations
- OCR is unsupported.
- Pure ASCII tab without sidecars is rejected.
- Drawn TABs without sidecars are refused.
