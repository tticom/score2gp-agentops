# Task 89 Interim Review: Segmentation Is Not Complete

## Verdict

NOT READY TO PROMOTE

## Reviewed Product Commits

- `9d5985e3` `feat: repair measure segmentation and compound note duration mapping`
- `c0b87f12` `feat: implement iterative barline restoration for overfull measures`

## Fresh Verification

The reviewer ran the recovery source at `c0b87f12` using:

```bash
cd /home/tticom/work/score2gp-workspace/score2gp-recovery
env PYTHONPATH=.:src ../score2gp/.venv/bin/python -m score2gp.cli convert \
  --pdf ../score2gp-private-fixtures/fixtures/private/Lesson-5.pdf \
  --out /home/tticom/work/score2gp-runs/segmentation-head-lesson5/Lesson-5.gp \
  --work-dir /home/tticom/work/score2gp-runs/segmentation-head-lesson5
```

The conversion still refuses with `musicxml_timing_risk`. Parsed MusicXML has
14 fatal timing issues. The residual overfull measures are 44, 45, and 73 in
the generated 12/8 timeline. Measure 45 contains events through 7,680
divisions while its supported capacity is 5,760 divisions.

The work is a measurable reduction from the prior 129 fatal timing issues,
but no Guitar Pro file is produced. It is not completion evidence and must not
be described as a successful Lesson-5 conversion.

## Required Continuation

1. Continue Task 89 without requesting routine maintainer input.
2. Inspect the source barline and measure-anchor evidence feeding each residual
   overfull generated measure. Do not use the recorded measure numbers as
   implementation conditions.
3. Determine whether the remaining defect is missing source boundary evidence,
   incorrect source-to-timeline ownership, or an iterative-restoration limit.
4. Add a public synthetic regression for the identified generic condition.
5. Re-run the fresh recovery command and require zero fatal parsed MusicXML
   timing issues before promotion.
6. Correct the corpus report if it marks a conversion successful without an
   actual GP output and parser-clean timing result.

## Guardrails

- Do not relax `musicxml_timing_risk`.
- Do not split based only on cumulative duration.
- Do not add PDF, page, system, or measure literals to product logic.
- Do not merge the recovery branch into the canonical product worktree until
  this reviewer verdict is replaced by an independently verified approval.
