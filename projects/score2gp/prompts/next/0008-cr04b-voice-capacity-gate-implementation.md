# 0008 - CR-04B Per-Voice Measure Capacity Gate Implementation

## Objective

Implement a deterministic per-voice measure capacity gate in `score2gp.notation_omr.timeline` and false-rest candidate suppression in `score2gp.quarter_rest_recogniser`. Emit structured refusal `omr_voice_capacity_overfull` when any voice duration exceeds expected measure capacity, preventing overfull timeline output without mutating event timing or silently deleting notes.

## Authorised Role

Developer

## Product Repository & Base

- **Repository**: `tticom/score2gp`
- **Base Commit**: `ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f`
- **Branch**: `agy/cr04b-voice-capacity-gate`

## Requirements

1. **Per-Voice Measure Capacity Calculation**:
   - Calculate expected measure capacity $C_{\text{measure}} = P \times \frac{3840}{Q}$ ticks (e.g. 3840 ticks for 4/4 meter).
   - Sum time-advancing note and rest durations per voice per measure ($D_{\text{voice}}$).
   - Exclude zero-advance events (clefs, barlines, key/time sigs, secondary chord member noteheads in same chord event, grace notes).

2. **Overfull Voice Refusal Gate** (`src/score2gp/notation_omr/timeline.py`):
   - If $D_{\text{voice}} > C_{\text{measure}}$ for any voice in any measure, mark measure status as `overfull` and record diagnostic refusal `omr_voice_capacity_overfull`.
   - Do NOT silently delete notes, alter event durations, or balance durations across independent voices.

3. **False-Rest Candidate Suppression** (`src/score2gp/quarter_rest_recogniser.py`):
   - Suppress orphan `flag_candidate` promotion to `quarter_rest_candidate` if adding its duration (960 ticks) to the containing measure voice would cause $D_{\text{voice}} + 960 > C_{\text{measure}}$.

4. **Product File Allowlist**:
   - `[MODIFY] src/score2gp/notation_omr/timeline.py`
   - `[MODIFY] src/score2gp/quarter_rest_recogniser.py`
   - `[NEW] tests/test_notation_omr_voice_capacity.py`

## Test Plan & Verification

1. **Regression Contract Tests** (`tests/test_notation_omr_voice_capacity.py`):
   - `test_exact_capacity_measure_timeline()`: $D = C$ produces status `exact`.
   - `test_underfull_capacity_measure_timeline()`: $D < C$ produces status `underfull` with padding rests up to $C_{\text{measure}}$.
   - `test_overfull_capacity_measure_refusal()`: $D > C$ emits `omr_voice_capacity_overfull` refusal.
   - `test_orphan_flag_false_rest_suppression_on_overflow()`: Suppresses orphan flag rest promotion when it causes measure overflow.
   - `test_chord_member_zero_advance()`: Multi-notehead chord members advance voice duration only once.

2. **Full Verification Suite**:
   ```bash
   .venv/bin/python -m pytest -v tests/test_notation_omr_voice_capacity.py
   .venv/bin/python -m pytest
   .venv/bin/python -m score2gp.cli export-schema --out schemas
   .venv/bin/python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json
   .venv/bin/python scripts/artifact_audit.py
   git diff --check origin/main...HEAD
   git diff --exit-code -- schemas
   git ls-files fixtures/private work
   git status --short
   ```

## Handoff

Commit allowed product files only, push `agy/cr04b-voice-capacity-gate` branch, and open one draft product PR on `tticom/score2gp`. Include exact verification results in PR description. Stop for independent review; do not merge.
