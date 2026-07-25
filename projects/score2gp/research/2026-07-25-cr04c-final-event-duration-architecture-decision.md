# Architecture Decision Record: CR-04C Final-Event Duration Consistency for PDF-Only TabRaw Conversion

**Author**: Architect (`tticom-automation`)  
**Date**: 2026-07-25  
**Governance Repo**: `score2gp-agentops`  
**Product Repo**: `score2gp`  
**Product Base Commit**: `f47194e57b551d4b571a04c0b7641fbe9c173f80`  
**Selected Decision Outcome**: **Outcome B — Alternative Developer Task (Option A: Grid-Sized Notes + Rest Fill)**  

---

## 1. Problem Statement & Evidenced Mismatch

During current-runtime evidence replay of `Lesson-5.pdf` and direct code inspection on product `main` (`f47194e5`), `build_ir_from_tabraw_only()` in [`src/score2gp/build_ir.py:L1834-L1835`](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/src/score2gp/build_ir.py#L1834-L1835) assigns `ev_duration_ticks = max(0, 3840 - current_onset)` to the final non-rest candidate subgroup in a bar.

For Bar 0 of `Lesson-5.pdf` (which contains $N=4$ candidates with onsets $0, 480, 960, 1440$ ticks):
- Events 0, 1, 2 receive `duration_ticks = 480` and `notated_duration = NotatedDuration(value="eighth", dots=0)`.
- Event 3 receives `duration_ticks = max(0, 3840 - 1440) = 2400` ticks while retaining `notated_duration = NotatedDuration(value="eighth", dots=0)`.

An eighth note has a nominal duration of 480 ticks ($1 \times 480$). Assigning 2400 ticks (2.5 quarter beats) to an event labeled `"eighth"` creates an internal contradiction in `ScoreIR` and causes GPIF XML output to render a visual eighth note followed by a 1920-tick timeline gap before the next measure.

---

## 2. Options Evaluated

| Option | Approach | ScoreIR & GPIF Validity | Truthfulness & Semantics | Decision |
| :--- | :--- | :--- | :--- | :--- |
| **Option A (Selected)** | Set final note duration to `grid_spacing` (matching `notated_duration`), and fill remaining measure capacity $R = 3840 - \text{current\_onset}$ with rest event(s) (`is_rest=True`). | Fully valid (`validate-ir` and `validate_gp` pass). | Truthful: notes reflect visual/grid duration (`eighth`), and unnotated measure tail reflects rest/silence. | **APPROVED** |
| **Option B** | Split final note into tied duration components (e.g. half note tied to eighth note). | Requires tie structure not present on TabRaw tab input without rhythm notation. | Un-evidenced: TabRaw input lacks rhythm beams or tie markers; creating artificial ties alters tab semantics. | REJECTED |
| **Option C** | Update `notated_duration` to match 2400 ticks. | Invalid: 2400 ticks (2.5 quarter beats) has no single un-tied `NotatedDuration` value in standard music notation. | Invalid notation representation. | REJECTED |
| **Option D** | Refuse input on 4-candidate bars. | Refuses valid drawn/vector tabs. | Unnecessarily restrictive. | REJECTED |

---

## 3. Invariants & Architectural Rules

1. **Tick-Label Invariant**: For every non-tied note event in `ScoreIR`, `duration_ticks` MUST equal the exact tick value of its `notated_duration` (with augmentation dots):
   - Whole = 3840 ticks
   - Half = 1920 ticks
   - Quarter = 960 ticks
   - Eighth = 480 ticks
   - 16th = 240 ticks
   - 32nd = 120 ticks
   - 64th = 60 ticks
2. **Measure Capacity Invariant**: The sum of `duration_ticks` across all events (notes + rests) in a bar MUST equal measure capacity ($C_{\text{measure}} = 3840$ ticks for 4/4 time signature).
3. **Rest Fill Representation**: Any unnotated measure capacity after the final candidate note event MUST be filled by appending rest event(s) (`is_rest=True`, `notes=[]`) with `duration_ticks` equal to the remaining capacity and a matching valid `notated_duration` (e.g. 1920 ticks $\to$ `NotatedDuration(value="half", dots=0)`).

---

## 4. Developer Task Specification (Prompt 0011)

- **Authorized Role**: Developer (Tier B)
- **Authorized Product Branch**: `agy/cr04c-final-event-duration-consistency-implementation`
- **Expected Product Files**:
  - `src/score2gp/build_ir.py`
  - `tests/test_pdf_only_tab.py`
  - `tests/test_build_ir.py`
- **Validation Commands**:
  - `python -m pytest tests/test_pdf_only_tab.py tests/test_build_ir.py`
  - `python scripts/agent_verify.py`
  - `python -m pytest`
  - `python scripts/artifact_audit.py`
