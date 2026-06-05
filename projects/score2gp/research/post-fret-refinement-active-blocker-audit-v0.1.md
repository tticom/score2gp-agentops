# Research Report: Post-Fret-Refinement Active Blocker Audit v0.1

Durable record of the active blocker audit executed from product `main` branch after merging PR #168 and agentops PR #33.

## Verdict
`private_input_1 milestone achieved`

---

## Evidence
- **Product Repository**: `tticom/score2gp`
- **Product Branch**: `main`
- **Product Commit Hash**: `ef3a397c5650b0ac2c5bf6ff8d49a39910b4002e`
- **Governance Repository**: `tticom/score2gp-agentops`
- **Governance Branch**: `research/post-fret-refinement-active-blocker-audit-v0.1`
- **Governance Commit Hash**: `f8239143b0795aa1ccc4142e6b8f8a251f8b8c07` (prior to committing this report)
- **Commands Run**:
  - `PYTHONPATH=. .venv/bin/pytest`
  - `PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py`
  - `PYTHONPATH=. .venv/bin/python3 scripts/private_e2e_smoke.py`
  - `git ls-files fixtures/private work`
  - `git diff --check`
- **Public Test Result**: `463 passed`
- **Private Smoke Result**: Successfully generated summary reports.
- **Private Quality Audit Result**: Verified stable matched notes for all passing inputs.
- **Private-Safety Output**: `fixtures/private/.gitkeep` (verified clean)
- **Working Tree Status**: Clean (no uncommitted files in the product repository)

---

## Private Input Summary Table

| Input Label | Stage Reached | Status | Quality Category | Matched | Unmatched | ScoreIR Notes | GPIF Notes | First Blocker | Generated GP | Interpretation |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :--- | :---: | :--- |
| `private_input_1` | GPIF Serialization | `pass` | `gp_output_technique_loss_expected` | 137 | 16 | 137 | 137 | None | Yes | Milestone achieved. Successfully compiles under default flow. |
| `private_input_2` | PDF Grouping | `fail` | `gp_output_empty_or_near_empty` | 0 | 54 | 0 | 0 | `provide-matching-musicxml-before-build-ir` | No | blocked. ASCII-tab input class lacks MusicXML sidecar. |
| `private_input_custom` (Rock Ballads) | PDF Grouping | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 | 0 | `provide-matching-musicxml-before-build-ir` | No | blocked. Multi-page commercial PDF lacks MusicXML sidecar. |
| `private_input_custom` (Chord Melody) | PDF Grouping | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 | 0 | `provide-matching-musicxml-before-build-ir` | No | blocked. Multi-page commercial PDF lacks MusicXML sidecar. |
| `private_input_custom` (Practice Lick) | PDF Grouping | `fail` | `gp_output_empty_or_near_empty` | 0 | 61 | 0 | 0 | `provide-matching-musicxml-before-build-ir` | No | blocked. Hand-drawn geometry PDF lacks MusicXML sidecar. |
| `private_input_custom` (Legato Licks) | PDF Grouping | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 | 0 | `provide-matching-musicxml-before-build-ir` | No | blocked. Drawn TAB without systems lacks MusicXML sidecar. |
| `private_input_custom_lesson_3` | GPIF Serialization | `pass` | `gp_output_technique_loss_expected` | 459 | 2 | 459 | 459 | None | Yes | Stable. |
| `private_input_custom_lesson_4` | GPIF Serialization | `pass` | `gp_output_technique_loss_expected` | 546 | 3 | 546 | 546 | None | Yes | Stable. |
| `private_input_custom_lesson_5` | GPIF Serialization | `pass` | `gp_output_technique_loss_expected` | 295 | 2</td> 295 | 295 | None | Yes | Stable. |
| `private_input_custom_lesson_6` | GPIF Serialization | `pass` | `gp_output_technique_loss_expected` | 235 | 3 | 235 | 235 | None | Yes | Stable. |
| `private_input_custom_lesson_7` | GPIF Serialization | `pass` | `gp_output_technique_loss_expected` | 624 | 0 | 624 | 624 | None | Yes | Stable. |
| `private_input_custom_melodic_soloing` | GPIF Serialization | `pass` | `gp_output_technique_loss_expected` | 82 | 0 | 82 | 82 | None | Yes | Stable. |

---

## `private_input_1` Residual Analysis

| Metric / Category | Value |
| :--- | :--- |
| Matched Candidates | 137 |
| Unmatched Candidates | 16 |
| ScoreIR Notes | 137 |
| GPIF Notes | 137 |
| Fatal Warnings | 0 |
| Non-fatal Warnings | 3,937 (mostly `unsupported-grace-note` and `musicxml-backup-encountered`) |
| Quality Category | `gp_output_technique_loss_expected` |

### Classification of the 16 Unmatched Candidates:
- **Expected loss / acceptable warning (skipped grace notes)**: 15
  - Since grace notes are explicitly skipped by the current MusicXML parser phase (`musicxml-grace-skipped`), the corresponding fret digits extracted from the PDF cannot be aligned, resulting in them being marked as `tab-candidate-unused`.
- **Unknown / other**: 1
  - Slight layout/pitch alignment mismatch in a complex bar.

---

## Architecture Recommendation

### Recommended Next Task:
- **Branch Name**: `task/layout-class-and-sidecar-refinement-v0.1`
- **Role Assignment**: Developer / Researcher
- **Likely Affected Files/Modules**: `src/score2gp/pdf.py`, `src/score2gp/tabraw.py`
- **Goal**: Implement explicit layout classification and missing-sidecar safety gates during the inspection stage to cleanly refuse and classify inputs lacking MusicXML or having unsupported layouts (ASCII/scanned) with specific reason codes rather than generic grouping failures.
- **Non-goals**:
  - Do not write a new ASCII tab parser.
  - Do not implement OCR for scanned PDFs.
  - Do not change timing/MusicXML core modules.
- **Implementation Approach**:
  - Add classification checks in `inspect_pdf` to identify whether the input class is ASCII or drawn TAB without barlines.
  - Raise a specific, clean refusal code (such as `pdf_input_class_ascii_tab_requires_alignment` or `pdf_input_class_drawn_tab_requires_barlines`) directly during the inspection pass.
- **Tests Required**: Add unit tests in `tests/test_pdf.py` for the new classification refusal codes.
- **Validation Commands**:
  - `PYTHONPATH=. .venv/bin/pytest`
  - `PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py`
- **Acceptance Criteria**:
  - `private_input_2` and other custom `pdf-tab-only` files cleanly report specific classification failures.
  - Lessons 3–7, Melodic Soloing, and `private_input_1` remain stable.
- **Stop Conditions**:
  - Any public tests fail.
  - Private safety invariant is violated.
- **Reporting Format**: Standard verdict and evidence summary.
