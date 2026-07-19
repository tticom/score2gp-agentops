# Active Task

**Task**: FS-01R: Remediate invalid FS-01 merge (#376) - Developer Phase
**Authorised Role**: Developer
**Repository**: `tticom/score2gp` (product) and `tticom/score2gp-agentops` (governance)

## Status

APPROVED

## Task Authorised

Yes. This narrow remediation is authorized before the Runtime-Provenance and
Functional-Stabilisation Programme may resume.

## Permissions and Boundaries

- Start from `origin/main` in the product repository. Do not use any historical
  branch or uncommitted implementation as a baseline.
- Implement only FS-01R as defined in
  `projects/score2gp/programmes/2026-07-19-runtime-provenance-functional-stabilisation.md`.
- Create exactly one normal product revert PR for the merge commit that merged
  product PR #376. Do not salvage, rewrite, extend, or reimplement #376.
- The revert must contain no unrelated change and must restore the pre-#376
  product behaviour. Run the focused tests affected by the reverted files and
  `git diff --check`.
- Obtain a distinct Reviewer verdict and address review findings with normal
  follow-up commits. Agy must never merge the product PR, merge a governance
  PR, use `gh pr merge`, use `--admin`, or push directly to `main`.

## Completion Evidence

1. The PR explicitly reverts the merge commit for product PR #376 and changes
   no unrelated file.
2. Focused public tests and `git diff --check` pass.
3. A distinct Reviewer verifies the exact PR head and records whether the
   revert is complete and narrow.
4. The PR is marked `READY_FOR_EXTERNAL_MERGE` with its exact head SHA;
   FS-01 remains blocked until an external maintainer merges it.

## Unattended Continuation

This task opts into the Unattended Consecutive Loop Protocol for developer and
review rework only. After acceptance, Agy must prepare the external-merge
handoff and may continue only with an independent approved task. It must not
advance FS-01 until an external maintainer merges the revert.
