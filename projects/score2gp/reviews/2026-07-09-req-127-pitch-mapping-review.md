# Req-127 Architecture Review Report

Date: 2026-07-09
Reviewer role: Reviewer
Task: Req-127 / Task 68/69
Governance PR: pending
Governance main SHA: pending

## Review Verdict

`approve architecture`

The proposed pitch mapping schema designed in [2026-07-09-req-127-pitch-mapping-schema.md](file:///home/tticom/work/score2gp-workspace/score2gp-agentops/projects/score2gp/reports/2026-07-09-req-127-pitch-mapping-schema.md) is mathematically sound, matches the existing repository coordinates in [pdf_staff_position_diagnostics.py](file:///home/tticom/work/score2gp-workspace/score2gp/src/score2gp/pdf_staff_position_diagnostics.py), and covers all requirements including Treble, Bass, and Alto clefs, and ledger lines.

## Plausibility Assessment

`well supported`

The lookup formulas and tables map the vertical `staff_step_index` directly to diatonic step offsets relative to Middle C (C4, MIDI 60). This provides a single unified equation:

$$d = C_{\text{clef}} - \text{step}$$

$$\text{midi}(d) = 60 + 12 \cdot (d \text{ div } 7) + \text{OFFSET}[d \pmod 7]$$

where $\text{OFFSET} = [0, 2, 4, 5, 7, 9, 11]$.

This handles positive, negative, even (line), and odd (space) indices correctly, and maps ledger lines above/below the staff up to at least 3 lines.

## Evidence Verified

- Reviewed [2026-07-09-req-127-pitch-mapping-schema.md](file:///home/tticom/work/score2gp-workspace/score2gp-agentops/projects/score2gp/reports/2026-07-09-req-127-pitch-mapping-schema.md).
- Verified compatibility with `staff_step_index` definition in [pdf_staff_position_diagnostics.py](file:///home/tticom/work/score2gp-workspace/score2gp/src/score2gp/pdf_staff_position_diagnostics.py).
- Confirmed lookup correctness for Middle C ($d=0$, MIDI 60) on Treble (ledger step 10), Bass (ledger step -2), and Alto (middle line step 4).

## Next Eligible Task Promotion

Since the pitch mapping schema is designed and approved, the next logical step is to implement this mapping inside `score2gp`. We define:
- **Task 70 — Implement clef-aware pitch mapping**: Implement the translation function inside `score2gp` (e.g. `src/score2gp/pdf_pitch_mapper.py` or within staff position diagnostics) and add focused tests.
- **Task 71 — Review clef-aware pitch mapping implementation**: Conformance review of the developer implementation.
