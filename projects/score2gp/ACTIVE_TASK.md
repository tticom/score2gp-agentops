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

Task 92 will implement import-checking protection and automatically fall back to `--pdf-only-tab` draft mode when no standard notation staves are detected on a vector TAB PDF, enabling out-of-the-box conversion of `Melodic Soloing Masterclass.pdf`.

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

## Completion Evidence

1. A verification script or CLI check validates that Python imports from the local recovery workspace.
2. The CLI successfully converts `Melodic Soloing Masterclass.pdf` automatically without requiring manual `--pdf-only-tab` flag under the default `convert` command form.
3. Tests and `python scripts/agent_verify.py` are clean.
