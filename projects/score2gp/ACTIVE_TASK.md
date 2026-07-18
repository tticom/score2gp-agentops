# Active Task

**Task**: CR-03A: Local tuplet-group evidence and meter resolution - Developer Phase
**Authorised Role**: Developer
**Repository**: `tticom/score2gp` (product) and `tticom/score2gp-agentops` (governance)

## Status

APPROVED

## Task Authorised

Yes, Tier 1 Developer phase authorized:
- Implementation of the local tuplet-group association rules and synthetic extraction fixture in the product repository (`score2gp`), as detailed in the Architect report and approved by the Reviewer.
- Must follow Clean-Base rule: product branch must start from `origin/main`.

## Permissions and Boundaries

- All work must be strictly constrained to implementing the approved CR-03A local geometric tuplet association rule.
- Product workspace access (`score2gp`) is now authorized for **READ AND WRITE**.
- Modification of product code, product tests, product branches, and opening product PRs is **PERMITTED**.
- Merging product PRs remains **STRICTLY FORBIDDEN** (human merge only unless otherwise authorized).

## Completion Evidence

1. Product code correctly extracts and identifies the genuine tuplet mark and ignores adversarial labels.
2. Synthetic unit tests cover 4/4 triplets, 6/8, and 12/8 as specified.
3. Tests pass, and a product PR is open against `score2gp`.
4. Governance PR updated with the completion evidence.
