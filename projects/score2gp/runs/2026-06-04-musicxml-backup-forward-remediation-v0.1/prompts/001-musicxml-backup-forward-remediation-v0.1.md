Title: MusicXML Backup/Forward Underfull Remediation v0.1

Context:
The MusicXML tuplet support PR has been merged.

Recent merged work:

* Product PR #166 added narrow support for MusicXML tuplets:

  * triplet 3:2
  * quadruplet 4:3
  * quintuplet 5:3
* `musicxml_tuplet_unsupported` for `private_input_1` dropped from 67 to 0.
* Public tests: 457 passed.
* Lessons 3–7 remain stable:

  * Lesson 3: 459
  * Lesson 4: 546
  * Lesson 5: 295
  * Lesson 6: 235
  * Lesson 7: 624
* Melodic Soloing remains stable at 82 matched notes.
* Private-safety invariant remains clean:
  `git ls-files fixtures/private work` -> `fixtures/private/.gitkeep`

Current active blocker:
`private_input_1` / Derek Trucks BB King is still blocked by `musicxml_unbalanced_backup_forward`, currently 15 occurrences.

Research finding:
The 15 affected measures are not blocked by tuplets anymore. They are duplicate staff/TAB voice structures where:

* voice 1 is notation staff
* voice 5 is TAB staff
* duplicate staff/TAB voice classification is confirmed by `classify_musicxml_voice_duplication`
* each voice timeline is internally coherent
* same-voice overlaps are not present
* cross-voice overlaps are remediated/downgraded under `allow_remediation=True`
* the global parsing cursor ends slightly underfull, for example 45 divisions instead of expected 48
* backup elements are used to transition between staves/voices and can cap/wrap the parsing cursor to zero
* `MusicXmlMeasure.unbalanced_backup_forward` is set before duplicate voice suppression, so it remains fatal even after the duplicate TAB voice is suppressed

This is a false-positive fatal timing blocker for underfull duplicate staff/TAB measures. Single-staff underfull measures normally produce warnings, not fatal timing errors.

Goal:
Implement a narrow remediation that downgrades `musicxml_unbalanced_backup_forward` and `musicxml_backup_forward_alignment_ambiguous` from error to warning only when `allow_remediation=True` and the affected measure is otherwise timing-safe.

Branch:
`feature/musicxml-backup-forward-remediation-v0.1`

Role:
Developer.

Likely affected files:

* `src/score2gp/musicxml.py`
* `tests/test_musicxml.py` or `tests/test_musicxml_voice_cursor.py`

Non-goals:

* Do not globally downgrade backup/forward errors.
* Do not downgrade anything when `allow_remediation=False`.
* Do not downgrade genuine invalid timing.
* Do not downgrade same-voice overlaps.
* Do not downgrade overfull bars.
* Do not downgrade backup-before-zero or forward-after-end cases.
* Do not change tuplet handling.
* Do not change PDF layout, TAB grouping, barline recovery, GPIF writing, technique handling, or MusicXML/PDF alignment.
* Do not commit private MusicXML, private PDFs, generated GP files, generated XML, audit JSON, logs, overlays, screenshots, or anything under `work/`.

Pre-flight:
Run in product repo:

```bash
git switch main
git pull --ff-only origin main
git status --short --branch
git log --oneline --decorate --max-count=10
gh pr status
PYTHONPATH=. .venv/bin/python3 -m pytest
PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py
git ls-files fixtures/private work
git diff --check
```

Private-safety invariant:
This command:

```bash
git ls-files fixtures/private work
```

must output exactly:

```text
fixtures/private/.gitkeep
```

Stop immediately if this fails.

Implementation guidance:
In `analyze_musicxml_timing`, add a narrow remediation pass for backup/forward drift.

Important ordering:
Apply the backup/forward remediation after all timing issues for a measure have been collected, but before the code counts measure-level fatal errors for `musicxml_many_timing_risks`.

The remediation must only affect issue codes:

