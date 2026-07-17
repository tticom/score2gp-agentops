# Active Task

**Task**: Task 90: Establish source-metadata evidence and fail-closed output
**Authorised Role**: Project Director, Corpus Analyst, Recognition Engineer, Conversion Engineer, and Reviewer
**Repository**: `tticom/score2gp-agentops` and `tticom/score2gp`

## Status

APPROVED

## Task Authorised

Yes

## Start State

Do not work on `feature/teamwork-corpus-conversion-accuracy-v0.1`.

Task 89 timing recovery has reached a narrow functional milestone. Continue
from the recovery branch:

`recovery/pre-teamwork-score-output-baseline-v0.1` at `b7a2aa79`

Do not merge, rebase, copy into, or otherwise deploy the frozen Teamwork
branch. The timing recovery is also not yet deployable; read
`reviews/2026-07-17-task-89-timing-milestone-and-release-blockers.md` before
working.

Use the recovery source tree, not the editable install bound to the frozen
worktree:

```bash
cd /home/tticom/work/score2gp-workspace/score2gp-recovery
env PYTHONPATH=.:src ../score2gp/.venv/bin/python -m score2gp.cli ...
```

All generated output belongs under:

`/home/tticom/work/score2gp-runs/<run-id>/`

Never write generated output to a repository-root `tmp/` directory.

## Verified Timing Milestone

Fresh source-first recovery conversions now write GP packages for Lessons 3
through 7 with zero fatal parsed MusicXML timing issues. Their timing-analysis
diagnostics are informational chord-stack and compound-meter reports, not
refusals. This is a limited timing result, not visual or musical acceptance.

The recovery branch still fails `git diff --check` against its baseline and
has no completed product verification record at `b7a2aa79`. The canonical
worktree remains on the failed Teamwork branch, so a normal canonical CLI
invocation cannot demonstrate recovery behaviour.

## User-Visible Release Blockers

- Key signatures are defaulted because the MusicXML emitter writes a neutral
  key unconditionally; source key recognition is absent.
- Phrase-title extraction accepts a literal `Example` condition and can emit
  false labels such as `P`.
- Tempo, source system/page breaks, and double/final bars lack a complete,
  inspectable source-to-GPIF trace.
- No embellishment path has sufficient attachment evidence to emit normal
  output. Legato, pull-off, slide, vibrato, and sustain must remain fail-closed.
- The user has observed unchanged or regressed canonical Lesson-3 and Lesson-4
  output. Do not claim an improvement from a generated file, an informational
  timing diagnostic, or a passing unit test alone.

## Required Work

1. Create a new branch from recovery head for this task. First make
   `git diff --check` clean using a whitespace-only commit. Do not mix it with
   behaviour changes.
2. Run and record `python scripts/agent_verify.py`, artifact audit, focused
   tests, and a full suite against the actual recovery source. The editable
   environment must not silently import the canonical worktree.
3. Add a severity-aware corpus evidence ledger. Fatal timing issues, warnings,
   and informational diagnostics are separate fields. Record external output
   paths, source commit, and whether a GP package exists.
4. Build an inspectable source-metadata trace for each selected system:
   PDF text/geometry -> page/system/staff -> measure anchor -> MusicXML ->
   ScoreIR -> GPIF. The trace must represent tempo, key status (`detected`,
   `unknown`, or explicit override), phrase-title candidate and rejection
   reason, source system/page break, and barline style.
5. Remove literal title matching and broad exception swallowing from the
   metadata path. A rejected label must be observable in diagnostics and must
   not be emitted as a phrase title.
6. Make unknown source key status explicit. Do not emit a neutral key as though
   it were recognised, and do not emit accidental symbols from unverified key
   evidence.
7. Add public structured true-positive and true-negative tests for title
   anchoring, tempo attachment, key status, and source layout propagation.
   Use Lessons 3 and 4 only as no-reference evidence probes; do not encode
   their names, pages, bars, counts, or reference contents in product logic.
8. Do not change pitch, duration, rest, tie, or embellishment output under this
   task except to remove an output that lacks source evidence. The next task
   will select one smallest evidence-backed layout or embellishment capability.

## Prohibited Shortcuts

- No filename, page, bar-number, measure-count, or private-reference rules.
- No broad duration scaling, dynamic meter inflation, or relaxed timing gate.
- No generated GP file, green unit suite, or informational diagnostic is
  visual-correctness evidence.
- No generic text token, including `Example`, may be used as a phrase-title
  classifier.
- No broad exception swallowing or silent default metadata.
- No technique label without a source-to-event evidence record.
- Do not merge, cherry-pick, or copy from the failed Teamwork branch.

## Completion Evidence

1. `git diff --check`, focused tests, full test suite, `agent_verify.py`, and
   artifact audit pass at the exact product head.
2. The reviewer independently reruns source-first no-reference conversions for
   Lessons 3, 4, and one distinct corpus PDF, then verifies the ledger's
   severity classification from parsed MusicXML.
3. Tests prove a nearby notation label is rejected as a phrase title, an
   unknown key is not represented as recognised, and detected source metadata
   survives the complete trace to GPIF.
4. The review identifies the first remaining user-visible mismatch without
   calling the output complete, then immediately promotes the next smallest
   eligible Teamwork task.
