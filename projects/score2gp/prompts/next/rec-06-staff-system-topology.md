# REC-06 — Staff and System Topology

Status: SKELETON — depends on REC-04 and REC-05
Role: Developer
Repository: `score2gp`

## Objective

Reconstruct pages, reading order, systems, staff regions, notation/TAB pairings
and stable identities from observations.

## Required work

1. Consume observations and scale estimates only through their interfaces.
2. Represent competing staff groupings and pairing support.
3. Support conventional notation, six-string TAB and paired instructional layouts.
4. Return Unsupported or Ambiguous for inadequate layouts.
5. Expose no measure, duration, pitch or final-event semantics.

## Acceptance and falsification

- Disconnected systems cannot cross-snap.
- Titles, diagrams and horizontal noise do not become supported staves.
- At least two structurally distinct private scores have stable identities.

## Validation

Promoted prompt must use the REC-01 topology oracle and include adversarial
negative regions from provenance-linked real-source extractions.