* `musicxml_unbalanced_backup_forward`
* `musicxml_backup_forward_alignment_ambiguous`

Only downgrade these from `error` to `warning` when all of the following are true:

1. `getattr(imported, "allow_remediation", False)` is true.
2. The measure has `voice_cursor_diagnostics`.
3. The measure is underfull-only, not overfull.
4. `vcd.same_voice_overlap_count == 0`.
5. `measure.backup_rewinds_before_measure_start` is false.
6. `measure.forward_exceeds_measure_end` is false.
7. No fatal overfull issue exists for that measure.
8. No fatal same-voice overlap or rest/note overlap issue exists for that measure.
9. No `musicxml_invalid_duration_grid` fatal issue exists for that measure.
10. Preferably, duplicate staff/TAB voice evidence is present via the existing duplication classifier, if available in this path.

Do not rely only on issue text. Use structured measure fields and `MusicXmlVoiceCursorDiagnostics` where possible.

Suggested helper shape:

```python
def _can_remediate_backup_forward_drift(
    measure: MusicXmlMeasure,
    measure_issues: list[MusicXmlTimingIssue],
) -> bool:
    ...
```

The helper should return `False` unless the measure is clearly safe.

When downgrading, preserve the issue code and add useful diagnostic metadata if the model already supports it. Do not delete the issue. It should remain visible as a warning.

Tests required:
Add public synthetic tests.

At minimum cover:

1. `allow_remediation=True` downgrades underfull-only backup/forward drift to warnings.
2. `allow_remediation=False` keeps the same backup/forward drift fatal.
3. Overfull measure with backup/forward remains fatal.
4. Same-voice overlap with backup/forward remains fatal.
5. Backup rewinds before measure start remains fatal.
6. Forward exceeds measure end remains fatal.
7. Existing passing MusicXML tests still pass.
8. Tuplet support from PR #166 remains unchanged.

Validation:
Run and report:

```bash
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_musicxml.py
PYTHONPATH=. .venv/bin/python3 -m pytest
PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py
git ls-files fixtures/private work
git diff --check
git status --short
```

Acceptance criteria:

* Public tests pass.
* New backup/forward remediation tests pass.
* `allow_remediation=False` keeps unsafe backup/forward cases fatal.
* `allow_remediation=True` downgrades only safe underfull backup/forward drift.
* Same-voice overlaps remain fatal.
* Overfull bars remain fatal.
* Backup-before-zero remains fatal.
* Forward-after-end remains fatal.
* `musicxml_tuplet_unsupported` remains 0 for `private_input_1`.
* `musicxml_unbalanced_backup_forward` fatal count for `private_input_1` drops from 15 to 0, or the report explains which cases remain fatal and why.
* Lessons 3–7 remain stable.
* Melodic Soloing remains stable at 82 matched notes.
* Private-safety invariant remains clean.

Expected outcome:
If the research is correct, `private_input_1` should pass the timing preflight suitability gate or move to the next later blocker. If it does not pass, report the new first fatal issue class rather than broadening the patch.

Stop conditions:
Stop and report instead of broadening the task if:

* Public tests fail before changes.
* Private-safety invariant fails.
* Same-voice overlaps would need to be downgraded.
* Overfull bars would need to be downgraded.
* Backup-before-zero or forward-after-end would need to be downgraded.
* The remediation cannot distinguish safe underfull drift from genuinely invalid timing.
* The fix requires committing private artifacts.
* The only viable solution appears to be a broader MusicXML timing-engine rewrite.

Reporting format:
Verdict:

* ready for review
* blocked
* needs architecture decision
* false hypothesis

Include:

* branch name
* commit hash
* files changed
* implementation summary
* exact downgrade conditions
* public test result
* private audit result, counts only
* `musicxml_unbalanced_backup_forward` before/after fatal count
* remaining fatal MusicXML timing blockers, if any
* whether `private_input_1` now passes timing preflight
* Lessons 3–7 matched counts
* Melodic Soloing matched count
* private-safety output
* working tree status
