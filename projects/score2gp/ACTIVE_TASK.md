# Active Task

**Task**: CR-03C: Revert CR-03A unauthorized scope - Developer Phase
**Authorised Role**: Developer
**Repository**: `tticom/score2gp` (product) and `tticom/score2gp-agentops` (governance)

## Status

APPROVED

## Task Authorised

Yes, Tier 2 implementation phase authorized for product integrity restoration.

## Permissions and Boundaries

- Do not start CR-04A or any new product feature work.
- Branch from current product `origin/main` to `cr-03c-revert`.
- Execute `git revert 40d061517523fcfe714d49c3aa4e7b3191d56a80 --no-commit`.
- Allowed files: `src/score2gp/whole_note_recogniser.py`, `src/score2gp/cli.py`, `src/score2gp/pdf_staff_geometry.py`, `src/score2gp/pdf_staff_notation_diagnostics.py`, `tests/test_pdf_only_tab.py`, `tests/test_tuplet_association.py`.
- Do not import recovery branches or PRs #371/#372.
- Do not modify other files or perform any other edits.

## Completion Evidence

1. Product tests (`pytest tests/`) must pass.
2. A separate independent Reviewer approves the revert PR based on exact adherence to the allowed-file list and the `git log` proving a clean revert.
3. The revert PR is squash-merged to `origin/main`.

## Unattended Continuation

This task opts into the Visual Output Correctness Recovery Programme's
Unattended Consecutive Loop Protocol. After review, rework, or guarded merge,
agents must continue to the next required role or eligible task without routine
maintainer confirmation. Before a genuine stop, they must commit the required
human-focused end-of-run report in AgentOps.
