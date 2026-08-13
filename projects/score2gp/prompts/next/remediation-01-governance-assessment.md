# Remediation 01 — Governance Assessment on Review Skills Failure

Status: SKELETON

## Role
tticom-codex (Reviewer / Governance)

## Context
The Devil's Advocate review on `main` HEAD (`7de1d0b`) discovered that recent implementations from CRP-10, CRP-11, and CRP-12 introduced severe architectural regressions and silent data corruption fallbacks despite a "green" test suite. The governance loop and specifically the `devils-advocate-review` skill is supposed to prevent this from happening. 

The violations that slipped through are:
1. **Synthetic Note Injection (CRP-12)**: `ScoreIRCompiler` claims to strictly refuse synthetic note generation, but when it encounters unowned notes, it silently generates and injects a fake `(string=1, fret=0)` note. This produces musically corrupt output instead of refusing the compilation.
2. **Fundamentally Flawed Chord Heuristics (CRP-11)**: `BiomechanicalPositionOptimizer` evaluates fingering costs purely sequentially. This completely breaks down for simultaneous notes (chords), treating them as a sequence of extreme physical hand jumps rather than a single hand shape.
3. **Partition Hacks Remaining (CRP-10)**: `TopologicallyLockedBarTimeline` claims to enforce capacity invariants without hacks, but it silently truncates overlapping same-voice notes and pads misaligned measures with synthetic `padding_rest` data.
4. **False Security in Tests**: Private integration tests use `pytest.skip` when the private fixture is missing, meaning the CI runs "green" without ever testing real PDF data. The isolation tests are meaningless mocks, and successful generation checks only assert that the output `.gp` file has a size greater than 0 with no semantic checks.

## Goal
Perform a governance assessment on why the `devils-advocate-review` skill failed to catch these P1 issues during the review of CRP-10, 11, and 12. 
Identify gaps in the current review prompts, test execution rules, and evidence verification mechanisms. 
Propose concrete amendments to `projects/score2gp/REVIEW_RULES.md` and the `devils-advocate-review` skill to prevent silent fallbacks and mock-only evidence from ever passing a review again.

## Acceptance
- A root-cause analysis artifact explaining how the review process failed.
- Specific proposed updates to governance review rules.
