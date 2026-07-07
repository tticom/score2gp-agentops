# Active Task

**Task**: Developer implementation — multi-staff track separation and parallel timing in notation_bridge.py
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## Status

APPROVED

## Executable Task

Yes

## 1. Baseline
- Product PR #337: squash-merged at `eae13541de67899ff9563a09f48ed747171dea6b`
- Governance PR #242: squash-merged at `373b6836b2121b82ad815753bcf78bc90e942137`
- Governance PR #243: squash-merged at `e43afed7ac541c8b1710693b5e0bce6a46bce9d4`
- Governance PR #244: squash-merged at `d6f8d8fbb08eb12ebd3665f618b6fdf93401e179`
- Research report: `projects/score2gp/research/2026-07-07-next-standard-staff-recognition-capability.md`

## 2. Context
Product PR #337 implemented same-onset chord grouping in `src/score2gp/notation_bridge.py` to prevent sequential tick accumulation errors for vertically aligned note candidates. Governance PR #244 recorded and approved the Architect's research report (Outcome B), identifying sequential timing serialization across multiple staves as the next blocker. This task authorises the Developer to implement parallel timing and track mapping for multi-staff scores.

## 3. Active Blocker
The existing notation bridge timing model serialises all candidates sequentially on a single track (`trk_0`) across different staves, causing tick overflow errors (such as `cumulative_duration_exceeds_one_4_4_bar` or incorrect timing) when multi-staff inputs are processed.

## 4. Goal
- Implement a bounded bridge-level timing model in `notation_bridge.py` so that note candidates from separate staves/tracks that are logically parallel do not accumulate onset ticks sequentially.
- Preserve existing single-staff sequential timing accumulation.
- Preserve same-onset chord grouping behaviour from PR #337.

## 5. Non-goals
- No true polyphony (multiple independent rhythmic voices on a single staff).
- No same-staff multi-voice support.
- No voice separation.
- No OMR candidate extraction changes.
- No staff geometry changes.
- No real-world score support claim.
- No private/copyrighted PDFs.
- No generated PDF/GP artifacts.
- No broad GP writer rewrite unless strictly necessary and separately justified.
- No UI/API changes.

## 6. Repo Scope
- **Allow**:
  - `src/score2gp/notation_bridge.py`
  - `tests/test_notation_bridge.py`
- **Stop before changing**:
  - GP writer/export internals (`gp_package.py`, `gpif.py`);
  - OMR recognisers (`whole_note_recogniser.py`, `quarter_rest_recogniser.py`);
  - staff geometry extraction;
  - fixture generators;
  - committed PDF fixtures;
  - CLI behaviour outside what tests require.

## 7. Branch Suggestion
`feature/multi-staff-bridge-parallel-timing-v0.1`

## 8. Pre-flight Checks
- `git status --short`
- `git branch --show-current`
- `git fetch --all --prune`
- Verify product `main` contains Product PR #337 merge commit.
- Inspect `notation_bridge.py` and `tests/test_notation_bridge.py`.
- Verify no private/generated artifacts are present.

## 9. Implementation Guidance
- Introduce the smallest bridge-level change needed to support independent timing accumulation per staff/track identity.
- Map each unique `staff_index` in outcomes to a separate `Track` in `ScoreIR` (e.g. `trk_0` for `staff_index=0`, `trk_1` for `staff_index=1`).
- Track `current_onset_ticks` independently for each staff/track, allowing parallel progression of time.
- Preserve same-onset chord grouping from PR #337.
- Coordinate-less/context-less candidates must retain safe existing behaviour and must not be silently grouped into parallel tracks unless identity is explicit.
- Multi-staff timing must be explicit and test-proven.
- If the current ScoreIR/GP model lacks enough track/staff representation to implement this safely, stop and return to Architect/Supervisor.

## 10. Required Tests & Evidence
Developer must add or update tests proving:
- Existing single-staff sequential timing still passes.
- Existing same-onset grouping still passes.
- Two staffs/tracks can maintain independent timing accumulation.
- Events from staff A do not incorrectly advance staff B timing.
- Events from staff B do not incorrectly advance staff A timing.
- Parallel starts across staff/track identities remain aligned where metadata indicates they should.
- Coordinate-less/context-less candidates do not gain unsafe parallel behaviour.
- No true polyphony or same-staff multi-voice behaviour is claimed.

## 11. Validation
- `PYTHONPATH=. .venv/bin/pytest tests/test_notation_bridge.py`

## 12. Acceptance Criteria
- Tests prove independent timing per staff/track.
- Existing notation bridge tests pass.
- Same-onset grouping behaviour from PR #337 is preserved.
- Implementation remains within authorised files unless stop condition triggers.
- No private/generated artifacts are committed.
- Developer report clearly states what was implemented, what was not implemented, commands run, and known limitations.

## 13. Failure Criteria
- Any existing same-onset grouping behaviour regresses.
- Single-staff sequential timing regresses.
- Coordinate-less/context-less candidates are unsafely grouped.
- Implementation claims true polyphony, same-staff multi-voice, voice separation, or real-world score support.
- Implementation needs GP writer/OMR/staff geometry changes without stopping.
- Tests are missing or only test implementation details.
- Private/generated artifacts are introduced.

## 14. Stop Conditions
- Stop if the current data model cannot represent independent staff/track timing safely.
- Stop if product files outside authorised scope must be modified.
- Stop if GP writer changes appear necessary.
- Stop if private/copyrighted PDFs are required.
- Stop if tests cannot prove behaviour from safe committed data.
- Stop if implementation would expand into OMR extraction, staff geometry, voice separation, or real polyphony.

## 15. Privacy/Artifact Constraints
- No private PDFs.
- No `.gp` files.
- No screenshots.
- No logs/dumps.
- No generated binaries.
- No rendered outputs.
- Check artifact hygiene before PR.

## 16. PR Requirements
- Product PR against `main`.
- Short-lived branch.
- No direct commits to `main`.
- Include exact files changed.
- Include commands run.
- Include test results.
- Include known limitations.
- Include artifact hygiene status.
- Required next review: Reviewer implementation conformance review.
- Required later review: PR readiness review.

## 17. Reporting Format
Developer must report exactly:
- Verdict
- Product PR URL
- Branch
- Head SHA
- Baseline
- Files changed
- Implementation summary
- Tests added/updated
- Commands run
- Test results
- Scope conformance
- Known limitations
- Artifact hygiene
- Required next review
