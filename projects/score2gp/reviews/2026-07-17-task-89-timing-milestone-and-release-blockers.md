# Task 89 Review: Timing Milestone Does Not Authorize Release

## Verdict

**PARTIALLY VERIFIED; NOT READY TO MERGE OR DEPLOY.**

The recovery branch clears the previous fatal `musicxml_timing_risk` refusal
for the tested Lesson PDFs, but that is a timing milestone only. It is not
evidence that the generated Guitar Pro output is musically or visually
acceptable.

## Reviewed Product State

- Branch: `recovery/pre-teamwork-score-output-baseline-v0.1`
- Head: `b7a2aa79`
- Baseline: `e70bddaa`
- Product worktree used:
  `/home/tticom/work/score2gp-workspace/score2gp-recovery`

The canonical `score2gp` worktree remains on the frozen failed Teamwork branch.
The virtual environment is editable-installed against that canonical worktree,
so all recovery validation must use source-first invocation:

```bash
cd /home/tticom/work/score2gp-workspace/score2gp-recovery
env PYTHONPATH=.:src ../score2gp/.venv/bin/python -m score2gp.cli convert ...
```

Using `.venv/bin/score2gp` from the canonical worktree cannot validate recovery
work and must not be described as a recovery result.

## Fresh Timing Evidence

Fresh no-reference runs at `b7a2aa79` wrote external artifacts for Lessons 3
through 7. The generated MusicXML was parsed with `analyze_musicxml_timing`.

| PDF | GP package written | Fatal timing issues | Diagnostics |
| --- | --- | ---: | --- |
| Lesson-3 | yes | 0 | 90 informational chord-stack diagnostics |
| Lesson-4 | yes | 0 | 48 informational chord-stack diagnostics |
| Lesson-5 | yes | 0 | 855 informational compound-meter and chord-stack diagnostics |
| Lesson-6 | yes | 0 | 957 informational compound-meter and chord-stack diagnostics |
| Lesson-7 | yes | 0 | 900 informational compound-meter and chord-stack diagnostics |

This supersedes the earlier interim result at `c0b87f12`, where Lesson-5 still
contained fatal timing errors. The diagnostic totals above must not be reported
as fatal failures: their recorded severity is `info`.

## Release Blockers

1. `git diff --check e70bddaa..b7a2aa79` fails. Recovery commits introduced
   trailing whitespace in product code, tests, and the corpus runner.
2. The timing change has focused public coverage, but the complete product
   verification suite and artifact audit have not yet been recorded against
   `b7a2aa79`.
3. Source key recognition is not implemented. `deterministic_musicxml.py`
   still writes `<fifths>0</fifths>` unconditionally. A neutral key must not be
   described as detected source metadata.
4. Existing title/tempo extraction is not a valid general solution. The source
   path only accepts text containing the literal `Example`, attaches text using
   a broad vertical-distance rule, and swallows all failures. The Lesson-4
   recovery MusicXML includes false rehearsal labels `P`, demonstrating that
   a nearby notation label can be promoted to a phrase title.
5. System/page breaks are copied only when a system preview already exists.
   This is not proof that all source system boundaries or double/final barlines
   were recognised and emitted correctly.
6. No accepted source-to-event embellishment path exists. The recovery timing
   changes provide no evidence for legato, pull-off, slide, chordal vibrato, or
   sustain output. Such labels must remain fail-closed.

## Required Continuation

Continue inside the existing Teamwork programme rather than opening another
unrelated broad feature pass.

1. Commit a hygiene-only repair for all recovery-introduced whitespace and run
   `git diff --check`, `python scripts/agent_verify.py`, and artifact audit at
   the exact recovery head.
2. Add a severity-aware corpus ledger: fatal timing issues, warnings, and
   informational diagnostics must be separate columns. A GP package and an
   informational diagnostic are not refusal evidence.
3. Implement a reusable source-evidence trace before changing emitted music:
   source text/geometry -> page/system/staff -> measure anchor -> MusicXML ->
   ScoreIR -> GPIF. The trace must cover tempo, key status (detected, unknown,
   or explicit override), system/page breaks, barline style, and phrase title.
4. Remove literal title filtering and broad exception swallowing. Reject text
   that cannot be classified and anchored as a title; do not emit it as a
   rehearsal marker.
5. Use the trace and bar-level comparator to select the smallest next generic
   implementation. No release claim is allowed until it passes a public
   true-positive and true-negative test plus a distinct corpus check.

## Deployment Rule

Do not merge or re-point the canonical worktree to this recovery branch yet.
The canonical command should change only after a focused PR passes the timing,
metadata, layout, and hygiene gates above. Until then, the user-visible
canonical output correctly remains evidence of the frozen branch, not proof
of a deployed recovery.
