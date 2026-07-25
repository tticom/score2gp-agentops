# Architecture Decision Record: CR-04C Final-Event Duration Consistency for PDF-Only TabRaw Conversion

**Author**: Architect (`tticom-automation`)
**Date**: 2026-07-25
**Governance Repo**: `score2gp-agentops`
**Product Repo**: `score2gp`
**Product Base Commit**: `f47194e57b551d4b571a04c0b7641fbe9c173f80`
**Selected Decision Outcome**: **Outcome B — Alternative Developer Task (Option A: Grid-Sized Notes + Deterministic Rest Fill)**

---

## 1. Problem Statement & Evidenced Mismatch

During current-runtime evidence replay of `Lesson-5.pdf` and direct code inspection on product `main` (`f47194e5`), `build_ir_from_tabraw_only()` in [`src/score2gp/build_ir.py:L1834-L1835`](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/src/score2gp/build_ir.py#L1834-L1835) assigns `ev_duration_ticks = max(0, 3840 - current_onset)` to the final non-rest candidate subgroup in a bar.

An eighth note has a nominal duration of 480 ticks ($1 \times 480$). Assigning padded durations (e.g. 2400 ticks for $N=4$ or 2880 ticks for $N=3$) to an event labeled `"eighth"` creates an internal contradiction in `ScoreIR` between `duration_ticks` and `notated_duration`. The architecture decision is grounded strictly on this independently verified internal `ScoreIR` and `GPIF` contract contradiction. The proprietary Guitar Pro GUI application visual rendering behavior is reclassified as an unverified hypothesis.

---

## 2. Empirical Verification & Evidence Ledger

### Verified Repository Facts (Product Commit `f47194e57b551d4b571a04c0b7641fbe9c173f80`)

Running `build_ir_from_tabraw_only()` on synthetic TabRaw inputs with $N$ candidate subgroups in a 4/4 measure (3840 ticks) yields the following exact event timing outputs on `main`:

```text
N=1: Total events=1 | Event 0: onset=0, duration_ticks=3840, notated={'value': 'eighth', 'dots': 0} (Remainder R=3360)
N=3: Total events=3 | Event 2: onset=960, duration_ticks=2880, notated={'value': 'eighth', 'dots': 0} (Remainder R=2400)
N=4: Total events=4 | Event 3: onset=1440, duration_ticks=2400, notated={'value': 'eighth', 'dots': 0} (Remainder R=1920)
N=7: Total events=7 | Event 6: onset=2880, duration_ticks=960, notated={'value': 'eighth', 'dots': 0} (Remainder R=480)
```

In every case ($N < 8$), the final note receives the full remaining measure ticks as `duration_ticks` while retaining `notated_duration.value == 'eighth'`, contradicting the nominal tick duration of an eighth note (480 ticks).

### Verified GPIF Package Validation

Creating a `ScoreIR` object where every note receives `duration_ticks == grid_spacing` (480 ticks) and remaining measure capacity $R$ is decomposed into explicit un-dotted rest events (`is_rest=True`, `notes=[]`) passes `write_gp()`, `validate_gp()`, and `inspect_gp()` with 0 validation errors:

```text
GPIF Package Validation Result: errors=[]
Package Inspection Summary: bar_count=1, note_count=N, tempo=120
```

### Separation of Fact, Inference, and Unknown

- **Fact (Verified)**: Current `build_ir_from_tabraw_only()` pads the final candidate note's `duration_ticks` to fill measure capacity 3840 without updating `notated_duration`, creating an internal `ScoreIR` timing-label mismatch (`duration_ticks=2400` vs `notated_duration={"value": "eighth", "dots": 0}` = 480 nominal ticks).
- **Fact (Verified)**: `ScoreIR` models and `gpif.py` writer serialize `is_rest=True` events with standard `NotatedDuration` values (`whole`, `half`, `quarter`, `eighth`, `16th`, `32nd`, `64th`) without validation errors (`validate_gp()` returns 0 errors).
- **Inference**: Representing unassigned measure capacity as explicit rest events in `ScoreIR` resolves the internal timing-label mismatch and reflects silent measure space without implying un-evidenced note sustain.
- **Hypothesis**: The internal timing-label contradiction would cause external GUI notation applications to render a visual notation/timeline discrepancy.
- **Unknown**: Exact visual rendering behavior inside the proprietary Guitar Pro GUI application (unverified in headless terminal environment; decisions are strictly based on verified `ScoreIR` and `GPIF` XML contract compliance).
- **Unknown**: Whether future non-4/4 time signatures (e.g. 3/4 or 6/8) will require measure capacity parameters beyond 3840 ticks (out of scope for active 4/4 blocker).

---

## 3. Options Evaluated

| Option | Approach | ScoreIR & GPIF Validity | Truthfulness & Semantics | Decision |
| :--- | :--- | :--- | :--- | :--- |
| **Option A (Selected)** | Set final note duration to `grid_spacing` (matching `notated_duration`), and fill remaining measure capacity $R = 3840 - \text{current\_onset}$ with deterministic rest event(s) (`is_rest=True`). | Fully valid (`validate-ir` and `validate_gp` pass with 0 errors). | Truthful: notes reflect visual/grid duration (`eighth`), and unnotated measure tail reflects rest/silence. | **APPROVED** |
| **Option B** | Split final note into tied duration components (e.g. half note tied to eighth note). | Requires tie structure not present on TabRaw tab input without rhythm notation. | Un-evidenced: TabRaw input lacks rhythm beams or tie markers; creating artificial ties alters tab semantics. | REJECTED |
| **Option C** | Update `notated_duration` to match 2400 ticks. | Invalid: 2400 ticks (2.5 quarter beats) has no single un-tied `NotatedDuration` value in standard music notation. | Invalid notation representation. | REJECTED |
| **Option D** | Refuse input on 4-candidate bars. | Refuses valid drawn/vector tabs. | Unnecessarily restrictive. | REJECTED |

---

## 4. Deterministic Rest Decomposition Specification

To handle any remainder $R = 3840 - \text{current\_onset}$ after placing candidate note events (where each note receives `duration_ticks = grid_spacing`), $R$ MUST be greedily decomposed into un-dotted rest events in descending order of nominal duration:

### Standard Duration Hierarchy (Ticks)
1. `whole` = 3840 ticks
2. `half` = 1920 ticks
3. `quarter` = 960 ticks
4. `eighth` = 480 ticks
5. `16th` = 240 ticks
6. `32nd` = 120 ticks
7. `64th` = 60 ticks

### Decomposition Rules
- **Greedy Selection**: At each step, select the largest un-dotted duration $D$ whose tick value $T(D) \le R$.
- **Augmentation Dots**: All generated rest events MUST set `dots = 0` (un-dotted rests).
- **Rest ID Format**: Rests generated for bar `output_bar_idx` MUST be assigned sequential IDs matching `f"bar-{output_bar_idx}-rest-{seq_idx}"`, where `seq_idx` starts at 1 for the first rest in that bar.
- **Onset Continuity**: The first rest starts at `onset_ticks = current_onset`. Subsequent rests advance sequentially by $T(D)$.
- **Confidence & Notes**: Rest events MUST set `is_rest=True`, `notes=[]`, `confidence=1.0`.

### Complete Decomposition Table for All Reachable 4/4 Remainder Values

| Remainder $R$ (ticks) | Cause ($N$ eighth notes in 4/4) | Sequence of Rest Events (Value, Ticks, Onset) | Total Rest Count |
| :--- | :--- | :--- | :--- |
| **3360** | $N=1$ (onset 480) | 1. `half` (1920 ticks, onset 480)<br>2. `quarter` (960 ticks, onset 2400)<br>3. `eighth` (480 ticks, onset 3360) | 3 rests |
| **2880** | $N=2$ (onset 960) | 1. `half` (1920 ticks, onset 960)<br>2. `quarter` (960 ticks, onset 2880) | 2 rests |
| **2400** | $N=3$ (onset 1440) | 1. `half` (1920 ticks, onset 1440)<br>2. `eighth` (480 ticks, onset 3360) | 2 rests |
| **1920** | $N=4$ (onset 1920) | 1. `half` (1920 ticks, onset 1920) | 1 rest |
| **1440** | $N=5$ (onset 2400) | 1. `quarter` (960 ticks, onset 2400)<br>2. `eighth` (480 ticks, onset 3360) | 2 rests |
| **960** | $N=6$ (onset 2880) | 1. `quarter` (960 ticks, onset 2880) | 1 rest |
| **480** | $N=7$ (onset 3360) | 1. `eighth` (480 ticks, onset 3360) | 1 rest |
| **0** | $N=8$ (onset 3840) | None (measure capacity exactly filled) | 0 rests |

---

## 5. Over-Capacity Refusal Rule

If the accumulated candidate note onset span exceeds measure capacity ($\text{current\_onset} > 3840$ ticks) or if adding a candidate note event causes $\text{current\_onset} + \text{grid\_spacing} > 3840$ ticks (e.g. $N \ge 5$ quarter-grid candidates in `--editable-draft` mode where $5 \times 960 = 4800 > 3840$), `build_ir_from_tabraw_only()` MUST refuse the input by raising `BuildIrInputRiskError`:

```python
raise BuildIrInputRiskError(
    category="pdf_only_tab_measure_overcapacity",
    stage="measure-assembly",
    message=f"Candidate note events in bar {output_bar_idx} exceed measure capacity 3840 ticks (accumulated {current_onset + grid_spacing} ticks).",
    details={
        "bar_index": str(output_bar_idx),
        "accumulated_ticks": str(current_onset + grid_spacing),
        "measure_capacity": "3840",
    },
)
```

---

## 6. Developer Task Specification (Prompt 0011)

- **Authorized Role**: Developer (Tier B)
- **Authorized Product Branch**: `agy/cr04c-final-event-duration-consistency-implementation`
- **Expected Product Files**:
  - `src/score2gp/build_ir.py`
  - `tests/test_pdf_only_tab.py`
  - `tests/test_build_ir.py`
- **Mandatory Public Tests**:
  1. $N=4$ remainder test ($R=1920 \to 1$ `half` rest).
  2. Non-single-duration remainder test ($N=3$, $R=2400 \to 1$ `half` rest + 1 `eighth` rest).
  3. Non-single-duration remainder test ($N=1$, $R=3360 \to 1$ `half` rest + 1 `quarter` rest + 1 `eighth` rest).
  4. Over-capacity refusal test (5 quarter-grid candidates in `--editable-draft` mode $\implies$ raises `BuildIrInputRiskError`).
- **Validation Commands**:
  - `python -m pytest tests/test_pdf_only_tab.py tests/test_build_ir.py`
  - `python scripts/agent_verify.py`
  - `python -m pytest`
  - `python scripts/artifact_audit.py`
