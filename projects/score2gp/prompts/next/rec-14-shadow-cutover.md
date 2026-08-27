# REC-14 — Shadow Mode, Calibration, Cutover and Legacy Retirement

Status: SKELETON — depends on REC-01 and REC-13
Role: Architect followed by separately promoted Developer tasks
Repository: `score2gp`

## Objective

Prove the replacement in shadow mode, calibrate selective acceptance, authorize
only supported input classes, and retire legacy recognition incrementally.

## Required work

1. Run legacy and replacement paths on identical source inputs without reference
   feedback; compare afterward through REC-01.
2. Define per-measure and per-score risk/coverage policy on held-out inputs.
3. Record cutover criteria per input class and a rollback-compatible seam.
4. Delete legacy code only in bounded successor PRs after red/green replacement
   evidence and independent review.
5. Evaluate learned relation models only after an annotated graph dataset,
   deterministic baseline, offline model provenance and calibration plan exist.

## Acceptance and falsification

- No average confidence threshold can hide a hard contradiction.
- Cutover requires productive correctness across at least two distinct scores.
- Refusal-only success cannot authorize an input class.
- Audiveris or other legacy dependencies are deleted only when no supported path
  or diagnostic contract still requires them.

## Validation

The promoted architecture task must split shadowing, calibration, cutover and
deletion into independently reviewable PRs with exact corpus and stop criteria.
