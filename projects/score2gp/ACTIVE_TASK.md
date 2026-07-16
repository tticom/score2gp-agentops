# Active Task

**Task**: Task 88 recovery: restore the pre-Teamwork output baseline and prove one layout improvement
**Authorised Role**: Project Director, Developer, and Reviewer
**Repository**: `tticom/score2gp-agentops` and `tticom/score2gp`

## Status

APPROVED

## Task Authorised

Yes

## Completion Evidence

Do not continue on `feature/teamwork-corpus-conversion-accuracy-v0.1`.

Use the non-destructive recovery branch:

`recovery/pre-teamwork-score-output-baseline-v0.1` at `e70bddaa`

Create a separate worktree for this branch before conversion work, leaving the
failed branch and its generated artifacts intact for later review.

Read:

`projects/score2gp/programmes/2026-07-16-teamwork-corpus-conversion-accuracy.md`

`projects/score2gp/reviews/2026-07-16-teamwork-recovery-decision.md`

## Completion Evidence

1. Fresh no-reference Lesson-3 and Lesson-4 outputs are generated from the
   recovery branch into an ignored recovery work directory.
2. The report separates the recovery baseline from failed Teamwork output;
   it does not compare them by aggregate counts only.
3. No accidental/key, duration, or embellishment code is changed in this task.
4. One and only one generic source-layout trace is implemented or repaired:
   PDF system identity -> MusicXML -> ScoreIR -> GPIF layout/title element.
5. A focused end-to-end test proves the trace, including a negative case.
6. The first remaining visible mismatch is recorded without a success claim.

The team may proceed to the next narrowly scoped task only after Reviewer
verification. It must never cherry-pick, merge, or copy code from the failed
Teamwork commits without an independent, focused review.

Historical rejection records:

`projects/score2gp/reviews/2026-07-16-teamwork-m3-m4-claim-rejection.md`

`projects/score2gp/reviews/2026-07-16-teamwork-regression-containment.md`
