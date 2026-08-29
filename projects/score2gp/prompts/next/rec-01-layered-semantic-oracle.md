# REC-01 — Layered Semantic Oracle

Status: SKELETON — depends on REC-00
Role: Developer
Repository: `score2gp`

## Objective

Build a reference-isolated, read-only oracle reporting first divergence at
topology, TAB-token, ownership, onset, rhythm, measure and score layers.

## Required work

1. Pin the accepted REC-00 contracts and exact known-bad revisions.
2. Run generation in a process that cannot receive reference GP paths or data.
3. (Deferred) Evaluate generated output afterward against approved private references. This PR is an infrastructure setup only.
4. Emit typed per-layer results plus first divergence and NOT_EVALUATED reasons.
5. Add mutation/revision probes proving each claimed guard turns red.

## Acceptance and falsification

- Lesson 5 and Lesson 6 are validation inputs, never generation inputs.
- Aggregate counts cannot yield a pass when ordered events differ.
- Corpus absence cannot satisfy productive acceptance, but this task is explicitly permitted to be infrastructure-only and make no real-source correctness claim. Governance accepts a basic infrastructure review.
- At least two historical destructive behaviours are detected.

## Validation

Use the commands promoted from REC-00; they must include targeted public tests,
private reference-isolation execution and `scripts/artifact_audit.py`.

