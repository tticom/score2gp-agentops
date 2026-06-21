# Feature: Multi-note Sequencing

## Repository
tticom/score2gp

## Goal
Implement clean, narrow deterministic multi-note sequencing from current `main`.

## Progress Baseline
* Product PR #314 reverted the accidental PR #313 merge.
* Product PR #315 merged the fractional/double-beam extraction fix.
* Fractional/double-beam extraction for the generated `4SixteenthNotes.pdf` fixture is no longer the active blocker.
* PR #313 remains reverted and must not be revived.

## Incremental Progress Check
* The next task must produce new decision-useful evidence by implementing sequential event mapping for multiple valid notation candidates in one staff group.
* Progress is proven by extracting candidates, sorting them by page/system/staff and x-position, accumulating `onset_ticks` within one 4/4 bar, and exporting correctly.

## Authorised Workflow
The task must explicitly follow this loop:
Developer implementation → Reviewer implementation conformance review → PR readiness review.

(Architect research is not required for this immediate task because the sequencing architecture was already approved and the active extraction blocker was resolved by PR #315).

## Explicit Scope & Acceptance
The implementation must:
* Implement sequential event mapping for multiple valid notation candidates in one staff group.
* Sort note outcomes by page/system/staff and x-position.
* Accumulate `onset_ticks` within one 4/4 bar.
* Preserve single-note PR #310 behaviour.
* Preserve PR #315 beam extraction behaviour.
* Reject unsupported chords, multiple staff groups, and sequences exceeding one 4/4 bar.

The Acceptance Fixture Set:
* `fixtures/public/generated_simple/simple/HalfNotes.pdf`
* `fixtures/public/generated_simple/simple/2EighthNotes.pdf`
* `fixtures/public/generated_simple/simple/4QuarterNotes.pdf`
* `fixtures/public/generated_simple/simple/4SixteenthNotes.pdf`

## Constraints and Preservation
Explicit non-goals:
* No rests
* No tab-only conversion
* No chords
* No voices
* No tuplets
* No mixed-duration-with-rest acceptance (`MixedDurations.pdf` remains exploratory/non-acceptance)
* No general conversion
* No PR #313 revival

## Stop Conditions for Developer
The developer must stop if:
* target fixtures fail;
* sequencing requires bridge/export scope beyond authorised files;
* private fixtures are needed;
* branch is dirty;
* tests fail;
* implementation attempts rests/tab/chords/voices/general conversion.
