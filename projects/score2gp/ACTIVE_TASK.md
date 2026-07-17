# Active Task

**Task**: CR-03A: Local tuplet-group evidence and meter resolution - Architect Phase
**Authorised Role**: Architect
**Repository**: `tticom/score2gp` (product) and `tticom/score2gp-agentops` (governance)

## Status

APPROVED

## Task Authorised

Yes, Tier 1 Architect phase authorized:
- Read-only product inspection (`score2gp` and `score2gp-recovery`).
- Read-only corpus/fixture inspection.
- Drafting of the local tuplet-group association rules and architecture report.
- Drafting of the public synthetic-fixture design.

## Permissions and Boundaries

- All product workspace access (`score2gp` and `score2gp-recovery`) must be strictly **READ-ONLY**.
- Modification of product code, product tests, product branches, opening product PRs, or performing product merges is **STRICTLY FORBIDDEN**.
- Working on governance documents under the `score2gp-agentops` repository is permitted.

## Completion Evidence

1. A comprehensive Architect report is written detailing the local tuplet-group association rules (associating tuplets to exactly one local group of three rhythmic events using geometry and grouping evidence).
2. The report specifies the adversarial synthetic test fixture design (containing true tuplet `3` marks, TAB fret `3` digits, measure label `3` headers, and unrelated text containing the digit `3`).
3. Explicit independent Reviewer approval of the Architect design is required before any Developer work may start.
