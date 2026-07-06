# Decision Record — Product PR #337 Same-Onset Chord Grouping Completion

- **Status**: COMPLETED
- **Product PR**: [PR #337](https://github.com/tticom/score2gp/pull/337)
- **Product Merge**:
  - Reviewed/merged head SHA: `b69f390ee74cc2425a4deb4b8ccaccc8d634cf5b`
  - Merge commit: `eae13541de67899ff9563a09f48ed747171dea6b`
  - Merged timestamp: `2026-07-06T19:51:28Z`
- **Baselines**:
  - Product PR #336 merge commit: `cae6a416076e66f6b84940ad0cbf3061beb241d9`
  - Governance PR #240 merge commit: `9c4ec0e7c98ffc923d7ac347f55e9e8a0a6b12cd`
  - Governance PR #241 merge commit: `ad49f26964ede1d45325854f6fde1c4c9770f0a1`

## Implemented Capability
- Bounded same-onset chord grouping in `src/score2gp/notation_bridge.py`.
- Only note candidates sharing page, system, and staff index identity, and within 1.0-point horizontal coordinate tolerance can group.
- Coordinate-less/context-less candidates stay sequential and do not group.
- Grouped Event contains multiple Notes and advances onset once per Event/group.

## Files Changed in Product PR
- `src/score2gp/notation_bridge.py`
- `tests/test_notation_bridge.py`

## Review Evidence
- Implementation conformance approved at head: `b69f390ee74cc2425a4deb4b8ccaccc8d634cf5b`.
- Merge was verified live; readiness report text was not present in this task context.

## Validation Evidence
- Reported by Developer/Reviewer:
  - Bounded same-context chord grouping verified with unit tests.
  - Coordinate-less and context-less candidates verified to remain separate.
  - All 863 pytest tests pass.
  - GitHub CI tests passed.

## Explicit Non-Goals and Limitations
- No true polyphony.
- No same-staff multi-voice support.
- No voice separation.
- No OMR extraction changes.
- No staff geometry changes.
- No GP writer changes.
- No new PDF fixtures.
- No committed `.gp` artifacts.
- No real-world score support claim.

## Governance State
- Developer authorisation closed.
- No active task approved (status `NO_ACTIVE_TASK_APPROVED`).
- Next step requires Supervisor decision.
