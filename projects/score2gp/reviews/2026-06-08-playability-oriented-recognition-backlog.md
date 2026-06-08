# Playability-Oriented Recognition Backlog

**Date:** 2026-06-08  
**Purpose:** Record the longer-term recognition roadmap shaped by current real-example failures, without turning the active queue into an uncontrolled semantic implementation effort.

## Design principle

The system should assume the source score is intentional and musically meaningful. When the current parse does not reconcile with the visible score, the system should not reject the score. It should record the mismatch, preserve the visual evidence, and search for the notation feature it has misunderstood.

The long-term target is not merely symbol detection. The target is a playable interpretation that helps a human learn the music.

## Current motivating observations

The current major-triad exercise example shows meaningful progress, but also exposes the next recognition classes:

- Bar 3: whole-note or full-bar duration is not preserved. This may involve open/unstemmed note evidence, tie/dot context, or full-bar duration interpretation.
- Bars 4 and 8: a double barline or section delimiter should create a logical break/new line.
- Bar 7: the final note is interpreted like a quaver when it should behave as a crotchet.
- Bars 23-25: the current output overcounts events across a boundary and fails to recognise a stacked/chord event.

These are not evidence that the score is invalid. They are evidence that the recogniser has missed or misinterpreted notation.

## Recognition pipeline shape

Do not treat semantics as one large layer. Split recognition into:

1. visual evidence capture
2. candidate grouping
3. interpretation
4. reconciliation
5. recovery search
6. playable export
7. human-facing report

## Priority 0 — Benchmark observations and playability target

### Task 36 — Record playability benchmark observations from current example

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: create a durable observation record for the current major triad exercise example, focused on what a human expects to play and where the current system differs.

Must record source location, visible score evidence, current output, expected playable result, likely notation feature misunderstood, affected category, and what evidence would help resolve it.

Initial observations: bar 3 whole/full-bar duration failure; bars 4 and 8 double-barline section break failure; bar 7 terminal crotchet duration failure; bars 23-25 boundary/event-count/chord simultaneity failure.

Non-goals: no implementation logic; do not treat the source as invalid; do not reject output because of mismatch.

Acceptance criteria: each issue is specific enough for a musician and developer to understand the expected playable result, and each is linked to a future task category.

### Task 37 — Define playability-oriented recognition principles

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: document the recognition philosophy before semantic work expands.

Must include: assume the source score is intentional; parse mismatch means the recogniser likely missed evidence; structural mismatch is a recovery signal, not a rejection reason; playable output is the target; diagnostics should explain choices; uncertain cases should preserve alternatives where feasible.

### Task 38 — Create visual-to-playable benchmark schema

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: define a small JSON schema for benchmark observations that links visible notation to expected playable interpretation.

Fields: benchmark_id, source_reference, page_index, system_index, bar_index, visual_description, current_output_summary, expected_playable_result, suspected_missing_feature, recognition_category, recovery_hint, status.

Recognition categories: structure, pitch, duration, rhythm, simultaneity, TAB, articulation, technique, navigation, expression, export.

## Priority 1 — Structural and layout recognition

### Task 39 — Add paired vertical boundary candidate model

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: represent close paired vertical strokes as a geometry-level boundary candidate.

Allowed terms: PairedVerticalBoundaryCandidate, SectionBoundaryCandidate, FinalBoundaryCandidate. RepeatBoundaryCandidate is allowed only when repeat dots are also observed.

Non-goals: no repeat playback; no full navigation structure.

### Task 40 — Add synthetic double-barline section fixture

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: create a synthetic fixture where a double barline separates short examples or phrases.

Expected behaviour: ordinary bars remain ordinary bars; double barline is detected as a section boundary candidate; downstream diagnostics can identify where a logical reset should occur.

### Task 41 — Add logical line/section segmentation diagnostics

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: add diagnostics that separate physical systems from logical musical sections.

Acceptance criteria: diagnostics can say a new logical section begins after a boundary; no assumption that every double barline means repeat or final ending; preserves enough evidence for later export/layout.

### Task 42 — Add final barline and end-of-example boundary candidate

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect final barline structures that mark the end of an example, exercise, or section.

### Task 43 — Add repeat-sign geometry candidate

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect double barline plus repeat dots as a repeat-sign candidate.

Non-goals: no playback expansion; no volta handling.

### Task 44 — Add volta bracket geometry candidate

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect first/second ending brackets as navigational structure.

### Task 45 — Add navigation marker text candidate

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect textual navigation markers such as D.C., D.S., Coda, Fine, and Segno.

