# 0038 - M1: Bar-Level Comparator and Mismatch Ledger

## Objective

Implement a reusable, deterministic bar-level comparator in the `score2gp` product repository. The comparator must read generated output (GPIF/ScoreIR/MusicXML) and reference files to produce a detailed, per-bar mismatch report. Additionally, add comprehensive public unit tests for this comparator, and use it to establish a truthful, no-reference baseline mismatch ledger for `Lesson-3` and `Lesson-4` on the approved private corpus.

## Authorized Product Files

- `src/score2gp/compare.py`
- `src/score2gp/cli.py`
- `tests/test_bar_comparator.py`

No other product files in `src/` may be edited in this task.

## Start

1. Work only in the canonical Ubuntu WSL repositories below `/home/tticom-automation/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `projects/score2gp/AGENT_CONTROL.md`, `projects/score2gp/ACTIVE_TASK.md`, `projects/score2gp/programmes/2026-07-16-teamwork-corpus-conversion-accuracy.md`, and product repository `AGENTS.md`.
4. Require clean governance and product worktrees.
5. Create product branch `agy/m1-bar-level-comparator` in `tticom/score2gp`.
6. Run `python scripts/agent_verify.py` in `score2gp` before making code modifications.

## Implementation Scope & Seam Contract

1. **Implement `compare.py`**:
   - Create a reusable comparator module that reads two score representations (actual and expected) and matches them bar-by-bar.
   - The comparison must inspect:
     - Ordered note and rest events.
     - Onset and duration in ticks/beats.
     - Dotted states, ties, and chord membership.
     - Pitch, string, and fret where applicable.
     - Key, time signature, and tempo changes.
     - Normal, double, and final barline styles.
     - Requested system/page break markers.
   - The comparator must return a structured result detailing the first mismatch and a compact per-bar event representation.
   - It must run safely as an invariant checker (without expected/reference input) or as a diagnostic comparator. It must never write back to either input.

2. **Expose CLI Command**:
   - Update `cli.py` to expose a command `compare-bars` that invokes the comparator and prints a clean, formatted text report of the mismatches.

3. **Verify and Test**:
   - Add unit tests in `tests/test_bar_comparator.py` using synthetic mock data to verify that the comparator correctly flags mismatching events, onsets, durations, barlines, and layout breaks.

## Validation Commands

1. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python -m pytest tests/test_bar_comparator.py`
2. `/home/tticom-automation/work/score2gp-workspace/score2gp/scripts/agent_verify.py`

## Non-goals

- Do not implement any OMR, pitch inference, duration association, or GPIF writing changes in this task.
- Do not modify existing `compare_gp` logic in `gp_package.py`.
- Do not commit any private fixture data or generated private GP/MusicXML files.
