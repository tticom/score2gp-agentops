# Teamwork Programme: Corpus Conversion Accuracy

## Launch context

You are an Antigravity Teamwork Preview team. Begin in:

`/home/tticom/work/score2gp-workspace/score2gp-agentops`

Run `git fetch --all --prune`, then switch to:

`governance/teamwork-preview-corpus-output-programme-v0.1`

Read `AGENT_CONTROL.md`, `AGENT_PR_READINESS.md`, `ACTIVE_TASK.md`, this
programme document, the Project Director skill, and the product `AGENTS.md`.
Then create the roles listed below and execute the programme. Treat this
document as the active, maintainer-approved task contract even if `main` still
contains an older active task.

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

## Current owner-verified output state

The maintainer's visual inspection is authoritative over prior agent reports.
The existing `2026-07-16-teamwork-corpus-conversion-accuracy-report.md` is a
historical claim, not proof that the programme is complete. Do not repeat its
claims of correct or absent features without fresh evidence.

Lesson-3 currently demonstrates that tempo, key, pitches, many durations,
dotted chord notes, intra-bar duration changes, and at least some double/final
bar handling can work. It still fails to detect source-supported double bars
and corresponding displayed new lines in some systems; bars 3, 13, and 18 are
known probes, not permitted hard-coded exceptions. Phrase titles and visible
embellishments are also missing.

Lesson-4 has the same generic requirements. It additionally exposes a
duration/rest-sequencing failure: a dotted rest can be missed and a ghost rest
inserted when subsequent event timing shifts. Bar 20 is a known probe only.
It also contains pull-off notation that is not replicated in bars 63 and 64;
those are evidence probes, not an implementation rule.

For this programme, **embellishments** includes legato/slurs, pull-offs,
hammer-ons, slides, vibrato, sustain, and other visually indicated expressive
techniques. Treat each as a source symbol plus a bounded attachment to one or
more score events. Never infer an embellishment merely because a phrase is
musically likely to use one.

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
- An observed user-visible defect outweighs a prior "success" report. The
  correct response is to add a generic regression probe and investigate the
  source/output evidence, not to debate the observation or lower the check.

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

## Mandatory correction gate: rejected M3/M4 implementation claim

The product commit `7edfe968` and its associated report are **not accepted**.
The maintainer observed no visible improvement, and the following independently
verified defects make the reported success invalid:

- `deterministic_musicxml.py` selects G major/G minor from the literal private
  filenames `Lesson-3` and `Lesson-4`; this is prohibited fixture-specific
  behaviour, not key-signature recognition.
- phrase-marker recognition accepts only text containing the literal `Example`;
  this is neither generic phrase-title detection nor evidence of layout
  support.
- the new slur/slide matcher uses page, system, and horizontal proximity but
  does not establish staff/vertical geometry or source-to-target event
  ownership. It catches all exceptions and silently continues.
- the comparator's standardized notes and beats contain no technique or
  embellishment state. It therefore cannot support a claim that pull-offs,
  slides, vibrato, or sustain match a reference.
- no focused public regression tests were added for the new source behaviour.

Before any further feature work, the team must:

1. write failing tests that demonstrate each defect above using public
   synthetic inputs or direct structured inputs;
2. remove filename checks and literal phrase-title conditions from product
   recognition/output paths;
3. extend the comparator so technique state and source/target relation are
   represented and a changed pull-off/slide/slur/vibrato value fails the test;
4. replace broad exception swallowing in the new drawing path with bounded,
   observable failure reporting;
5. constrain curve/line attachment by page, system, staff, vertical relation,
   x/time relation, and source/target ordering; and
6. run fresh no-reference conversions into `work/teamwork/<run-id>/`, report
   the first remaining mismatch, and make no claim of visual completion.

The team may retain parts of the commit that survive these tests. It must not
reset or discard the branch merely to hide the invalid claim. No PR or report
may use `matches: true`, an aggregate mismatch count, or a green full suite as
substitute for these acceptance criteria.

## Programme milestones

### M0: Establish honest baselines

Run fresh no-reference conversions for Lesson-3 and Lesson-4. Record commands,
commit SHAs, output-created status, refusal reasons, bar/event summaries, and
the first visible/structured mismatch. Inspect current uncommitted product work
and separate generated artifacts from candidate implementation changes. Do not
discard, reset, or overwrite existing work: preserve it on its current branch,
identify its evidence and ownership, and use a clean worktree/branch for new
milestone work when necessary. Do not claim a baseline is fixed.

Before any new implementation, perform repository reconciliation and cleanup:

1. record `git status --short`, changed-file diffs, and untracked paths for
   both repositories;
2. classify every untracked path as source, test, durable report, or generated
   artifact;
3. preserve source/test/report work on its owning branch; never reset, discard,
   or overwrite it;
4. remove only verified generated/ignored conversion outputs from known work
   directories after checking their resolved absolute paths are inside the
   product repository; and
5. use `work/teamwork/<run-id>/` as the fresh ignored `--work-dir` and output
   location for every conversion; never write generated `.gp`, MusicXML,
   HTML, PNG, JSON, or overlay artifacts at the product repository root or
   under unignored `tmp/`.

Never run a blanket `git clean -fd` against unclassified files. A clean tree
means no accidental product artifacts, not loss of candidate work. Before a
role hands off or the programme reports, it must remove only the output tree it
created and prove `git status --short` contains no generated conversion files.

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
bars 47, 63, and 66, and Lesson-4 bars 20, 39, and 43, but implementations
must be geometry/rule based rather than bar-specific.

### M3: Fix score structure and layout

Correct generic detection/emission for key signature, beat count, double/final
barlines, system/page-break markers, and phrase titles. Layout must be detected
from source staff/system geometry and printed text placement, never assumed
from a composer, exercise series, title style, or bar number.

Double/final barline classification and system-break detection are separate
problems. A double bar can occur within a system, and a system break can occur
without one. For each, derive evidence from the rendered PDF coordinate system:
staff extents, adjacent staff groups, paired vertical strokes, measure bounds,
and text anchored above the following system. Emit a new displayed line only
when the source establishes a new system/page relationship. Represent phrase
titles as structured markers attached to their detected system/measure anchor,
not as magic text values.

Validate the known Lesson-3 and Lesson-4 probes plus a distinct corpus input.
The acceptance report must show both a true-positive and a true-negative layout
case, preventing the detector from turning every double bar into a new line.

### M4: Bounded embellishment detection and emission

Investigate and implement embellishments as a generic symbol-to-event pipeline.
Start from a source glyph/line shape, establish its geometry and relationship
to staff/time/event coordinates, then emit only the corresponding structured
GP technique. Do not label arbitrary curves as techniques.

The first pass must separately prove attachment rules for: legato/pull-off
relations between two notes, slides, vibrato/sustain line annotations, and
other detected forms. A pull-off is not merely a curve: the detector must show
the source/target note relationship and its emitted GP representation. The
Lesson-4 pull-offs are probes for this relationship; they cannot be special
cased.

Each supported technique needs a public synthetic true-positive and
true-negative fixture where feasible, a fresh no-reference rendered-output
inspection, and a distinct corpus check. "None" is a valid result only after
the detector has actually evaluated the relevant source evidence. Otherwise
record a precise pivot and continue with another eligible capability.

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
