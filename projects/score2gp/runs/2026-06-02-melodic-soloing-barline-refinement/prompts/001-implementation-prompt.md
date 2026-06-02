# Antigravity Task: Melodic Soloing Barline Refinement v0.1

## Pre-Flight Merge Check

Before writing code or creating a branch, verify that the recent product and governance PRs are merged and local workspaces are synced.

Run in `score2gp`:

```bash
gh pr view 156 --web=false
git switch main
git pull --ff-only origin main
python -m pytest
python scripts/private_e2e_smoke.py
python scripts/private_gp_quality_audit.py
```

Run in `score2gp-agentops`:

```bash
gh pr view 19 --web=false
git switch main
git pull --ff-only origin main
```

Proceed only if:

* `score2gp` PR #156 is merged.
* `score2gp-agentops` PR #19 is merged.
* Both local `main` branches are clean and up to date.
* Public tests pass.
* Private smoke/audit can run without committing private artifacts.

If any condition fails, stop and report the exact state. Do not create a branch.

## Branch

Create in `score2gp`:

```bash
git switch -c feature/melodic-soloing-barline-refinement-v0.1
```

## Context

The Bar Alignment Quality Gate v0.1 corrected a parser-level defect where non-musical `<Automation><Bar>` tags were counted as musical bars.

Current private-safe quality audit status:

* Lessons 3–7:
  * true musical GPIF bars align with ScoreIR bars
  * final classification: `gp_output_technique_loss_expected`
  * remaining limitation: guitar technique serialization is not yet implemented

* Melodic soloing:
  * true musical GPIF bars align with ScoreIR bars
  * final classification: `gp_output_empty_or_near_empty`
  * 59 playable fret candidates remain unmatched
  * output has 0 matched notes
  * suspected cause: layout/barline drift and x-to-onset mapping failure

This branch targets the melodic soloing empty-output blocker only.

## Goal

Investigate and fix the melodic soloing score's barline/layout/onset mapping so playable fret candidates can be matched into ScoreIR and serialized into non-empty GPIF output.

The target is not full musical perfection. The target is correct-enough geometry, plausible bar/onset mapping, non-empty notes, and no regression in Lessons 3–7.

## Acceptance Criteria

This branch is complete when:

1. The first failing stage for melodic soloing is identified.
2. Public tests cover the diagnosed defect class.
3. Melodic soloing no longer silently produces empty GP output if a safe fix is possible.
4. If non-empty output is not safely achievable, the branch emits a clear private-safe first-failing-stage diagnostic.
5. Lessons 3–7 do not regress from `gp_output_technique_loss_expected`.
6. The bar-alignment quality gate remains strict.
7. Full public tests pass.
8. Private smoke and audit run cleanly.
9. No private files or `work/` artifacts are committed.

## Validation Commands

Run:

```bash
python -m pytest
python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json
python scripts/private_e2e_smoke.py
python scripts/private_gp_quality_audit.py
git diff --check
git ls-files fixtures/private work
```

Expected private-safety invariant:

```text
fixtures/private/.gitkeep
```
