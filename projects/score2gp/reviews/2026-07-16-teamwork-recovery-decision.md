# Decision: Recover From the Failed Teamwork Branch

## Decision

Freeze `feature/teamwork-corpus-conversion-accuracy-v0.1` for forensic review.
Use `recovery/pre-teamwork-score-output-baseline-v0.1` at `e70bddaa` for the
next product task.

## Evidence

The failed branch is 1,963 added lines across 15 files beyond `e70bddaa` and
has introduced visible accidental/technique regressions without delivering the
requested layout/title improvement. Its generated artifacts also repeatedly
pollute the product root and `tmp/`.

## Scope of the recovery task

- establish a fresh no-reference baseline from the recovery branch;
- preserve failed work without merging, deleting, resetting, or cherry-picking
  it by default;
- implement at most one source-layout propagation fix with an end-to-end
  positive and negative test;
- exclude accidental, key, duration, chord, and embellishment changes.

## Success condition

The task restores a trustworthy evidence loop. It must report the first
remaining visible mismatch rather than claiming whole-score success.
