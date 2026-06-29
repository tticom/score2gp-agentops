# Active Task

**Task**: Supervisor Fixture-Ingestion / Artifact-Boundary Approval Decision
**Authorised Role**: Supervisor
**Repository**: `tticom/score2gp-agentops`

## 1. Baseline
- Product PR #333 merged (commit `b38c0acc9c284379dcd0f82316db08c3fc6211ec`).
- Prior governance (`projects/score2gp/decisions/2026-06-27-safe-natural-fixture-candidate-approval.md`) selected the Mutopia A4 PDF as a candidate, requiring a Supervisor-approved fixture ingestion decision before diagnostic use.
- A diagnostic run on Mutopia A4 produced evidence indicating basic whole-note heuristics are unsafe (>120 false positives), but this run lacks a durable artifact-boundary governance approval record.
- Whole-note rule-based Developer implementation remains formally blocked.

## 2. Active Blocker
Outcome C (and subsequent OMR/CV Architecture Research) is deferred and not yet durable because the diagnostic evidence relies on a fixture that has not yet passed a formal artifact-boundary / fixture-ingestion governance approval.

## 3. Authorised Scope
The Supervisor must decide to:
- Approve the ingestion and diagnostic use of the pinned Mutopia A4 PDF; OR
- Reject it and require an alternative approved false-positive fixture strategy.

## 4. Non-Goals
- Do not authorise OMR/CV Architecture Research from unapproved evidence.
- Do not run or validate the diagnostic until the boundary is approved.
- Do not authorise Developer implementation.

## 5. Required Evidence
- A formal governance decision recording the approval or rejection of the Mutopia A4 fixture ingestion.

## 6. Stop Conditions
- Stop if the artifact boundary is bypassed to authorise product work.

## 7. Next Required Review
PR readiness review for the Supervisor decision record.
