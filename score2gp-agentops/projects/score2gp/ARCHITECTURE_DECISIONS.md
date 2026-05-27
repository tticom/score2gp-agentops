# ScoreToGP Agent-Ops Architecture Decisions

## ADR-001: Keep Agent Control Outside Product Code

Decision: agent-control artifacts live in `score2gp-agentops`, not inside ScoreToGP product source.

Reason: product correctness is separate from agent-control prose. The product repository should remain focused on source code, tests, schemas, fixtures, and user-facing docs.

## ADR-002: Use A Benchmark Ladder

Decision: ScoreToGP evaluation follows a ladder from simple controlled GP-originated PDFs to noisy real-world scores.

Reason: early acceptance targets need controlled evidence. Stress cases are useful, but they should not become the first acceptance target.

## ADR-003: Require Separate Result Channels

Decision: strict mode, remediation mode, semantic comparison, and generated-file existence must always be reported separately.

Reason: these fields answer different questions. Combining them hides failure modes and can create false confidence.

## ADR-004: Reviewer Evaluates Before Prompting

Decision: the reviewer/architect agent must evaluate the current evidence before writing the next implementation prompt.

Reason: next prompts should be driven by observed failures, not by assumed progress.

## ADR-005: Evidence Hierarchy

Decision: visual/source evidence outranks generated summaries, and diagnostic tables are evidence, not truth.

Reason: generated summaries and tables can omit, smooth over, or misclassify the actual conversion behavior.

## ADR-006: Private Assets Stay Private

Decision: private PDFs, images, exports, and derived confidential benchmark artifacts must never be committed.

Reason: private benchmark access is a local maintainer privilege, not a repository asset.

## ADR-007: Stress Cases Are Research Inputs

Decision: the Derek Trucks stress/research case is a later-rung diagnostic case, not an initial acceptance target.

Reason: hard noisy cases are valuable for understanding system limits, but they can obscure foundational correctness work.
