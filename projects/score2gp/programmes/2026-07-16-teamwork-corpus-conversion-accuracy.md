# Teamwork Programme: Corpus Conversion Accuracy

## Maintainer intent

Make `score2gp` produce materially usable Guitar Pro files from the approved
guitar-PDF corpus. The current priority is truthful, visible conversion quality
rather than new reports that merely say the pipeline passed.

This document is the complete Teamwork Preview prompt. Start the team from the
governance repository, read the live control files, and execute this programme
without asking the maintainer for routine plan, role, branch, WSL, filesystem,
GitHub, validation, or merge permission. Routine operations are pre-approved
within this bounded programme. Ask only when the next credible action would
expand the named corpus/capabilities, expose private artifacts, require a
destructive operation, or has no evidence-backed safe interpretation.

Start with Lesson-3 and Lesson-4 because they expose concrete defects, then
generalise every accepted change against the named corpus. Do not overfit to a
private filename, bar number, reference score, hard-coded measure list, or
fixture-specific threshold.

## Approved corpus

Use the sibling approved fixture repository for inspection and local output:

`/home/tticom/work/score2gp-workspace/score2gp-private-fixtures/fixtures/private`

The initial corpus is:

- `Derek Trucks BB King.pdf`
- `Hal Leonard Corporation. Rock Ballads.pdf`
- `Jazz Classics for Solo Guitar- Chord Melody Arrangements.pdf`
- `Just-Practice-Like-THIS-Every-Day.pdf`
- `LegatoLicks.pdf`
- `Lesson-3.pdf` through `Lesson-7.pdf`
- `Lick in All 5 CAGED Shapes start on the 5 _ guitar tab creator.pdf`
- `Melodic Soloing Masterclass.pdf`

Private inputs and outputs may be interrogated locally. They must not be
committed, copied into reports, or used to mutate generation from `--ref-gp`.

## Team roles

Use Teamwork Preview to create the following coordinated roles. They share this
contract and a single evidence ledger; they do not work as independent
opinion-generators.

1. **Project Director**: owns sequencing, scope, milestone decisions, PR
   state, continuation, and the final human report.
2. **Corpus Analyst**: builds/maintains the corpus matrix and captures
   reproducible no-reference failure signatures without editing product code.
3. **Output Verifier**: builds and operates the bar-level comparator, checks
   generated GPIF/MusicXML, and rejects false claims of success.
4. **Recognition Engineer**: isolates PDF geometry/notation recognition defects
   using public synthetic regression fixtures where possible.
5. **Conversion Engineer**: fixes MusicXML, ScoreIR, GPIF, timing, guitar
   mapping, and layout emission only after the verifier identifies the exact
   product mismatch.
6. **Adversarial Reviewer**: independently reviews every product PR against
   this programme, including a fresh no-reference run and the first remaining
   mismatch.

The Project Director decides the next milestone from their evidence. A role
handoff, an opened PR, a passing unit suite, or a completed walkthrough is not
a stopping point.

## Non-negotiable truth rules

- `--ref-gp` is a validator only. It must never influence any generated tempo,
  track metadata, bar/event count, notes, durations, rests, layout, thresholds,
  or inference choices.
- Never hide a defect by changing time signatures, adding/resting events,
  dropping measures, suppressing warnings, or accepting a mismatch because a
  summary count happens to match.
- Never tune an algorithm based on a literal private file name, page/bar index,
  hard-coded expected measure count, or private reference contents.
- The existing aggregate `compare_gp` is a smoke check only. It cannot certify
  musical or visual correctness.
- Every conversion claim uses a fresh work directory and is reproducible from
  the command and commit recorded in the evidence ledger.
- Product changes must be tested first where practical and must add a public
  synthetic regression that expresses the general rule, not copied private
  musical content.
- Retain existing valid improvements. Do not revert working duration/tie/
  barline behaviour merely because a later case is hard.

## Required evidence instrument: bar-level comparator

Before accepting parser changes, implement or complete a reusable comparator
that reads generated and reference GPIF (and relevant generated MusicXML) and
produces a deterministic per-bar mismatch report. It must compare, at minimum:

- ordered note and rest events;
- onset and duration in beats/ticks;
- dotted state, ties, and chord membership;
- pitch, string, and fret where applicable;
- key/time/tempo changes;
- normal, double, and final barline styles;
- requested system/page break markers;
- techniques/embellishments when they are in scope.

It must report the first mismatch and a compact per-bar event shape. It must
be usable without a reference score as an invariant checker, and with a
reference score as a diagnostic comparator. It must not write back to either
output.

## Programme milestones

### M0: Establish honest baselines

Run fresh no-reference conversions for Lesson-3 and Lesson-4. Record commands,
commit SHAs, output-created status, refusal reasons, bar/event summaries, and
the first visible/structured mismatch. Inspect current uncommitted product work
and separate generated artifacts from candidate implementation changes. Do not
discard, reset, or overwrite existing work: preserve it on its current branch,
identify its evidence and ownership, and use a clean worktree/branch for new
milestone work when necessary. Do not claim a baseline is fixed.

### M1: Make correctness observable

Ship the bar-level comparator and public synthetic tests that prove it detects
event ordering, duration/dot, rest, barline, and layout differences. Use it to
create a truthful initial mismatch ledger for Lesson-3 and Lesson-4.

### M2: Fix event timing and duration semantics

Using M1 evidence, correct the smallest generic causes of:

- ghost rests;
- missing/incorrect whole, half, quarter, eighth, sixteenth, and thirty-second
  duration where present;
- dots on notes and rests;
- ordered rests versus notes;
- ties and carried duration;
- chord versus sequential event grouping.

Acceptance is exact bar-level improvement in the reported affected bars and no
regression on at least one non-Lesson PDF. The known targets include Lesson-3
bars 47, 63, and 66, and Lesson-4 bars 39 and 43, but implementations must be
geometry/rule based rather than bar-specific.

### M3: Fix score structure and layout

Correct generic detection/emission for key signature, beat count, double/final
barlines, and system-break markers. For the Lesson series, double/final
barlines and section titles are evidence for a new displayed line only when
the PDF supports that relation. Validate against Lesson-3 double-bar failures
and Lesson-4's missing middle double bars, then another corpus input.

### M4: Bounded embellishment investigation and implementation

Investigate visible embellishments such as vibrato lines on chordal notes. Do
not label arbitrary curves as techniques. First establish a geometry-to-event
association rule and a public synthetic test; implement only the smallest
technique whose true/false-positive boundary is measurable. Otherwise record a
precise pivot and continue with another eligible capability.

### M5: Corpus generalisation and final report

Run the corpus smoke matrix. Cluster failures by capability, not filename.
For each PDF, report: output produced, stage/refusal, structure quality,
duration/rest/dot status, barline/layout status, embellishment status, and
first blocker. Select and execute the next smallest generic capability while
credible work remains.

## Working loop

For each milestone:

1. Director reads the current evidence ledger and selects one generic defect.
2. Analyst/Verifier isolate it with source/output evidence and state a
   measurable expected change.
3. Engineer adds a failing public regression where feasible, implements the
   narrow change, and runs focused plus full verification.
4. Verifier runs a fresh no-reference conversion and comparator against the
   relevant bar(s), plus one distinct corpus regression input.
5. Reviewer either approves the precise claim or returns it for changes.
6. Director opens/updates a focused PR, performs the guarded merge checks, and
   merges only when authorised by `ACTIVE_TASK.md` and `AGENT_CONTROL.md`.
7. Director records the decision, pulls `main`, and immediately starts the
   next eligible milestone.

If a proposed fix fails, keep the failure evidence, abandon only that approach,
and select the smallest credible pivot. Never stop merely because the first
approach was wrong.

## Required final report

Write a human-focused report in `score2gp-agentops` containing:

- PRs/commits merged and their exact capabilities;
- before/after mismatch ledger for Lesson-3 and Lesson-4;
- corpus matrix grouped by capability;
- what now works, what improved but remains imperfect, and what is deferred;
- evidence that no reference leakage occurred;
- remaining first blocker and the next ordered programme task;
- process changes needed only where the evidence shows a genuine bottleneck.

Do not report "complete", "working", or "fully correct" unless the
bar-level evidence supports that statement.
