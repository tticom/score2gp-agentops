# Active Task: Architect Research on Tab-Only Rhythm Inference

## Repository
tticom/score2gp

## Goal
Perform an Architect research decision gate to determine whether Score2GP can infer rhythm for tab-only PDF input using deterministic evidence from raster/vector/tab geometry, with enough reliability to justify implementation.

## Progress Baseline
* **Product PR #323 merged**: `feat: tab-only quarter rest candidate wiring`
  * Merge commit: `6afdd3195f37eca6e319caf33dbeccfbbf1d4b5c`
  * Baseline capability: Tab-only quarter-rest candidate support is now merged and wired into `--pdf-only-tab`.
* **Governance Decision**: `projects/score2gp/decisions/2026-06-24-post-pr323-tab-only-rhythm-inference-gate.md` records PR #323 completion and blocks Developer work on rhythm inference until architecture is approved.

## Active Blocker
The active blocker is no longer "can we recognise tab-only quarter rests?". That is baseline capability.
The active blocker is: **Can Score2GP infer rhythm for tab-only PDF input using deterministic evidence from raster/vector/tab geometry, with enough reliability to justify implementation?**
General tab-only rhythm inference remains unimplemented. Whole, half, eighth, and sixteenth rests remain unsupported.

## Explicit Scope & Acceptance
* The next authorised task is **Architect research only**. Developer implementation is blocked.
* The Architect must produce exactly one of the following outcomes:

  * **Outcome A**: The current deterministic raster/vector/tab-geometry path is viable for tab-only rhythm inference on a defined fixture set.
  * **Outcome B**: The current deterministic path is not viable, but another concrete non-ML approach is viable.
  * **Outcome C**: No credible deterministic or non-ML path is currently viable. The project must stop or pivot.

## Constraints and Preservation
* Do not perform Developer implementation.
* Do not modify product code, tests, or fixtures.
* Do not commit private PDFs, GP files, screenshots, logs, diagnostic dumps, or local scratch files.
* Developer work remains blocked until Reviewer architecture verification approves Outcome A or B.
