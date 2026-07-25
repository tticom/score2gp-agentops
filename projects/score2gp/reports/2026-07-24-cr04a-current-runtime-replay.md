# CR-04A Current-Runtime Lesson-5 Evidence Replay Report

**Authorised Role**: Architect (Evidence Collection)  
**Governance Repository**: `score2gp-agentops`  
**Product Repository**: `score2gp`  
**Product Base Commit**: `ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f` (contains `ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f`)  
**Date**: 2026-07-25  
**Verdict**: `DEFECT_NOT_REPRODUCED`  

---

## 1. Executive Summary

This report records the bounded current-runtime evidence replay for **CR-04A** (`Lesson-5.pdf`) on product `origin/main` (`ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f`).

Historical evidence ledger `2026-07-17-first-divergence-evidence-ledger.json` previously recorded a false **half rest** (1920 ticks) inflating measure duration to 5760 ticks and causing a 12/8 meter misclassification.

Empirical replay on current product `main` establishes that:
1. **Candidate Recognition**: Emits **0** `half_rest_candidate` objects, **0** `half_rest` objects, and **0** 1920-tick rest candidates across all 14 systems in `Lesson-5.pdf`.
2. **Notation Bridge**: `build_ir_from_notation_outcomes()` in `score2gp.notation_bridge` ignores/filters half-rest candidates, accepting only whole/half/quarter/eighth/sixteenth/32nd/64th note candidates and `quarter_rest_candidate`.
3. **Generated ScoreIR**: Contains **0** rest events across all 34 bars. Bar 0 emits 4 note events (TabRaw fret extractions) with time signature `4/4` and 0 rest duration.
4. **Decision Gate**: **`DEFECT_NOT_REPRODUCED`**. The false 1920-tick half rest does not exist on current product `main`. Implementing obsolete half-rest suppression is disauthorized.

---

## 2. Runtime Provenance

- **Product Commit (HEAD)**: `ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f`
- **Product Working Tree Status**: Clean (`git status --short` output empty)
- **Executable Location**: `/home/tticom/work/score2gp-workspace/score2gp/.venv/bin/score2gp`
- **Resolved Module Path**: `/home/tticom/work/score2gp-workspace/score2gp/src/score2gp/__init__.py`
- **Private Input Path**: `/home/tticom/work/score2gp-workspace/score2gp-private-fixtures/fixtures/private/Lesson-5.pdf`
- **Private Input SHA-256**: `585ac4669a85e44d29ab571620544ca860a907221b625e28074c0cccf4447654`
- **MusicXML Sidecar Path**: `absent` (none used)
- **Diagnostic Commands & Exit Statuses**:
  - `score2gp note-candidate-recognition --pdf <Lesson-5.pdf> --json` -> Exit status `0`
  - `score2gp convert --pdf <Lesson-5.pdf> --pdf-only-tab --work-dir work/lesson5_work -o work/lesson5_out.gp --json-report work/lesson5_report.json` -> Exit status `0`

---

## 3. Current-Runtime Evidence Collection

### Question 1: Does current recognition emit any `half_rest_candidate`, `half_rest`, or 1920-tick rest?
- **Observed Fact**: No. In `work/lesson5_note_candidates.json`:
  - `read_only_recognition_outcomes` contains 0 rest candidates (unique symbol types: `quarter_note_candidate`, `flag_candidate`, `left_margin_candidate`, `sixty_fourth_note_candidate`, `x_aligned_cluster_candidate`, `thirty_second_note_candidate`, `eighth_note_candidate`, `ledger_line_candidate`, `treble_clef_candidate`, `sixteenth_note_candidate`, `beam_candidate`).
  - `semantic_candidates` contains 0 half rests for System 1 / Measure 1 (`half_rests: []`) and 0 half rests across all 14 systems on Page 1-3.

### Question 2: Does the current notation bridge accept or reject half-rest outcomes?
- **Observed Fact**: `build_ir_from_notation_outcomes()` in `score2gp.notation_bridge` filters outcomes against an explicit candidate list:
  ```python
  if sym_type not in [
      "whole_note_candidate", "half_note_candidate", "quarter_note_candidate",
      "eighth_note_candidate", "sixteenth_note_candidate", "thirty_second_note_candidate",
      "sixty_fourth_note_candidate", "quarter_rest_candidate"
  ]:
      continue
  ```
  Any `half_rest_candidate` or `half_rest` outcome is skipped (`continue`) and never passes into `ScoreIR`.

### Question 3: Does generated ScoreIR, MusicXML, or GPIF contain a half rest in the first affected measure?
- **Observed Fact**: No. In `work/lesson5_work/score.ir.json`:
  - Total bars: 34.
  - Total rests across all bars in `ScoreIR`: 0.
  - Bar 0 events count: 4 events (containing TabRaw note fret extractions, e.g., fret 8 on string 5), with 0 rest events.

### Question 4: What meter and per-voice durations are emitted?
- **Observed Fact**:
  - Time signature emitted for Bar 0 and all 34 bars: `4/4` (`{'numerator': 4, 'denominator': 4}`).
  - Total rest duration emitted for Bar 0: 0 ticks.

### Question 5: At what earliest current stage does observed output first differ from the approved source facts?
- **Observed Fact**:
  - Historical ledger recorded a 12/8 detected meter with a 1920-tick false half rest in measure 1 under an older code version.
  - On current `origin/main` (`ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f`), candidate recognition emits 0 half rests, `notation_bridge` skips half rests, and TabRaw conversion emits 4/4 meter with 34 bars.

---

## 4. Historical Ledger vs Current Evidence Comparison

| Dimension | Historical Evidence Ledger (2026-07-17) | Current Runtime Observation (`ff9fb48`) |
| :--- | :--- | :--- |
| **False Rest Defect** | Half rest (1920 ticks) in measure 1 | None (0 rest events emitted) |
| **Detected Meter** | 12/8 (inflated measure duration 5760 ticks) | 4/4 (34 bars emitted) |
| **Notation Bridge Gate** | Accepted historical half rest | Filters out `half_rest_candidate` / `half_rest` |
| **ScoreIR Rest Count** | 1 rest in measure 1 (1920 ticks) | 0 rest events in total |

---

## 5. Decision Gate & Governed Next State

- **Selected Outcome**: **`DEFECT_NOT_REPRODUCED`**
- **Justification**: The false 1920-tick half rest is completely absent on current product `main`. Implementing obsolete half-rest suppression is disauthorized under Architect skill rules.
- **Product Code Authorization**: **NO PRODUCT CODE CHANGES AUTHORISED**.
- **Next Governed Step**: Publish this evidence report, synchronize governance state (`ACTIVE_TASK.md` and `prompts/NEXT.md`), and open a governance PR for Codex review.
