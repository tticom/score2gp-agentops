# Antigravity Task: GPIF Hammer/Pull/Slide Minimal Round-Trip v0.1

## Role

You are the Developer.

Implement the smallest safe product change that makes hammer-on and pull-off techniques survive a GPIF write/read round trip. Use slide as a regression guard because research indicates slide is already written and recovered.

This is not a broad guitar-technique preservation branch. Do not implement PDF proximity assignment, palm mute, let ring, or slur recovery in this branch.

## Current verified state

Recent validation on main:

- Public tests: 442 passed.
- Private audit:
  - Lessons 3–7 pass as `gp_output_technique_loss_expected`.
  - Melodic soloing passes as `gp_output_fret_matching_suspect` with 16 matched notes.
- Private-safety invariant:
  - `git ls-files fixtures/private work` outputs exactly `fixtures/private/.gitkeep`.

Research finding:

- Hammer-on and pull-off are extracted from PDF text candidates, mapped to ScoreIR, and serialized to GPIF.
- Hammer-on and pull-off are lost when GPIF is parsed back to ScoreIR.
- Slide is serialized and recovered, so it should be used as a regression guard.

## Branch

Create from current main:

```bash
git switch main
git pull --ff-only origin main
git switch -c feature/gpif-hammer-pull-slide-minimal-v0.1
```
