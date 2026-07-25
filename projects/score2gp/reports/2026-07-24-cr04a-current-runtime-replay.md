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
3. **Generated ScoreIR**: Contains **0** rest events across all 34 bars. Bar 0 emits 4 Voice 1 note events (`[480, 480, 480, 2400]` ticks, total $D_{\text{voice1}} = 3840$ ticks) with time signature `4/4`.
4. **Decision Gate**: **`DEFECT_NOT_REPRODUCED`**. The false 1920-tick half rest does not exist on current product `main`. Implementing obsolete half-rest suppression is disauthorized. Separate non-executable candidate task records have been created for the two currently evidenced product mismatches.

---

## 2. Runtime Provenance & Identity Remediation

- **Product Commit (HEAD)**: `ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f`
- **Product Working Tree Status**: Clean (`git status --short` output empty)
- **Executable Location**: `/home/tticom/work/score2gp-workspace/score2gp/.venv/bin/score2gp`
- **Resolved Module Path**: `/home/tticom/work/score2gp-workspace/score2gp/src/score2gp/__init__.py`
- **Private Input Path**: `/home/tticom/work/score2gp-workspace/score2gp-private-fixtures/fixtures/private/Lesson-5.pdf`
- **Private Input SHA-256**: `585ac4669a85e44d29ab571620544ca860a907221b625e28074c0cccf4447654`
- **MusicXML Sidecar Path**: `absent` (none used)
- **GitHub CLI Account**: `tticom-automation`
- **Git Identity Remediation**: Governance commits `359a369d` and `026485d8` were authored while local repository git config overrode the global user identity to `tticom-codex`. Local repository configuration was corrected to `user.name "tticom-automation"` (`tticomautomation@gmail.com`) for commit `b8ef490a` and all subsequent commits without force-pushing, preserving non-destructive audit history. Commits `359a369d` and `026485d8` remain in history as un-amended audit records; the identity gate is verified for remote head `b8ef490a` and subsequent commits.
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
- **Observed Fact (`supported`)**: `build_ir_from_notation_outcomes()` in `score2gp.notation_bridge` filters outcomes against an explicit candidate list:
  ```python
  if sym_type not in [
      "whole_note_candidate", "half_note_candidate", "quarter_note_candidate",
      "eighth_note_candidate", "sixteenth_note_candidate", "thirty_second_note_candidate",
      "sixty_fourth_note_candidate", "quarter_rest_candidate"
  ]:
      continue
  ```
  Any `half_rest_candidate` or `half_rest` outcome is skipped (`continue`) and never passes into `ScoreIR`.
- **Historical Route Classification (`unproven`)**: Whether an older pre-`ff9fb48` recovery path accepted half rests into `ScoreIR` or if 1920 ticks entered via an external OMR sidecar is not backed by source code in current `score2gp` repository state and is classified as `unproven`. Current source code proves only current rejection.

### Question 3: Does generated ScoreIR, MusicXML, or GPIF contain a half rest in the first affected measure?
- **Observed Fact**: No. In `work/lesson5_work/score.ir.json`:
  - Total bars: 34.
  - Total rests across all bars in `ScoreIR`: 0.
  - Bar 0 events count: 4 events (containing TabRaw note fret extractions), with 0 rest events.

### Question 4: What meter and per-voice durations are emitted?
- **Source Facts**: Expected meter is `4/4` (measure capacity $C_{\text{measure}} = 3840$ ticks).
- **Emitted Meter**: Time signature emitted for Bar 0 and all 34 bars is `4/4` (`{'numerator': 4, 'denominator': 4}`).
- **Emitted Per-Voice Ordered Events & Durations**:
  - **Voice 1 Ordered Events (Bar 0)**:
    - Event 0: `onset_ticks=0`, `duration_ticks=480`, `voice=1`, `notated_duration={'value': 'eighth', 'dots': 0}`, `notes=['string=6,fret=8']`
    - Event 1: `onset_ticks=480`, `duration_ticks=480`, `voice=1`, `notated_duration={'value': 'eighth', 'dots': 0}`, `notes=['string=6,fret=10', 'string=5,fret=8']`
    - Event 2: `onset_ticks=960`, `duration_ticks=480`, `voice=1`, `notated_duration={'value': 'eighth', 'dots': 0}`, `notes=['string=4,fret=7']`
    - Event 3: `onset_ticks=1440`, `duration_ticks=2400`, `voice=1`, `notated_duration={'value': 'eighth', 'dots': 0}`, `notes=['string=4,fret=9', 'string=5,fret=8']`
  - **Voice 1 Duration Total**: $480 + 480 + 480 + 2400 = 3840$ ticks ($D_{\text{voice1}} = 3840$ ticks).
  - **Voice 2 Events**: None emitted (0 voice 2 event objects present in Bar 0).
  - **Measure Capacity Gate**: $D_{\text{voice1}} = 3840 \le C_{\text{measure}} = 3840$ ticks. Measure capacity is exactly filled, not exceeded.
  - **Remaining Visible Mismatch**: Event 3 (onset 1440, duration 2400 ticks) is internally labeled `notated_duration={'value': 'eighth', 'dots': 0}` while extending 2400 ticks to pad out the 3840-tick measure.

