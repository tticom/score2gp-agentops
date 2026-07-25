# Candidate Task: TabRaw Default Tempo Handling vs Source Tempo

## Status

CANDIDATE (NON-EXECUTABLE / AWAITING GOVERNANCE AUTHORIZATION)

## Evidenced Code Injection Point

- **File & Function**: `src/score2gp/build_ir.py` in `build_ir_from_tabraw_only()` ([line 1629](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/src/score2gp/build_ir.py#L1629)).
- **Mechanism**: Declares `tempo_bpm: float = 120.0` default parameter and constructs `Tempo(bpm=tempo_bpm)`.
- **Observed Mismatch**: Historical evidence ledger `source_facts` records `expected_tempo: 70` BPM, whereas TabRaw conversion (`--pdf-only-tab`) defaults to 120.0 BPM.

## Claim Under Test

`build_ir_from_tabraw_only()` can accept an explicit source-extracted or CLI-passed tempo parameter (e.g., `70.0`) rather than unconditionally defaulting to 120.0 BPM.

## Public-Testable Generic Rule

When an explicit valid tempo parameter `T` (e.g. 70.0 BPM) is supplied to `build_ir_from_tabraw_only()`, `ScoreIR` emits `Tempo(bpm=T)`. When omitted, it defaults to 120.0 BPM.

## Measurable Success & Refusal Criteria

- **Success**: `build_ir_from_tabraw_only(..., tempo_bpm=70.0)` emits `ir.tempo.bpm == 70.0` in `score.ir.json`.
- **Refusal**: Supplying non-positive tempo values (`bpm <= 0`) raises `BuildIrInputRiskError`.

## Scope & Validation

- **Maximum Scope**: `build_ir_from_tabraw_only()` signature in `src/score2gp/build_ir.py` and CLI parameter forwarding in `src/score2gp/cli.py`.
- **Validation Command**: `pytest tests/test_build_ir.py`
- **Stop / Pivot Criteria**: If tempo extraction from vector/raster text requires OMR model changes or unapproved heuristic heuristics, stop and return to governance. Product code implementation remains disauthorized under this candidate record.
