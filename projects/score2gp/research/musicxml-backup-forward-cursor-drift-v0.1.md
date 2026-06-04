# MusicXML Backup/Forward Cursor Drift Investigation v0.1

## Verdict
safe narrow remediation identified

## Evidence
* **Product branch**: `main`
* **Product commit hash**: `811313182852ec41f88daaf5db19cd59b0d8a513`
* **Agentops branch**: `research/musicxml-backup-forward-cursor-drift-v0.1`
* **Agentops commit hash**: `d158aba7d58882bf595830ddd0dca7aef37865ff`
* **Commands run**:
  - `wsl bash -c "PYTHONPATH=. .venv/bin/python3 -m pytest"`
  - `wsl bash -c "PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py"`
  - `git ls-files fixtures/private work`
  - `git diff --check`
  - `git status --short`
* **Public test result**: 457 passed
* **Private audit result**: 
  - `private_input_1`: fail (`gp_output_empty_or_near_empty`, 0 notes, 0 matched) due to `musicxml_unbalanced_backup_forward` (15 occurrences)
  - `private_input_custom_lesson_3`: pass (459 matched notes)
  - `private_input_custom_lesson_4`: pass (546 matched notes)
  - `private_input_custom_lesson_5`: pass (295 matched notes)
  - `private_input_custom_lesson_6`: pass (235 matched notes)
  - `private_input_custom_lesson_7`: pass (624 matched notes)
  - `private_input_custom_melodic_soloing`: pass (82 matched notes)
* **Private-safety output**: `fixtures/private/.gitkeep` (no private musical content committed)
* **Working tree status**: Clean (with only `.antigravitycli/...json` modified)

## Backup/Forward Drift Table
Here is the private-safe table documenting all 15 occurrences of the `musicxml_unbalanced_backup_forward` blocker in `private_input_1` (Part `P1` / `Derek Trucks BB King`):

| Measure Number | Expected Divisions | Observed Final Cursor | Delta | Backup Count | Forward Count | Voice Cursor Ends | Voice Duration Summary | Overlap Summary | Fatal Issue Codes | Interpretation | Recommended Handling |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 48.0 | 45 | -3.0 | 1 | 0 | `{'1': 45, '5': 45}` | `{'1': 45, '5': 45}` | 0 same-voice, 9 cross-voice | `musicxml_unbalanced_backup_forward`, `musicxml_backup_forward_alignment_ambiguous` | Underfull duplicate staff/TAB voices | Treat as remediable under `allow_remediation` |
| 2 | 192.0 | 189 | -3.0 | 1 | 0 | `{'1': 189, '5': 189}` | `{'1': 189, '5': 189}` | 0 same-voice, 10 cross-voice | `musicxml_unbalanced_backup_forward`, `musicxml_backup_forward_alignment_ambiguous` | Underfull duplicate staff/TAB voices | Treat as remediable under `allow_remediation` |
| 3 | 288.0 | 264 | -24.0 | 1 | 0 | `{'1': 264, '5': 264}` | `{'1': 264, '5': 264}` | 0 same-voice, 8 cross-voice | `musicxml_unbalanced_backup_forward`, `musicxml_backup_forward_alignment_ambiguous` | Underfull duplicate staff/TAB voices | Treat as remediable under `allow_remediation` |
| 4 | 48.0 | 46 | -2.0 | 1 | 0 | `{'1': 46, '5': 46}` | `{'1': 46, '5': 46}` | 0 same-voice, 9 cross-voice | `musicxml_unbalanced_backup_forward`, `musicxml_backup_forward_alignment_ambiguous` | Underfull duplicate staff/TAB voices | Treat as remediable under `allow_remediation` |
| 5 | 576.0 | 546 | -30.0 | 1 | 0 | `{'1': 546, '5': 546}` | `{'1': 546, '5': 546}` | 0 same-voice, 12 cross-voice | `musicxml_unbalanced_backup_forward`, `musicxml_backup_forward_alignment_ambiguous` | Underfull duplicate staff/TAB voices | Treat as remediable under `allow_remediation` |
| 6 | 240.0 | 220 | -20.0 | 1 | 0 | `{'1': 220, '5': 220}` | `{'1': 220, '5': 220}` | 0 same-voice, 14 cross-voice | `musicxml_unbalanced_backup_forward`, `musicxml_backup_forward_alignment_ambiguous` | Underfull duplicate staff/TAB voices | Treat as remediable under `allow_remediation` |
| 7 | 240.0 | 232 | -8.0 | 1 | 0 | `{'1': 232, '5': 232}` | `{'1': 232, '5': 232}` | 0 same-voice, 9 cross-voice | `musicxml_unbalanced_backup_forward`, `musicxml_backup_forward_alignment_ambiguous` | Underfull duplicate staff/TAB voices | Treat as remediable under `allow_remediation` |
| 8 | 960.0 | 873 | -87.0 | 1 | 0 | `{'1': 873, '5': 873}` | `{'1': 873, '5': 873}` | 0 same-voice, 10 cross-voice | `musicxml_unbalanced_backup_forward`, `musicxml_backup_forward_alignment_ambiguous` | Underfull duplicate staff/TAB voices | Treat as remediable under `allow_remediation` |
| 9 | 240.0 | 227 | -13.0 | 1 | 0 | `{'1': 227, '5': 227}` | `{'1': 227, '5': 227}` | 0 same-voice, 11 cross-voice | `musicxml_unbalanced_backup_forward`, `musicxml_backup_forward_alignment_ambiguous` | Underfull duplicate staff/TAB voices | Treat as remediable under `allow_remediation` |
| 10 | 576.0 | 543 | -33.0 | 1 | 0 | `{'1': 543, '5': 543}` | `{'1': 543, '5': 543}` | 0 same-voice, 15 cross-voice | `musicxml_unbalanced_backup_forward`, `musicxml_backup_forward_alignment_ambiguous` | Underfull duplicate staff/TAB voices | Treat as remediable under `allow_remediation` |
| 11 | 240.0 | 222 | -18.0 | 1 | 0 | `{'1': 222, '5': 222}` | `{'1': 222, '5': 222}` | 0 same-voice, 15 cross-voice | `musicxml_unbalanced_backup_forward`, `musicxml_backup_forward_alignment_ambiguous` | Underfull duplicate staff/TAB voices | Treat as remediable under `allow_remediation` |
| 13 | 192.0 | 186 | -6.0 | 1 | 0 | `{'1': 186, '5': 186}` | `{'1': 186, '5': 186}` | 0 same-voice, 11 cross-voice | `musicxml_unbalanced_backup_forward`, `musicxml_backup_forward_alignment_ambiguous` | Underfull duplicate staff/TAB voices | Treat as remediable under `allow_remediation` |
| 14 | 1440.0 | 1239 | -201.0 | 1 | 0 | `{'1': 1239, '5': 1239}` | `{'1': 1239, '5': 1239}` | 0 same-voice, 19 cross-voice | `musicxml_unbalanced_backup_forward`, `musicxml_backup_forward_alignment_ambiguous` | Underfull duplicate staff/TAB voices | Treat as remediable under `allow_remediation` |
| 15 | 48.0 | 46 | -2.0 | 1 | 0 | `{'1': 46, '5': 46}` | `{'1': 46, '5': 46}` | 0 same-voice, 10 cross-voice | `musicxml_unbalanced_backup_forward`, `musicxml_backup_forward_alignment_ambiguous` | Underfull duplicate staff/TAB voices | Treat as remediable under `allow_remediation` |
| 16 | 48.0 | 47 | -1.0 | 1 | 0 | `{'1': 47, '5': 47}` | `{'1': 47, '5': 47}` | 0 same-voice, 11 cross-voice | `musicxml_unbalanced_backup_forward`, `musicxml_backup_forward_alignment_ambiguous` | Underfull duplicate staff/TAB voices | Treat as remediable under `allow_remediation` |

