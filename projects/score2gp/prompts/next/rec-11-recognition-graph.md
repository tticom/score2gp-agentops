# REC-11 — Recognition Graph Assembler

Status: SKELETON — depends on REC-08, REC-09 and REC-10
Role: Developer
Repository: `score2gp`

## Objective

Assemble observations, topology and recognition hypotheses into a typed,
provenance-preserving graph with bounded candidate relations.

## Required work

1. Implement the relation vocabulary accepted by REC-00/02.
2. Generate relations deterministically from spatial and topological context.
3. Encode conflicts and competing alternatives explicitly.
4. Spatially/topologically prune pair generation and report complexity metrics.
5. Do not resolve final musical semantics in this module.

## Acceptance and falsification

- Every node and edge traces to source evidence or a versioned derivation.
- Dangling references and cross-system illegal relations fail validation.
- Dense pages remain within the promoted performance envelope.

## Validation

Require graph schema validation, deterministic snapshots from real-source
observations, relation negative controls and measured candidate-pair growth.

