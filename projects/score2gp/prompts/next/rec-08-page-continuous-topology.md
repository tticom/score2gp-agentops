# REC-08 — Page-Continuous Topology

Status: SKELETON — depends on REC-07
Role: Developer
Repository: `score2gp`

## Objective

Create stable page-continuous system and measure identities without mutable
running indexes or coordinate-offset leakage.

## Required work

1. Define deterministic reading-order and continuation relations.
2. Derive global identities from topology rather than caller-maintained counters.
3. Preserve page-local coordinates and page identity.
4. Represent ambiguous continuations explicitly.
5. Add a compatibility projection for consumers requiring sequential bar indexes.

## Acceptance and falsification

- Page reprocessing order cannot silently renumber accepted topology.
- Missing pages and alternative page sizes fail or remain explicit.
- Lesson 6 continuity is evaluated semantically, not by a hard-coded count.

## Validation

Use REC-01 boundary and complete-measure layers on at least two multipage scores.

