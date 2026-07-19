# Notation OMR Refactor Readiness

## Status

Preparation only. This is not authority to rename, move, or split product
modules. The existing `whole_note_recogniser.py` name is misleading: the file
now owns broader notation-OMR concerns, including staff geometry, event
evidence, duration and rest evidence, timeline construction, and diagnostics.

## Entry Gates

The FS-06 architecture task may begin only when all of these are true:

1. The invalid product PR #376 has been remediated by an externally merged,
   independently reviewed revert or replacement decision.
2. FS-01 and FS-02 have established the committed `score2gp convert` runtime
   and its source-to-output call path.
3. FS-03 has a repeatable corpus status record and FS-05 has accepted a
   liveable baseline.
4. The refactor task has characterization tests and corpus comparison records
   that distinguish code relocation from behaviour change.

## Target Boundary

The intended package is `score2gp.notation_omr`. Its public facade should be a
small, explicitly named recognition service. Internal modules should be split
only along demonstrated ownership boundaries:

- `models`: immutable evidence and timeline data contracts;
- `staff_geometry`: staff, system, barline, and measure-span facts;
- `event_evidence`: notehead, stem, beam, dot, rest, and text evidence;
- `duration_evidence`: duration, tuplet, and meter evidence without GP output;
- `pitch`: clef-aware staff-position to pitch facts;
- `timeline`: event ordering, chord grouping, and measure-capacity checks;
- `diagnostics`: serialisation and explicit uncertainty reporting; and
- `service`: the narrow compatibility-facing entry point.

Module names are hypotheses until FS-06 maps actual functions and imports. Do
not create empty modules merely to match this list.

## Compatibility-First Migration

1. Add characterization tests around the current public functions and corpus
   records before moving code.
2. Move one cohesive data model or pure helper boundary at a time, preserving
   function signatures and imports.
3. Introduce `notation_omr.service` as the new facade only after its behaviour
   is covered.
4. Turn `whole_note_recogniser.py` into a thin documented compatibility shim
   that delegates to the facade. Keep it during a defined compatibility window.
5. Migrate callers one at a time. Delete the shim only under a separately
   approved breaking-change task.

Each product PR may cover one boundary only. A refactor PR must not also repair
durations, rests, tuplets, layout, embellishments, or fixture-specific output.
Those are functional tasks with their own evidence and review.

## Refactor Acceptance Evidence

Every migration PR needs:

- a changed-path allowlist and before/after public characterization results;
- unchanged committed conversion command and runtime-provenance record;
- corpus comparison showing no unapproved change to output status, timing
  refusal, bar/event/rest counts, or rendered output where the baseline has it;
- import compatibility for callers still using `whole_note_recogniser`; and
- an explicit rollback path (normally reverting the one migration PR).

The FS-06 Architect turns this readiness document into a source-grounded module
map, dependency graph, ordered migration PR list, and test plan. It must reject
the refactor if the functional baseline is not stable enough to distinguish a
refactor regression from an existing recognition defect.