### Question 5: At what earliest current stage does observed output first differ from the approved source facts?
- **Committed Source Facts**: `2026-07-17-first-divergence-evidence-ledger.json` records `expected_meter: "4/4"`, `expected_tempo: 70`. Any assertion that Measure 1 requires 8 eighth notes is classified as `unproven` without independent visual score transcription.
- **Direct Source vs Output Comparison & Evidenced Injection Points (`supported`)**:
  1. **Tempo Mismatch (70 vs 120 BPM)**: Emitted top-level tempo is `{'bpm': 120, 'text': None}`, which contradicts `expected_tempo: 70`.
     - *Evidenced Code Injection Point*: [`src/score2gp/build_ir.py:L1629`](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/src/score2gp/build_ir.py#L1629) in `build_ir_from_tabraw_only()`, which declares `tempo_bpm: float = 120.0` default parameter and constructs `Tempo(bpm=tempo_bpm)`.
  2. **Event Duration Padding & Eighth-Label Mismatch**: Emitted Bar 0 Voice 1 Event 3 has duration 2400 ticks while labeled `notated_duration={'value': 'eighth', 'dots': 0}`.
     - *Evidenced Code Injection Point*: [`src/score2gp/build_ir.py:L1834-L1835`](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/src/score2gp/build_ir.py#L1834-L1835) in `build_ir_from_tabraw_only()`, which calculates `ev_duration_ticks = max(0, 3840 - current_onset)` for the final non-rest subgroup ($N=4$, $3840 - 1440 = 2400$) while retaining `ev_duration_name = duration_name` (`"eighth"` for $N \le 8$).
- **Divergence Note**: The historical 1920-tick false half rest divergence is **absent** (`DEFECT_NOT_REPRODUCED`).

---

## 4. Non-Executable Candidate Task Records Created

To satisfy prompt 0008's `DEFECT_NOT_REPRODUCED` gate, two non-executable candidate tasks with measurable decision criteria have been recorded for the two evidenced injection points:

1. [`projects/score2gp/tasks/2026-07-25-candidate-task-lesson5-tempo-mismatch.md`](../tasks/2026-07-25-candidate-task-lesson5-tempo-mismatch.md): Evaluates forwarding an explicit tempo parameter to `build_ir_from_tabraw_only()` ([line 1629](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/src/score2gp/build_ir.py#L1629)) vs defaulting to 120.0 BPM.
2. [`projects/score2gp/tasks/2026-07-25-candidate-task-lesson5-duration-padding.md`](../tasks/2026-07-25-candidate-task-lesson5-duration-padding.md): Evaluates aligning `notated_duration` with padded `duration_ticks` in `build_ir_from_tabraw_only()` ([lines 1834-1835](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/src/score2gp/build_ir.py#L1834-L1835)).

Neither candidate task authorizes product code changes.

---

## 5. Historical Ledger vs Current Evidence Comparison

| Dimension | Historical Evidence Ledger (2026-07-17) | Current Runtime Observation (`ff9fb48`) | Source Classification | Evidenced Injection Point |
| :--- | :--- | :--- | :--- | :--- |
| **False Rest Defect** | Half rest (1920 ticks) in measure 1 | None (0 rest events emitted) | `supported` | Absent on current `main` |
| **Detected Meter** | 12/8 (inflated measure duration 5760 ticks) | 4/4 (34 bars emitted) | `supported` | `build_ir.py:L1771` |
| **Tempo** | Expected `70` BPM | Emitted `120` BPM (`{'bpm': 120, 'text': None}`) | Mismatch (`supported`) | [`build_ir.py:L1629`](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/src/score2gp/build_ir.py#L1629) |
| **Notation Bridge Gate** | Claimed accepted in historical ledger | Filters out `half_rest_candidate` / `half_rest` | Current rejection `supported`; Historical acceptance `unproven` | [`notation_bridge.py:L41-47`](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/src/score2gp/notation_bridge.py#L41-L47) |
| **ScoreIR Rest Count** | 1 rest in measure 1 (1920 ticks) | 0 rest events in total | `supported` | N/A |
| **Voice 1 Bar 0 Durations** | Claimed `[480, 480, 480, 480, 480, 480, 480, 480, 1920]` | `[480, 480, 480, 2400]` ticks ($D_{\text{voice1}} = 3840$) | `supported` | [`build_ir.py:L1834-1835`](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/src/score2gp/build_ir.py#L1834-L1835) |

---

## 6. Decision Gate & Governed Next State

- **Selected Outcome**: **`DEFECT_NOT_REPRODUCED`**
- **Justification**: The false 1920-tick half rest is completely absent on current product `main`. Implementing obsolete half-rest suppression is disauthorized under Architect skill rules.
- **Product Code Authorization**: **NO PRODUCT CODE CHANGES AUTHORISED**.
- **Next Governed Step**: Publish this evidence report, synchronize governance state (`ACTIVE_TASK.md` and `prompts/NEXT.md`), record candidate decision tasks, and open a governance PR for Codex review.