## Priority 2 — Note-event evidence layer

### Task 46 — Define note-event evidence model

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: create an intermediate model that collects evidence for a playable note or rest without finalising semantics too early.

Model should support marker position, marker shape, filled/hollow evidence, stem evidence, flag evidence, beam membership, dot evidence, tie/slur nearby curve evidence, TAB fret evidence, same-x simultaneity evidence, and confidence/evidence notes.

Non-goals: no final duration assignment; no pitch spelling; no voice assignment.

### Task 47 — Add hollow/open marker detection fixture

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: support recognition of whole-note or minim-like open noteheads.

### Task 48 — Add stem association diagnostics

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: associate vertical strokes with nearby note markers where appropriate.

### Task 49 — Add flag and beam association diagnostics

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: identify flags and beams attached to note stems.

### Task 50 — Add augmentation dot candidate detection

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect dots immediately to the right of notes or rests as duration modifiers.

### Task 51 — Add tie/slur curve candidate distinction research

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: research how to distinguish ties from slurs using geometry and musical context.

Must consider: ties connect same pitch across adjacent notes; slurs connect different notes or phrases; in TAB/guitar context slurs may indicate hammer-ons or pull-offs; visual geometry alone may be insufficient.

### Task 52 — Add rest-symbol evidence candidates

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: create geometry/text candidates for rests without assigning final duration too early.

## Priority 3 — Duration and rhythm interpretation

### Task 53 — Define duration evidence resolver

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: implement a resolver that assigns possible durations from evidence: notehead type, stem, flags, beams, dots, ties, rests, and bar context.

Non-goals: no voice assignment; no complex tuplets; no full rhythm repair.

### Task 54 — Add whole-note/full-bar duration fixture

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: create a synthetic fixture equivalent to the bar 3 problem.

### Task 55 — Add terminal crotchet-after-quavers fixture

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: create a synthetic fixture equivalent to the bar 7 problem.

### Task 56 — Add dotted note duration fixture

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: test augmentation dots as duration modifiers.

### Task 57 — Add tied-duration fixture

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: test tied notes across a barline and within a bar.

### Task 58 — Add rest duration fixture

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: test rests as duration-bearing events.

### Task 59 — Add tuplets research note

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: document how tuplets should later affect duration interpretation.

### Task 60 — Add bar-duration reconciliation diagnostics

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: compare interpreted event durations against the expected bar duration from the time signature.

Design principle: mismatch is a recovery signal, not a rejection.

### Task 61 — Add alternate duration interpretation search

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: when bar duration does not reconcile, try plausible alternate interpretations.

Examples: final quaver may be a crotchet; open unstemmed marker may be whole-note duration; dot may have been missed; tie may extend duration; stacked notes should be simultaneous, not sequential.

## Priority 4 — Pitch, TAB, simultaneity, and chords

### Task 62 — Define same-x simultaneity candidate

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: represent multiple markers or TAB fret numbers aligned at the same x-position as simultaneous candidates.

### Task 63 — Add stacked-marker synthetic fixture

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: create a synthetic fixture equivalent to the chord failure.

### Task 64 — Add chord-event model

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: represent a playable simultaneous event.

Model should support standard notation members, TAB members, onset position, duration evidence, optional chord name if text/diagram provides it, and confidence/evidence trace.

### Task 65 — Add standard-staff pitch-position resolver

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: resolve staff vertical positions into pitch candidates using clef, key signature, accidentals, and ledger lines.

Prerequisites: clef detection, key signature detection, and stable staff position indexing.

### Task 66 — Add treble clef candidate detection

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect treble clef in standard guitar notation.

### Task 67 — Add key signature candidate detection

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect sharps/flats after clef and before time signature.

### Task 68 — Add time signature candidate detection

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect stacked numeric time signatures.

### Task 69 — Add local accidental candidate detection

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect sharps, flats, and naturals near note events.

### Task 70 — Add ledger-line candidate support

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: recognise ledger lines and associate them with note markers outside the staff.

### Task 71 — Add TAB staff string-index resolver

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: map TAB lines to guitar strings.

### Task 72 — Add TAB fret-number event resolver

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: resolve TAB fret numbers into string/fret events.

### Task 73 — Add standard/TAB alignment resolver

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: align standard notation events with TAB events where both are present.

### Task 74 — Add guitar tuning model

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: represent tuning explicitly for TAB-to-pitch conversion.

## Priority 5 — Guitar articulations and performance techniques

### Task 75 — Add hammer-on and pull-off candidate detection

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect TAB `h` and `p` markings and associated slur curves.

