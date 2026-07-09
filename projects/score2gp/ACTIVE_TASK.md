# Active Task

**Task**: Req-121 / Task 54: Implement fail-closed semantic coverage expansion
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## Status
APPROVED

## Task Authorised
Yes

## Completion Evidence
Developer must expand semantic candidate extraction coverage to verify fail-closed handling on complex rests (whole rests, half rests) and overlapping/polyphonic geometry clusters.

## 1. Baseline
- The semantic candidate CLI/reporting path (Req-120) has been implemented, tested, and merged.
- We need to expand candidate extraction coverage and verify that the heuristics fail closed safely under complex rests and polyphonic collisions.

## 2. Context
Real-world scores frequently introduce whole rests, half rests, and polyphonic collisions where multiple voices share vertical space. We need to implement and test heuristics that safely ignore these structures (fail-closed) to protect downstream interpretation from invalid quarter-rest or clef classifications.

## 3. Goal
Create synthetic tests and expand heuristics to prove that whole rests, half rests, and overlapping/polyphonic geometry clusters are safely ignored (fail closed).

## 4. Non-goals
- Do not add pitch or rhythmic duration inference.
- Do not build ScoreIR events.
- Do not guess or map ambiguous symbols.

## 5. Required Output & Outcome
A product PR with test coverage and safe heuristics implementing the fail-closed boundary.

## 6. Next Steps
- Promote the next valid task, likely Req-122, after Req-121 is reviewed and merged.
