# Candidate Task: Lesson-5 Event Duration Padding Anomaly (2400 Ticks)

## Status

CANDIDATE (NON-EXECUTABLE / AWAITING AUTHORIZATION)

## Objective

Investigate and locate the exact pipeline stage where the 4th Voice 1 event in Bar 0 (`onset_ticks=1440`, notes `['string=4,fret=9', 'string=5,fret=8']`) is assigned `duration_ticks=2400` while carrying internal label `notated_duration={'value': 'eighth', 'dots': 0}` during `Lesson-5.pdf` TabRaw conversion (`--pdf-only-tab`).

## Context & Observed Facts

- **Emitted Voice 1 Bar 0 Events**:
  - Event 0: `onset=0`, `duration_ticks=480`, `notated_duration={'value': 'eighth'}`
  - Event 1: `onset=480`, `duration_ticks=480`, `notated_duration={'value': 'eighth'}`
  - Event 2: `onset=960`, `duration_ticks=480`, `notated_duration={'value': 'eighth'}`
  - Event 3: `onset=1440`, `duration_ticks=2400`, `notated_duration={'value': 'eighth'}`
- **Total Voice 1 Duration**: 3840 ticks ($D_{\text{voice1}} = 3840$). Measure capacity $C_{\text{measure}} = 3840$ ticks in 4/4 meter.
- **Anomaly**: Event 3 is assigned 2400 ticks to fill the measure capacity while remaining labeled as an eighth note (`value: eighth` = 480 ticks).
- **Discovered During**: CR-04A current-runtime evidence replay on product base `ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f`.

## Scope & Boundaries

- **No Product Code Authorized**: This is a candidate task record only. No developer implementation or product code modification is authorized.
- **Investigation Boundary**: When authorized, trace TabRaw rhythm alignment and measure duration fill logic in `pdf_staff_tab_timing_aligner.py` and `build_ir.py` to identify why duration padding assigns 2400 ticks to an eighth note.