### Task 76 — Add slide candidate detection

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect diagonal slide markings in TAB or standard notation.

### Task 77 — Add bend candidate detection

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect curved bend arrows and bend amount text.

### Task 78 — Add vibrato candidate detection

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect wavy vibrato lines.

### Task 79 — Add muted/dead note handling

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect `x` noteheads or TAB fret markers.

### Task 80 — Add palm muting region detection

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect `P.M.` text and dashed continuation line.

### Task 81 — Add arpeggiated chord/roll candidate detection

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect vertical wavy lines beside chords.

### Task 82 — Add picking direction candidate detection

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect down-pick and up-pick markers.

## Priority 6 — Dynamics, expression, text, and navigation

### Task 83 — Add tempo marking detection

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect tempo text such as crotchet = 120.

### Task 84 — Add dynamic mark detection

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect p, mp, mf, f, and related dynamic marks.

### Task 85 — Add crescendo/diminuendo hairpin detection

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect opening and closing hairpins.

### Task 86 — Add chord diagram detection

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect guitar chord boxes above the staff.

### Task 87 — Add chord name text detection

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: detect chord names above the staff.

### Task 88 — Add lyrics/text annotation isolation

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: prevent lyrics, labels, and example headings from being misread as musical events.

## Priority 7 — Reconciliation, recovery, and export

### Task 89 — Add parse mismatch log

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: create a diagnostics structure that records when current interpretation does not reconcile with visible evidence.

Important: this is not an error and not a rejection.

### Task 90 — Add recovery strategy registry

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: define small recovery strategies that can be applied when parse mismatch occurs.

Examples: reinterpret note duration; search for missed dot; search for missed tie; split section at boundary; group same-x events as simultaneity; check TAB alignment; check rest/event omission.

### Task 91 — Add playable interpretation ranking

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: rank alternate parses by visual evidence and musical reconciliation.

### Task 92 — Add human-readable recognition report

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: generate a report that explains what the system read and why.

Audience: a human learning to play the piece and a developer debugging recognition.

### Task 93 — Add MusicXML export compatibility check

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: ensure playable interpretation can be represented in MusicXML.

### Task 94 — Add Guitar Pro export compatibility check

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: ensure playable interpretation can be represented in Guitar Pro output.

### Task 95 — Add side-by-side expected vs current output report

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: support benchmark-driven development by comparing expected playable interpretation with current output.

### Task 96 — Add regression benchmark suite

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: turn benchmark observations into regression cases.

### Task 97 — Add confidence and uncertainty model

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: represent uncertainty honestly without stopping output.

### Task 98 — Add learning-focused output review

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: review whether output is useful to a guitarist trying to learn the piece.

## Priority 8 — Long-term completeness coverage

### Task 99 — Create notation taxonomy document

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: document the full symbol space the system eventually needs to handle.

Categories: staff framework, clefs, key signatures, time signatures, notes, rests, dots, ties, beams, tuplets, accidentals, ledger lines, TAB fret numbers, TAB string semantics, guitar techniques, barlines, repeats, volta brackets, navigation markers, dynamics, expression, chord diagrams, chord names, and text annotations.

### Task 100 — Create staged notation capability matrix

Status: PLANNED / NOT ACTIVE until explicitly promoted.

Purpose: track what the system can detect, interpret, reconcile, and export.

Columns: symbol/feature, detection status, interpretation status, reconciliation support, export support, benchmark coverage, known limitations, and next task.

## Recommended insertion order

Add Tasks 36-38 immediately after the current governance backlog only if the human wants benchmark recording before continuing product implementation.

Then run Tasks 39-45 before broad duration work, because structure and section boundaries directly affect bars 4, 8, and 24.

Then run Tasks 46-61, because duration and rhythm are currently the most visible blocker for playable output.

Then run Tasks 62-74, because simultaneity, TAB alignment, pitch, and chord handling are needed to fix the bar 23-25 class of failures.

Then run Tasks 75-88, because guitar-specific performance notation and expression are essential for real guitar music but should not distract from notes, bars, durations, and chords.

Then run Tasks 89-100, because reconciliation, recovery, export, and capability tracking make the system durable rather than a collection of one-off recognisers.

## Governance warning

This document is a roadmap. It does not override `ACTIVE_TASK.md`. It does not approve immediate implementation of pitch, duration, voice assignment, full rhythm interpretation, or ScoreIR event generation unless those tasks are explicitly promoted into the executable queue with prerequisites, validation, acceptance criteria, and stop conditions.
