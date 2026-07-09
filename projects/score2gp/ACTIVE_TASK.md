# Active Task

**Task**: Req-119 / Task 50: Implement semantic candidate JSON snapshot tests
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## Status
APPROVED

## Task Authorised
Yes

## Completion Evidence
Developer must implement deterministic public JSON snapshot tests for current semantic candidate outputs:
- logical clef candidate outputs
- quarter rest candidate outputs

## 1. Baseline
- The logical clef recognition (Req-113) and quarter rest extraction (Req-114) are fully implemented, tested, and merged.
- They extract semantic candidates but we lack deterministic JSON snapshot tests to prevent regressions on these parsed candidates.

## 2. Context
We need to harden the observability of these semantic candidates by creating deterministic JSON snapshot tests for `QuarterRestCandidate` and `LogicalClefCandidate` outputs, mirroring the safety nets we built for primitive geometry in Req-105.

## 3. Goal
Create a test suite in `score2gp` that serializes the extracted semantic candidates (`LogicalClefCandidate`, `QuarterRestCandidate`) from the public fixtures and compares them to checked-in JSON snapshots.

## 4. Non-goals
- Do not add pitch, rhythm timeline, ScoreIR mapping, duration inference, or private fixtures.
- Do not modify the existing extraction logic or rules.
- Do not guess or infer missing structural features.

## 5. Required Output & Outcome
A product PR containing the snapshot test implementation, the JSON snapshot fixtures, and passing test runs.

## 6. Next Steps
- Promote the next valid task, likely Req-120 (Semantic candidate CLI/reporting smoke path), after Req-119 is reviewed and merged.
