# Grace Note Support Architecture Investigation v0.1

This document investigates the current handling of grace notes in the `score2gp` codebase and designs the smallest safe implementation slice to introduce grace-note alignment and serialization.

## Verdict

`safe minimal implementation slice identified`

## Evidence

- **Product Branch**: `main`
- **Product Commit Hash**: `b9f54a40ffa963e83e91a2fd22070ec9eeff6d75`
- **Agentops Branch**: `research/grace-note-support-architecture-v0.1`
- **Agentops Commit Hash**: `a6d0e34`
- **Commands Run**:
  - `git switch main`
  - `git pull --ff-only origin main`
  - `PYTHONPATH=. .venv/bin/python3 -m pytest`
  - `PYTHONPATH=. .venv/bin/python3 scripts/private_e2e_smoke.py`
  - `PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py`
  - `git ls-files fixtures/private work`
  - `git diff --check`
- **Public Test Result**: All 466 tests passed successfully.
- **Private Smoke Result**: Successfully processed all 12 private booklets and wrote reports.
- **Private Quality Audit Result**:
  - `private_input_1` passes quality audit with `gp_output_technique_loss_expected` and 137/137 matched notes.
  - Lessons 3–7 remain stable and passed.
  - Melodic Soloing remains stable at 82 matched notes.
- **Private-Safety Result**: `git ls-files fixtures/private work` outputs exactly `fixtures/private/.gitkeep`.
- **Working Tree Status**: Clean (no modified tracked files).

---

## Grace-note loss table

| Phase | Current Behaviour | Observed Count | Fatal or Skipped | Evidence Path under `work/` | Interpretation | Proposed Next Action |
| --- | --- | --- | --- | --- | --- | --- |
| **MusicXML parse** | Parses grace notes and sets `grace = True` but emits warning `unsupported-grace-note`. Voice 5 TAB grace notes are suppressed (`n.is_suppressed = True`), but their fret/string data is NOT merged into Voice 1 grace notes because of `not n.grace` filter in `musicxml.py` deduplication. | 90 (45 in Voice 1, 45 in Voice 5) | Skipped (warning logged) | `work/private_e2e_smoke_v0_1/private_input_1/diagnostics.json` | Parsing is successful, but skipping deduplication/merge leaves notation grace notes without string/fret data, while TAB grace notes are suppressed. | Update `deduplicate_suspected_staff_tab_voices` in `musicxml.py` to merge notation/TAB grace notes. Parse `slash` attribute from the `<grace>` tag. |
| **timing analysis** | Skips grace notes (`not n.grace`) when checking voice extents and durations. | 0 warnings/errors (grace notes are ignored) | Skipped | `work/private_e2e_smoke_v0_1/private_input_1/diagnostics.json` | Rhythmic duration checks correctly ignore grace notes, as they do not consume main timeline duration. | Retain skipping in timing checks to prevent false timing overlaps. |
| **build-ir candidate matching** | Skips note groups starting with a grace note during event creation, emitting a `musicxml-grace-skipped` warning. Consequently, their corresponding PDF candidates are left unmatched. | 15 skipped grace notes in measures 1-7 | Skipped | `work/private_e2e_smoke_v0_1/private_input_1/diagnostics.json` | Skipping grace notes prevents their PDF candidates from being aligned, leaving 15 unmatched fret candidates and causing pitch mismatches on adjacent main notes. | Stop skipping grace notes during event creation, allowing them to be aligned. |
| **ScoreIR construction** | Grace notes are skipped entirely and not compiled into `Bar.events`. | 15 events skipped (Page 1-2) | Skipped | `work/private_e2e_smoke_v0_1/private_input_1/score.ir.json` | ScoreIR has no grace events. | Compile grace notes as separate `Event` objects in `Bar.events` with `event.timing.grace` populated and `onset_ticks` equal to the host note's `onset_ticks`. |
| **GPIF serialization** | Writer already supports serializing grace notes if they are present in ScoreIR, writing `<GraceNotes>` and the `Grace` property. | 0 (since none are in ScoreIR) | Skipped | `src/score2gp/gpif.py` | Serialization support is already built-in. | Verify serialization works with synthetic tests once grace notes are emitted. |
| **GPIF parser recovery** | GPIF is only written, not parsed back (no parser recovery in product flow). | N/A | N/A | N/A | Not applicable. | N/A |

