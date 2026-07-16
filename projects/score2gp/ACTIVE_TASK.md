# Active Task

**Task**: Task 89: Repair source-supported measure segmentation after meter detection
**Authorised Role**: Project Director, Developer, and Reviewer
**Repository**: `tticom/score2gp-agentops` and `tticom/score2gp`

## Status

APPROVED

## Task Authorised

Yes

## Start State

Do not work on `feature/teamwork-corpus-conversion-accuracy-v0.1`.

Continue from the recovery branch:

`recovery/pre-teamwork-score-output-baseline-v0.1` at `0eea506d`

The branch contains a source-evidence meter detector. Its report is not
completion evidence: a fresh recovery run of `Lesson-5.pdf` detects `12/8`,
but `build-ir` still refuses the generated MusicXML.

Use the recovery source tree, not the editable install bound to the frozen
worktree:

```bash
cd /home/tticom/work/score2gp-workspace/score2gp-recovery
env PYTHONPATH=.:src ../score2gp/.venv/bin/python -m score2gp.cli ...
```

All generated output belongs under:

`/home/tticom/work/score2gp-runs/<run-id>/`

Never write generated output to a repository-root `tmp/` directory.

## Verified Failure

In a fresh `Lesson-5.pdf` recovery conversion, generated MusicXML measures
1--18 use `12/8` correctly. At measure 19 the timeline emits 16 eighth-note
events, or 7,680 divisions, into one `12/8` measure. The parser correctly
reports `musicxml-overfull-bar`; the source-measure segmentation has merged
multiple measures. Lesson-6 and Lesson-7 require the same general proof.

The corpus reports committed after `0eea506d` must be corrected: their
valid/invalid measure columns are not derived from parsed MusicXML timing and
must not be used as completion evidence.

## Required Work

1. Make the corpus runner derive timing-valid and timing-invalid counts only
   from parsed MusicXML and `analyze_musicxml_timing`.
2. Add public synthetic tests for a valid 12/8 sequence and for a merged
   source-measure error.
3. Repair the generic PDF barline/measure-anchor to timeline segmentation path.
   A split is allowed only when source boundary evidence supports it; never
   split solely because a measure is overfull.
4. Demonstrate fresh no-reference recovery runs for Lessons 5, 6, and 7 with
   no `musicxml_timing_risk` before claiming output success.
5. Re-run Lessons 3 and 4 as no-reference regressions. Do not alter their
   behavior merely to satisfy a check.

## Prohibited Shortcuts

- No filename, page, bar-number, measure-count, or private-reference rules.
- No broad duration scaling, dynamic meter inflation, or relaxed timing gate.
- No generated GP file is evidence of success while parsed MusicXML has fatal
  timing issues.
- Do not merge, cherry-pick, or copy from the failed Teamwork branch.

## Completion Evidence

1. `git diff --check`, focused tests, full test suite, and artifact audit pass.
2. The reviewer independently reruns the recovery command above.
3. Corpus reporting distinguishes actual parser timing errors from predicted
   timeline counts.
4. The first remaining cross-corpus blocker is recorded without a success
   claim, and the next eligible task is promoted without waiting for routine
   maintainer permission.
