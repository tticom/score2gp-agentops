Title: MusicXML Quadruplet and Quintuplet Preflight Support v0.1

Context:
The post-milestone audit shows that the melodic soloing milestone is complete and stable. The next highest-value blocker is `private_input_1` / Derek Trucks BB King, which is blocked in MusicXML timing preflight.

Current verified milestone state:

* Product main includes PR #165.
* Product merge commit: `47cf92c52408e8c1f2d08400f7e8a075d14ff266`.
* Public baseline: `456 passed`.
* Lessons 3–7 are stable:

  * Lesson 3: 459 matched
  * Lesson 4: 546 matched
  * Lesson 5: 295 matched
  * Lesson 6: 235 matched
  * Lesson 7: 624 matched
* Melodic Soloing is at 100% note coverage:

  * 82 playable candidates
  * 82 matched notes
  * 82 ScoreIR notes
  * 82 GPIF notes
  * 8 bar boxes
* Private-safety invariant is clean:
  `git ls-files fixtures/private work` -> `fixtures/private/.gitkeep`

Research context:
The MusicXML timing-risk decomposition identified two remaining fatal issue classes for `private_input_1`:

1. `musicxml_unbalanced_backup_forward`, first seen at Measure 1, where OMR cursor offsets leave the timeline cursor at 45 divisions instead of expected 48.
2. `musicxml_tuplet_unsupported`, with 67 occurrences on staff 2, caused by quadruplets `4:3` and quintuplets `5:3`.

The audit also showed that under `allow_remediation=True`, cross-voice overlaps are successfully downgraded to warnings, so cross-voice overlap is not the next implementation target.

Goal:
Add narrow MusicXML preflight support for quadruplet `4:3` and quintuplet `5:3` tuplets so they are parsed as supported tuplets rather than fatal `musicxml_tuplet_unsupported` errors.

Branch:
`feature/musicxml-tuplet-quintuplet-quadruplet-support-v0.1`

Role:
Developer.

Non-goals:

* Do not attempt to fix `musicxml_unbalanced_backup_forward`.
* Do not change backup/forward cursor reconciliation.
* Do not relax timing preflight globally.
* Do not suppress `musicxml_tuplet_unsupported` without parsing the tuplets correctly.
* Do not implement a full tuplets engine for arbitrary ratios.
* Do not change PDF layout, TAB grouping, barline recovery, GPIF writing, or technique handling.
* Do not commit private MusicXML, private PDFs, generated GP files, audit JSON, logs, overlays, screenshots, or anything under `work/`.

Likely affected files:

* `src/score2gp/musicxml.py`
* `tests/test_musicxml.py`

Required pre-flight:
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
Find the note parsing logic in `src/score2gp/musicxml.py` that creates `MusicXmlTuplet` and sets `MusicXmlNote.tuplet_unsupported`.

Current expected conceptual behaviour:

* Triplets `3:2` are supported.
* Other tuplets are marked unsupported.
* `analyze_musicxml_timing` emits fatal `musicxml_tuplet_unsupported` when `note.tuplet_unsupported` is true.

Change the supported tuplet predicate to allow exactly:

* triplet: `actual_notes == 3 and normal_notes == 2`
* quadruplet: `actual_notes == 4 and normal_notes == 3`
* quintuplet: `actual_notes == 5 and normal_notes == 3`

Do not allow arbitrary tuplets in this PR.

Suggested helper shape:

```python
def _is_supported_tuplet(tuplet: MusicXmlTuplet | None) -> bool:
    if tuplet is None:
        return True
    return (
        (tuplet.actual_notes == 3 and tuplet.normal_notes == 2)
        or (tuplet.actual_notes == 4 and tuplet.normal_notes == 3)
        or (tuplet.actual_notes == 5 and tuplet.normal_notes == 3)
    )
```

Then set:

```python
tuplet_unsupported = tuplet is not None and not _is_supported_tuplet(tuplet)
```

Tests required:
Add public synthetic tests in `tests/test_musicxml.py`.

At minimum cover:

1. Existing triplet `3:2` remains supported.
2. Quadruplet `4:3` is supported and does not set `tuplet_unsupported`.
3. Quintuplet `5:3` is supported and does not set `tuplet_unsupported`.
4. Unsupported tuplets, for example `7:4` or malformed ratio, remain unsupported.
5. A synthetic 12/8 measure containing supported `4:3` and `5:3` tuplets does not emit `musicxml_tuplet_unsupported`.
6. Existing passing MusicXML tests still pass.

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
* New tuplets tests pass.
* Existing triplet behaviour is unchanged.
* Unsupported arbitrary tuplets remain rejected.
* `musicxml_tuplet_unsupported` count for `private_input_1` drops from 67 to 0.
* Lessons 3–7 remain stable.
* Melodic Soloing remains stable at 82 matched notes.
* Private-safety invariant remains clean.
* Any remaining failure in `private_input_1` is clearly reported, expected to be `musicxml_unbalanced_backup_forward` / backup-forward cursor drift.

Stop conditions:
Stop and report instead of broadening the task if:

* Public tests fail before changes.
* Private-safety invariant fails.
* The parser does not expose `actual_notes` / `normal_notes` in the expected place.
* Supporting `4:3` or `5:3` causes invalid duration grids or new timing errors in passing fixtures.
* The only way to make private_input_1 pass is to relax backup/forward, overlap, or timing-risk gates.
* Triplet parsing regresses.
* Any private/generated artifact would be committed.

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
* supported tuplet ratios
* unsupported ratios still rejected
* public test result
* private audit result, counts only
* `musicxml_tuplet_unsupported` before/after count for private_input_1
* remaining fatal MusicXML timing blockers
* Lessons 3–7 matched counts
* Melodic Soloing matched count
* private-safety output
* working tree status
