# Candidate Task: TabRaw Final Event Duration Padding and Notated Label Consistency

## Status

CANDIDATE (NON-EXECUTABLE / AWAITING GOVERNANCE AUTHORIZATION)

## Evidenced Code Injection Point

- **File & Function**: `src/score2gp/build_ir.py` in `build_ir_from_tabraw_only()` ([lines 1834-1835](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/src/score2gp/build_ir.py#L1834-L1835)).
- **Mechanism**: For a non-rest final subgroup, `ev_duration_ticks` is assigned `max(0, 3840 - current_onset)`, while `ev_duration_name` remains the grid-derived `"eighth"` for candidate count $N \le 8$.
- **Observed Mismatch**: With $N=4$ candidates in Bar 0 and `current_onset=1440`, `ev_duration_ticks` is calculated as $3840 - 1440 = 2400$ ticks, while `notated_duration` remains `{'value': 'eighth', 'dots': 0}`.

## Claim Under Test

Final event duration fill logic in `build_ir_from_tabraw_only()` can align `notated_duration` with `duration_ticks` (or split padded duration into tied/notated duration components) rather than labeling a 2400-tick event as `"eighth"`.

## Public-Testable Generic Rule

For any TabRaw event where `duration_ticks` is padded to fill measure capacity (e.g. 2400 ticks), `notated_duration` must match the actual notated duration value corresponding to `duration_ticks` or be structured into valid notated duration components.

## Measurable Success & Refusal Criteria

- **Success**: In emitted `score.ir.json`, no event carries `notated_duration.value == 'eighth'` (480 ticks) alongside `duration_ticks == 2400`. `score2gp validate-ir` succeeds.
- **Refusal**: Supplying candidates whose total onset exceeds measure capacity ($current\_onset > 3840$) raises `BuildIrInputRiskError`.

## Scope & Validation

- **Maximum Scope**: Final event duration calculation loop in `build_ir_from_tabraw_only()` (`src/score2gp/build_ir.py` lines 1827-1836).
- **Validation Command**: `pytest tests/test_build_ir.py`
- **Stop / Pivot Criteria**: If measure fill rules alter existing passing TabRaw regression tests without explicit maintainer policy, stop and return to governance. Product code implementation remains disauthorized under this candidate record.
