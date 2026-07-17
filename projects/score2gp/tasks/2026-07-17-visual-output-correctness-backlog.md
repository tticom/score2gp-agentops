# Visual Output Correctness Backlog

## CR-01: Complete Safe TAB-Only Contract

Status: IN REVIEW. Product PR #371 is stacked on #372 and remains blocked.

Done only when public tests prove normal unsafe TAB-only conversion refuses,
explicit approximate conversion has a non-strict machine-readable outcome, and
the PR parent chain is independently approved.

## CR-02: Build the Visual Output Probe and First-Divergence Ledger

Status: ACTIVE. Tier 1 research/documentation only.

Identify the exact approved input represented by VO-01. Create a sanitized
per-system/per-measure evidence ledger containing source meter/tempo/title/
barline/tuplet facts, emitted MusicXML facts, ScoreIR events, GPIF master-bar
facts, and the first divergence. Add an equivalent probe for one distinct
corpus input. No product code changes.

Done only when the 4/4-to-12/8 mismatch is located to a single source-to-output
transition and the next code task has a measurable rule and a public-test plan.

## CR-03A: Local tuplet-group evidence and meter resolution

Blocked by CR-02.

- **Clean-Base Rule**: Every product branch for CR-03A must start from the current product `origin/main` (or an independently approved parent). It must NEVER start from recovery `task-92`, product PR #371, product PR #372, or the prototype `3b138a7f` commit.
- **Architect-First Handoff**: This task is Architect-first. No Developer/implementation work starts until the Architect's local tuplet-group association rule has been independently reviewed and approved.
- **Adversarial Public Test Contract**: The synthetic extraction fixture must contain true tuplet `3` marks as well as adversarial elements—specifically TAB fret `3` digits, measure label `3` headers, and unrelated text containing the digit `3` (e.g. metadata `[3:50]`). The tests must prove that only the local standard-staff tuplet group is associated and scaled, ignoring all other unrelated/adversarial `3` candidates.
- **Tuplet Association**: A tuplet must be associated with exactly one local group of three rhythmic events using geometry and rhythmic grouping evidence.
- **No Fallbacks**: No global count threshold and no "11 eighth notes" fallback.
- **Scope Limit**: Scope is explicitly limited to 3:2 eighth-note triplets unless evidence supports another ratio.
- **Regression Guard**: Verify 4/4 triplets, ordinary 6/8, and ordinary 12/8 remain distinct.

## CR-04A: False-rest candidate and per-voice capacity gate

Blocked by CR-03A.

- **Clean-Base Rule**: Every product branch for CR-04A must start from the current product `origin/main` (or an independently approved parent). It must NEVER start from recovery `task-92`, product PR #371, product PR #372, or the prototype `3b138a7f` commit.
- **False-Rest Rejection**: Investigate and remove/reject the Lesson-5 false-rest cause generically.
- **Per-Voice Balance Gate**: Every emitted MusicXML measure must balance independently per voice. A measure with an extra rest or overfull voice must refuse rather than report strict success.
- **Verification**: Verify emitted MusicXML event durations, voices, chords, and backups.

## CR-05: Repair Structural Layout and Titles

Blocked by CR-02; may research in parallel with CR-03.

Separate source double/final barline classification, system/page layout, and
phrase-title anchoring. A double bar does not imply a line break; a title needs
text classification plus geometry and measure ownership.

## CR-06: Key-Signature Semantics

Blocked by CR-02 and CR-05. Replaces the prematurely promoted Task 93.

Detect sharp/flat key evidence or record key as unknown. Do not emit a neutral
key as recognised and do not create accidentals from unknown evidence.

## CR-07: Bounded Embellishment Attachments

Blocked by CR-04 and CR-05.

Implement one technique class at a time with source glyph/geometry, source and
target event ownership, ordering, and a true-negative test. Chordal vibrato is
a separate class.

## CR-08: Canonical Deployment Gate

Blocked by accepted CR-01 through the selected functional tasks.

Merge only reviewed parent-first PRs, install/point the canonical workspace at
the accepted product revision, and rerun the maintainer's exact command with
external output paths. This is the first point at which a canonical result can
be called improved.

## CR-09: Corpus Capability Expansion

Blocked by CR-08. Cluster failures by input class and missing capability.
Scanned/mixed PDFs require explicit support or fast, truthful refusal.

## CR-10: Rename and Split `whole_note_recogniser`

Blocked by CR-03 through CR-07.

Perform a behaviour-preserving refactor after characterization tests exist.
Proposed destination modules: staff recognition/pitch resolution, timeline and
meter reconstruction, source metadata/layout, and notation-event assembly.
Keep a compatibility import during migration; no functional changes in this
task.
