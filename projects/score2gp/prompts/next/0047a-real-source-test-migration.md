# CRP-04 — Real-Source Test-Suite Migration

Status: SUPERSEDED by REC-01 — historical prompt, not executable.

## Dependencies

Accepted CRP-02 testing architecture and CRP-03 real-source oracle.

## Objective

Inventory every current product test by claim, production path exercised, and
data provenance. Replace synthetic behavioural false oracles with whole
real-world fixtures or provenance-linked cases extracted from approved private
PDFs. Quarantine and delete a legacy false oracle only after its replacement is
red on the exact known-bad implementation and green on the accepted one.

## Required outputs before implementation

- TBD_FROM_ORACLE: private manifest and result schema revision.
- TBD_FROM_INVENTORY: test path, claim, data source, bypassed production stages,
  known-bad mutation, replacement fixture case, and disposition.
- TBD_FROM_PRIVACY: ownership of extracted cases and CI credential boundary.
- TBD_FROM_ARCHITECTURE: permitted product and private-repository paths.
- TBD_FROM_REVIEW: independently accepted migration batch.

## Rules

- No synthetic geometry, IR, MusicXML, bar, event, fret, or timing data may
  prove conversion behaviour.
- Pure serialization and schema tests may remain only when their claim is
  explicitly non-musical.
- Refusal tests remain safety checks and require paired productive evidence.
- Missing private execution is NOT_EVALUATED, not PASS.
- Do not mass-delete tests. Migrate in reviewable batches grouped by one
  production seam.

## Provisional acceptance

Every synthetic behavioural test has a recorded disposition and dependency.
The first migration batch replaces one false-oracle family, proves its
known-bad disconfirmation, runs non-skipped on the private corpus, and leaves
full validation and artifact audits clean.
