# Active Task

**Task**: CR-02: Build the Visual Output Probe and First-Divergence Ledger
**Authorised Role**: Project Director, Corpus Analyst, Output Verifier, Architect, and Reviewer
**Repository**: `tticom/score2gp-agentops`, with read-only inspection of `score2gp` and approved local fixtures

## Status

APPROVED

## Task Authorised

Yes, Tier 1 research/documentation only.

## Context

The maintainer's current rendered source/output comparison shows a source
tempo of 70 and 4/4 being emitted as 12/8, followed by missing notes, ghost
rests, incorrect grouping, and missing double bars and phrase titles. Earlier
timing-gate success claims are therefore insufficient. Product PR #372 and
stacked PR #371 remain open and blocked; do not merge, modify, or claim either
as complete in this task.

Read:

1. `projects/score2gp/research/2026-07-17-maintainer-visual-observation-ledger.md`
2. `projects/score2gp/programmes/2026-07-17-visual-output-correctness-recovery.md`
3. `projects/score2gp/tasks/2026-07-17-visual-output-correctness-backlog.md`
4. `projects/score2gp/reviews/2026-07-17-task-89-timing-milestone-and-release-blockers.md`

## Required Work

1. Identify the exact approved input represented by VO-01 using title/tempo/
   layout evidence. Do not guess its filename.
2. Run the selected product branch source-first into an external run directory.
   Record source facts, generated MusicXML, ScoreIR, and GPIF facts in a
   sanitized per-system/per-measure first-divergence ledger.
3. Run one distinct corpus input through the same probe.
4. Determine whether 12/8 is selected during source meter detection, timeline
   reconstruction, MusicXML emission, or a later conversion stage.
5. Define CR-03 with one generic meter rule, public structured test plan,
   acceptance facts, and pivot condition. If meter is not the first divergence,
   promote the actual first-divergence task instead.

## Boundaries

- No product code, product test, package, branch, PR, or installation changes.
- No private fixture or generated artifact in Git.
- No reference score influences generation.
- Do not use a title, tempo, bar count, or fixture identity as an implementation
  shortcut.

## Completion Evidence

- A research report and sanitized JSON ledger are committed in AgentOps.
- The report names one first causal transition for the 4/4-to-12/8 mismatch.
- A Reviewer records the evidence and promotes the next smallest task without
  routine maintainer approval.
