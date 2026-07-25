# Candidate Task: TabRaw Final Event Duration Padding and Notated Label Consistency

## Status

AUTHORIZED FOR IMPLEMENTATION BY PROMPT 0011 (ARCHITECTURE RESOLVED)

## Evidenced Code Injection Point

- **File & Function**: `src/score2gp/build_ir.py` in `build_ir_from_tabraw_only()` ([lines 1834-1835](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/src/score2gp/build_ir.py#L1834-L1835)).
- **Mechanism**: For a non-rest final subgroup, `ev_duration_ticks` was assigned `max(0, 3840 - current_onset)`, while `ev_duration_name` remained the grid-derived `"eighth"` for candidate count $N \le 8$.
- **Observed Mismatch**: With $N=4$ candidates in Bar 0 and `current_onset=1440`, `ev_duration_ticks` was calculated as $3840 - 1440 = 2400$ ticks, while `notated_duration` remained `{'value': 'eighth', 'dots': 0}`.

## Architecture Verdict (CR-04C)

- **Selected Option**: Option A (Grid-Sized Notes + Deterministic Rest Fill for Remaining Capacity).
- **ADR Document**: [`projects/score2gp/research/2026-07-25-cr04c-final-event-duration-architecture-decision.md`](../research/2026-07-25-cr04c-final-event-duration-architecture-decision.md)
- **Rule**: Every note event receives `duration_ticks = grid_spacing` and `notated_duration = NotatedDuration(value=duration_name, dots=0)`. Any remaining measure capacity $R = 3840 - \text{current\_onset}$ is greedily decomposed into un-dotted rest events (`is_rest=True`, `notes=[]`, `dots=0`, `id=f"bar-{bar_idx}-rest-{seq_idx}"`) in descending order of nominal duration (`whole` 3840, `half` 1920, `quarter` 960, `eighth` 480, `16th` 240, `32nd` 120, `64th` 60). Over-capacity candidate note onsets exceeding 3840 ticks raise `BuildIrInputRiskError(category="pdf_only_tab_measure_overcapacity")`.

## Public-Testable Generic Rule

For any TabRaw bar converted via `build_ir_from_tabraw_only()`:
1. Candidate note events receive `duration_ticks = grid_spacing` matching `notated_duration`.
2. Accumulated note onsets exceeding 3840 ticks raise `BuildIrInputRiskError`.
3. Remainder $R = 3840 - \text{current\_onset}$ is greedily decomposed into un-dotted rest events (`is_rest=True`).

## Measurable Success & Refusal Criteria

- **Success**: In emitted `score.ir.json`, no event carries `notated_duration.value == 'eighth'` (480 ticks) alongside `duration_ticks == 2400`. Every event satisfies `duration_ticks == nominal_ticks(notated_duration)`. Total measure duration equals 3840 ticks ($C_{\text{measure}}$). `score2gp validate-ir` and `validate_gp` succeed with 0 errors.
- **Refusal**: Supplying candidates whose total onset span exceeds measure capacity ($current\_onset + grid\_spacing > 3840$) raises `BuildIrInputRiskError(category="pdf_only_tab_measure_overcapacity")`.

## Scope & Validation

- **Maximum Scope**: Final event duration calculation loop in `build_ir_from_tabraw_only()` (`src/score2gp/build_ir.py` lines 1827-1845).
- **Validation Command**: `pytest tests/test_pdf_only_tab.py tests/test_build_ir.py`
- **Authorized Developer Prompt**: `projects/score2gp/prompts/next/0011-cr04c-final-event-duration-consistency-implementation.md`
