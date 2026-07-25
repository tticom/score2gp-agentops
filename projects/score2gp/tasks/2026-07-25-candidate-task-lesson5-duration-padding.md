# Candidate Task: TabRaw Final Event Duration Padding and Notated Label Consistency

## Status

AUTHORIZED FOR IMPLEMENTATION BY PROMPT 0011 (ARCHITECTURE RESOLVED)

## Evidenced Code Injection Point

- **File & Function**: `src/score2gp/build_ir.py` in `build_ir_from_tabraw_only()` ([lines 1834-1835](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/src/score2gp/build_ir.py#L1834-L1835)).
- **Mechanism**: For a non-rest final subgroup, `ev_duration_ticks` was assigned `max(0, 3840 - current_onset)`, while `ev_duration_name` remained the grid-derived `"eighth"` for candidate count $N \le 8$.
- **Observed Mismatch**: With $N=4$ candidates in Bar 0 and `current_onset=1440`, `ev_duration_ticks` was calculated as $3840 - 1440 = 2400$ ticks, while `notated_duration` remained `{'value': 'eighth', 'dots': 0}`.

## Architecture Verdict (CR-04C)

- **Selected Option**: Option A (Grid-Sized Notes + Rest Fill for Remaining Capacity).
- **ADR Document**: [`projects/score2gp/research/2026-07-25-cr04c-final-event-duration-architecture-decision.md`](../research/2026-07-25-cr04c-final-event-duration-architecture-decision.md)
- **Rule**: Every note event receives `duration_ticks = grid_spacing` and `notated_duration = NotatedDuration(value=duration_name, dots=0)`. Any remaining measure capacity $R = 3840 - \text{current\_onset}$ is filled by appending rest event(s) (`is_rest=True`, `notes=[]`) with `duration_ticks = R` and a matching valid `notated_duration`.

## Public-Testable Generic Rule

For any TabRaw event where `current_onset < 3840` after adding all candidate note subgroups, final note duration is set to `grid_spacing` matching `notated_duration`, and remaining measure capacity $R$ is filled by rest event(s) (`is_rest=True`).

## Measurable Success & Refusal Criteria

- **Success**: In emitted `score.ir.json`, no event carries `notated_duration.value == 'eighth'` (480 ticks) alongside `duration_ticks == 2400`. Every event satisfies `duration_ticks == nominal_ticks(notated_duration)`. Measure capacity total equals 3840 ticks. `score2gp validate-ir` and `validate_gp` succeed.
- **Refusal**: Supplying candidates whose total onset exceeds measure capacity ($current\_onset > 3840$) raises `BuildIrInputRiskError`.

## Scope & Validation

- **Maximum Scope**: Final event duration calculation loop in `build_ir_from_tabraw_only()` (`src/score2gp/build_ir.py` lines 1827-1845).
- **Validation Command**: `pytest tests/test_pdf_only_tab.py tests/test_build_ir.py`
- **Authorized Developer Prompt**: `projects/score2gp/prompts/next/0011-cr04c-final-event-duration-consistency-implementation.md`
