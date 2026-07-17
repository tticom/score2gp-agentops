# Active Task

**Task**: Task 92: Hardened Import Verification and CLI Layout Auto-Fallback
**Authorised Role**: Developer, Architect, Reviewer, and Project Director
**Repository**: `tticom/score2gp`, `tticom/score2gp-agentops`, and the approved local fixture repository

## Status

APPROVED

## Task Authorised

Yes, branch and PR work authorized.

## Reason For This Promotion

The deep root-cause research identified two immediate deployment and observability blockers:
1. Virtual environment package import mismatch.
2. Auto-OMR timing refusal on born-digital TAB-only PDFs due to 0 standard notation staves.

Task 92 will implement import-checking protection and a safe TAB-only handling
path. It must not turn an unsafe approximate extraction into a normal strict
conversion merely because no standard notation staves were detected.

## Start State

- Canonical product worktree: `/home/tticom/work/score2gp-workspace/score2gp` on `feature/teamwork-corpus-conversion-accuracy-v0.1` at `34b7c2e5` (frozen).
- Recovery worktree: `/home/tticom/work/score2gp-workspace/score2gp-recovery` on `feature/task-90-source-metadata-trace-fail-closed` at `fdaee5e4`.
- Research report and evidence ledger committed in `score2gp-agentops`.

## Permissions and Boundaries

- Tier 2 branch and PR work.
- Allowed product files to modify in `score2gp`:
  - `src/score2gp/cli.py`
  - `scripts/import_check.py` [NEW] or similar helper scripts
  - `tests/` for verification
- Do not modify pitch, duration, rests, ties, key signatures, or embellishment logic.
- Keep all modifications minimal and focused on import verification and TAB-only auto-fallback.
- The existing PR #371 is blocked by review. It is not eligible for merge in
  its current form.

## Reviewer Correction

A fresh source-first run of the proposed Masterclass fallback returned
`status=success`, `stage=gp-write`, and `strict=true` while its own diagnostics
reported `pdf_timing_mapping_not_implemented`, `partial_pdf_grouping`,
`pdf_grouping_not_safe_for_build_ir`, and
`pdf_layout_detection_requires_manual_review`. This is a release-blocking false
success.

The PR also compares 40 files and more than 5,000 additions against `main`,
including Task 89/90 changes outside this task. It is not a focused Task 92 PR.

Required correction:

1. Normal `convert` must remain refused when grouping or timing is unsafe.
2. An approximate tab-only artifact, if retained, must require explicit user
   consent through a clearly named draft/approximate option and must report its
   mode and missing timing evidence in JSON and HTML output. It must never be
   represented as a strict success.
3. Add public structured tests for both paths: unsafe normal conversion refuses;
   explicit approximate conversion is marked as such.
4. Recreate the product PR as a focused branch based on an approved parent, or
   retain it as an explicitly stacked non-mergeable PR. Do not merge prerequisite
   recovery work under Task 92.

## Completion Evidence

1. A verification script or CLI check validates that Python imports from the local recovery workspace.
2. A normal conversion of an unsafe TAB-only PDF refuses with a precise stage
   and remediation. No GP package is written.
3. Any explicitly requested approximate TAB-only conversion is visibly marked
   as approximate in the report and cannot claim strict timing correctness.
4. Public tests, focused product tests, `python scripts/agent_verify.py`, and
   `git diff --check origin/main...HEAD` are clean at the exact PR head.
