# Active Task

**Task**: Req-112 / Task 40: Implement semantic boundary validation gate
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## Status
APPROVED

## Executable Task
Yes

## Completion Evidence
Developer must implement the semantic boundary validation gate (checking for a logical clef candidate from the left margin) based on the Architect's proposal in `docs/testing/standard-staff-semantic-boundary.md`. 

## 1. Baseline
- Req-111 / Task 34 architecture proposal was merged in product PR #347.
- The Reviewer approved the semantic boundary proposal in governance PR #263.
- The smallest safe semantic unit identified is the Logical Clef from `left_margin_primitives`.

## 2. Context
We are now entering Epic C (Semantic Boundary Definition & Core Interpretation). Before we can reliably extract pitches, we must formally transition from purely geometric candidates to semantic interpretation. The first step is to implement a validation gate that attempts to parse a Logical Clef from the isolated `left_margin_primitives`.

## 3. Active Blocker
Subsequent tasks (like mapping pitch) are completely blocked until the semantic boundary (the clef) is reliably extracted.

## 4. Goal
Create the foundational logic that transitions `left_margin_primitives` into a `LogicalClefCandidate` (or similar semantic structure), proving we can safely interpret a known glyph (e.g., treble clef) without inferring pitches or rhythms yet.

## 5. Non-goals
- No pitch, duration, rhythm, voice, key signature, or time signature inference.
- No rests (quarter/whole) interpretation yet.
- Do not modify existing `GeometryCandidateSet` models; map from them instead.

## 6. Repo Scope
- **Allow**:
  - `src/score2gp/pdf_candidate_semantic_gate.py` (or similar new/existing modules)
  - `tests/test_pdf_candidate_semantic_gate.py`
- **Stop before changing**:
  - `ACTIVE_TASK.md` (once authorised)

## 7. Branch Suggestion
`feature/logical-clef-semantic-boundary-v0.1`

## 8. Required Output & Outcome
A product PR implementing the logical clef extraction and a passing test suite proving >90% reliability on public standard-staff fixtures.

## 9. Incremental Progress Check
- **What new evidence will this task produce?**: Tests proving a logical clef is identified from geometry.
- **Which prior result must it not merely repeat?**: Must generate a semantic `LogicalClefCandidate` instead of just returning raw geometric boundaries.
- **How will we know the task moved the project forward?**: A PR is opened with the new semantic parsing logic.
- **What is the smallest next decision this task enables?**: Extracting subsequent elements that depend on the clef, such as pitches or quarter rests.

## 10. Next Steps
- Promote the next available Epic C task (e.g., Req-113 Logical clef recognition candidate integration or Req-114 Quarter rest extraction).
