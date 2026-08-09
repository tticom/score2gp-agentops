# CRP-06 — Source Modality and TAB Recognition

Status: SKELETON — not executable.

## Dependencies

accepted CRP-03 oracle

## Objective

Resolve embedded-text, vector, and raster evidence per page and compare recognition adapters on held-out real-source material.

## Fields required before promotion

- TBD_FROM_ARCHITECTURE: exact product base, module interface, invariants, and allowed files.
- TBD_FROM_REAL_ORACLE: fixture manifest revision, source hashes, expected bar/event contract, and known-bad SHA.
- TBD_FROM_RESEARCH: selected technology, version, license, privacy, and stop or pivot decision where relevant.
- TBD_FROM_REVIEW: accepted predecessor PRs and unresolved risks.
- TBD_FROM_GOVERNANCE: identity, branch, validation commands, delivery action, and exact non-goals.

## Testing rule

Behavioural evidence must use whole real-world private fixtures or
provenance-linked extractions from them. Synthetic or mocked musical evidence
cannot satisfy acceptance. A skipped private suite is NOT_EVALUATED. Generation
must not receive the reference GP path.

## Provisional acceptance

Select adapters using confusion matrices for frets, fingering digits, labels, tempo text, and nearby numeric glyphs; no opaque training.

The final prompt must also require a reviewer-created counterexample, full
artifact/privacy audit, fresh no-reference conversion, first remaining
mismatch, and an exact-head handback.
