# Decision: PR #315 Completion and Multi-note Sequencing Authorisation

## 1. Product PR #315 Completion
Product PR #315 has been successfully merged (`7288d7ae0f55fd4ecde189c947a8fcd19937825e`), successfully integrating the narrow fractional/double-beam extraction fix.

## 2. Fractional/Double-Beam Blocker Resolved
PR #315 effectively resolved the extraction blocker for the required public generated fixtures. Specifically:
- `4SixteenthNotes.pdf`: correctly yields four `sixteenth_note_candidate` outcomes.
- `4QuarterNotes.pdf`: correctly yields four `quarter_note_candidate` outcomes.
- `2EighthNotes.pdf`: correctly yields two `eighth_note_candidate` outcomes.

## 3. PR #313 Remains Reverted
Product PR #313 remains safely reverted (via PR #314) and must not be revived under any circumstances.

## 4. New Product Baseline
The new product baseline is set to the current `main` immediately following the merge of PR #315.

## 5. Next Product Task Authorised
A clean, product implementation task for narrow deterministic multi-note sequencing is now authorised from current `main`. The implementation must sort note outcomes by page/system/staff and x-position, and cleanly accumulate `onset_ticks` within one 4/4 bar.

## 6. Acceptance Fixture Set
- `fixtures/public/generated_simple/simple/HalfNotes.pdf`
- `fixtures/public/generated_simple/simple/2EighthNotes.pdf`
- `fixtures/public/generated_simple/simple/4QuarterNotes.pdf`
- `fixtures/public/generated_simple/simple/4SixteenthNotes.pdf`

## 7. Explicit Non-Goals
The following features are explicitly out of scope for the next product task:
- no rests;
- no tab-only conversion;
- no chords;
- no voices;
- no tuplets;
- no mixed-duration-with-rest acceptance (`MixedDurations.pdf`);
- no general conversion;
- no PR #313 revival.

## 8. Required Future Loop
The task must follow this exact loop:
1. Developer implementation;
2. Reviewer implementation conformance review;
3. PR readiness review.

## 9. Architect Research Exception
Architect research is not required for the immediate sequencing task because the multi-note sequencing architecture was already approved during previous tasks, and the extraction blocker has now been resolved by PR #315.

## 10. Stop Conditions
The next Developer must stop if:
* target fixtures fail;
* sequencing requires bridge/export scope beyond authorised files;
* private fixtures are needed;
* branch is dirty;
* tests fail;
* implementation attempts rests/tab/chords/voices/general conversion.
