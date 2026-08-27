# REC-00 — Recognition Domain Contract and Supersession Ledger

Status: SKELETON — promote separately before execution
Role: Architect
Repository: `score2gp-agentops`

## Objective

Define the recognition ubiquitous language, module seams, stage invariants,
failure taxonomy and auditable supersession map. This task changes governance
and design truth only; it must not change product behaviour.

## Required work

1. Read the recognition backlog, conversion-recovery programme, NPG-00R decision,
   and current product types at the exact main revisions.
2. Create `projects/score2gp/CONTEXT.md` as an implementation-free glossary.
3. Record the selected hybrid vector/raster, topology-first architecture and
   rejected alternatives in `decisions/recognition-architecture-v1.md`.
4. Verify each prior pending task has one explicit disposition and replacement.
5. Propose REC-01 without promoting or executing it.

## Acceptance and falsification

- Every canonical term has one meaning and one owning stage.
- Observation contracts cannot contain musical assignments.
- Completed history remains intact.
- Fail if any unresolved term would change a downstream schema.

## Validation

`git diff --check`
`python3 scripts/score2gp_governance_audit.py`
`python3 -m pytest -q tests/test_score2gp_orchestrator.py tests/test_governance_audit.py`

