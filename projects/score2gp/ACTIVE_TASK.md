# Active Task

**Task**: Developer implementation — Bounded same-onset chord grouping in `notation_bridge.py`
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## Status

APPROVED

## Executable Task

Yes

## 1. Baseline
- Product PR #336 merged at `cae6a416076e66f6b84940ad0cbf3061beb241d9`.
- Governance PR #240 merged at `9c4ec0e7c98ffc923d7ac347f55e9e8a0a6b12cd`.
- Architecture approval: Reviewer architecture re-verification approved PR #240 at head `6cd939eccb8889b1867c91b4c4d17eb0d6c6786f`.

## 2. Context
PR #240 architecture research identified same-onset chord grouping in `notation_bridge.py` as the smallest next implementation task. Currently, `notation_bridge.py` sequentially increments onsets for all note candidates, which causes overlapping chord notes to be serialized, violating timing and exceeding measure limits. The Developer will implement chord grouping to address this blocker. The GP writer is verified to support multiple notes in a single event as a chord (iterating over `event.notes` in `gpif.py` lines 1819-1820).

## 3. Scope
- **Approved**: Same-onset chord grouping in `src/score2gp/notation_bridge.py` for eighth/sixteenth note candidates so horizontally aligned same-onset candidates become one ScoreIR `Event` containing multiple `Note` objects. Candidates may be grouped into a single chord Event only when they share the same page identity, system identity, staff index identity, and have horizontal onset/x coordinates within a tolerance of 1.0 point. Candidates with the same x/onset coordinate but different page, system, or staff context must remain separate events. Bridge-level tests in `tests/test_notation_bridge.py` must prove timing, duration, and no cumulative 4/4 overflow for valid chord inputs.
- **Excluded**: True polyphony, same-staff multi-voice support, voice separation, multiple independent rhythmic voices, OMR candidate extraction changes, staff geometry changes, new PDF fixtures, committed `.gp` artifacts, and real-world score support claims.

## 4. Required Output & Outcome
Implementation of chord-grouping in `src/score2gp/notation_bridge.py` and comprehensive unit and integration tests in `tests/test_notation_bridge.py` verifying:
- same-onset candidates in the same page/system/staff context are grouped into one Event;
- candidates with the same x/onset coordinate but different page identity are not grouped;
- candidates with the same x/onset coordinate but different system identity are not grouped;
- candidates with the same x/onset coordinate but different staff index are not grouped;
- non-aligned sequential candidates remain sequential;
- existing eighth/sixteenth duration mapping remains intact;
- valid same-context chord inputs do not raise `cumulative_duration_exceeds_one_4_4_bar`.

## 5. Artifact & Privacy Constraints
- No private score PDFs or copyrighted music may be processed.
- No generated PDFs or GP files may be committed to git.
- Product working tree must remain clean.

## 6. Required Next Review
Reviewer implementation conformance review and PR readiness review.