---

## Skipped grace-note classification table

Counts from `private_input_1` (`Derek Trucks BB King`):

| Classification Category | Observed Count | Interpretation / Notes |
| --- | --- | --- |
| **Total skipped grace notes** | 90 | 45 in notation voice (Voice 1), 45 in TAB voice (Voice 5). |
| **Pitched grace notes** | 90 | All 90 grace notes have pitch data. |
| **Grace notes with string/fret** | 45 | All 45 Voice 5 grace notes have string/fret details in XML. |
| **Slash grace notes** | 0 | All grace notes in the MusicXML are marked with `slash="no"`. |
| **Grace notes with host/following note evidence** | 45 | Each notation grace note is followed by a main note in the same measure and voice. |
| **Grace notes with matching PDF candidate evidence** | 15 | 15 grace notes in measures 1-7 match 15 unmatched PDF candidates on Page 1. |
| **Ambiguous grace notes** | 0 | No ambiguities; they form a clear one-to-one sequence before host notes. |
| **Unsafe cases** | 0 | No timing/overlap issues or layout violations. |

---

## Architecture recommendation

### Smallest Next Developer Task
Implement grace-note alignment and serialization for pitched tab grace notes.

- **Branch Name**: `feature/grace-note-support-v0.1` (on product repo)
- **Affected Files/Modules**:
  - [musicxml.py](file:///home/tticom/work/score2gp-workspace/score2gp/src/score2gp/musicxml.py)
  - [build_ir.py](file:///home/tticom/work/score2gp-workspace/score2gp/src/score2gp/build_ir.py)
- **Goal**: Merge Voice 5 grace note details into Voice 1 notation grace notes, compile them into ScoreIR events, align them to PDF candidates, and serialize them to GPIF. This should resolve 15 of the 16 unmatched candidates on Page 1 of `private_input_1`.
- **Non-goals**:
  - Do not change ASCII tab gate logic.
  - Do not change spacing/geometry layout gating.
  - Do not edit grace notes in tracks other than the primary guitar track.
- **Implementation Approach**:
  1. **Parse Grace slash**: Update XML parsing in `musicxml.py` to parse the `slash` attribute of the `<grace>` node (defaulting to `False` if not `"yes"`).
  2. **Deduplicate Grace Notes**: Update `deduplicate_suspected_staff_tab_voices` in `musicxml.py` to also pair and merge grace notes in notation voice and TAB voice, copying string, fret, and other technical details to the notation grace note.
  3. **Compile Grace Events**: Update `_measure_events` in `build_ir.py` to stop skipping grace notes. Compile them as separate `Event` objects with `event.timing.grace = GraceTiming(position="before", slash=note.grace_slash, duration_ticks=0, duration=note.notated_type)` and `onset_ticks` equal to the following host note's `onset_ticks`.
  4. **Align Grace Candidates**: In the candidate alignment phase, ensure grace events are matched to PDF candidates positioned immediately before the host note's candidate (by X coordinate ordering).
- **Tests Required**:
  - MusicXML with one simple grace note before a normal note.
  - MusicXML with grace note containing string/fret technical data.
  - Grace note with slash.
  - Grace note without duration.
  - Grace note should not affect measure duration.
  - Grace note should round-trip through GPIF.
- **Validation Commands**:
  ```bash
  PYTHONPATH=. .venv/bin/python3 -m pytest
  PYTHONPATH=. .venv/bin/python3 scripts/private_e2e_smoke.py
  PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py
  ```
- **Acceptance Criteria**:
  - All public tests pass.
  - `private_input_1` passes quality audit, and unmatched PDF candidates in measures 1-7 drop from 16 to 1.
  - No regression in Lessons 3-7 or Melodic Soloing.
  - The private-safety invariant remains clean.
- **Stop Conditions**:
  - Any public test fails.
  - `private_input_1` default-flow fails to run.
  - Grace notes cause timing overlap errors in `analyze_musicxml_timing`.