Note: Measure 12 is balanced and does not trigger this issue.

## Classification Summary
* **Count of small terminal drift cases**: 15 (all 15 cases fall within the small terminal cursor drift pattern where the voices are coherent but stop slightly short of the expected measure boundary).
* **Count of genuine invalid cursor cases**: 0 (all timelines are mathematically consistent, they are just underfull).
* **Count of backup-before-zero cases**: 0
* **Count of forward-after-end cases**: 0
* **Count of voice extent mismatch cases**: 0
* **Count of cases where per-voice extents appear coherent**: 15 (all voice extents are aligned and match the final cursor exactly).
* **Count of cases that remain unsafe**: 0

## Architecture Recommendation
We recommend implementing **Shape A** to resolve this blocker. This is the narrowest and safest approach because the cursor drift is caused by underfull measures in a duplicate-staff structure, and no genuine timing invalidity or voice overlap exists.

### Developer Task Plan
* **Branch name**: `feature/musicxml-backup-forward-remediation-v0.1`
* **Affected files/modules**: `src/score2gp/musicxml.py`
* **Goal**: Enable downgrading of `musicxml_unbalanced_backup_forward` and `musicxml_backup_forward_alignment_ambiguous` timing issues to warnings when `allow_remediation=True` is enabled, provided that the timing is otherwise safe/coherent.
* **Non-goals**:
  - Do not globally downgrade unbalanced backup/forward errors (severity must remain `error` when `allow_remediation` is `False`).
  - Do not alter tuplet parsing, palm mute, let ring, or other unrelated components.
  - Do not allow backup-before-zero, forward-after-end, same-voice overlaps, or overfull bars to become warnings.
* **Implementation approach**:
  - In `src/score2gp/musicxml.py:analyze_musicxml_timing`, check if `getattr(imported, "allow_remediation", False)` is `True`.
  - For each timing issue of code `musicxml_unbalanced_backup_forward` or `musicxml_backup_forward_alignment_ambiguous`, change its severity from `"error"` to `"warning"` if the measure contains no other fatal timing errors (i.e., no overfull bar, no same-voice overlaps, no backup before zero, and no forward after end).
* **Tests required**:
  - Add unit tests in `tests/test_musicxml_voice_cursor.py` targeting `allow_remediation=True` to confirm that:
    - An underfull measure with backup/forward is downgraded to `"warning"`.
    - Overfull measures, same-voice overlaps, backup before zero, or forward past end still trigger `"error"`.
* **Validation commands**:
  - `python -m pytest`
  - `python scripts/private_gp_quality_audit.py`
* **Acceptance criteria**:
  - All public tests (457) pass.
  - Unit tests for the remediation pass successfully.
  - `private_input_1` passes the timing preflight suitability gate (allowing ScoreIR generation and GP package serialization).
* **Stop conditions**:
  - If any public test breaks.
  - If same-voice overlaps or overfull bars are incorrectly downgraded.
  - If the private-safety invariant is violated.
