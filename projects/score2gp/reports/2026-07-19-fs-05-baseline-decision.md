# FS-05: Baseline Decision

**Date**: 2026-07-19
**Programme**: Runtime-Provenance and Functional-Stabilisation
**Role**: Project Director

## Objective
Record whether the baseline is liveable, and declare if the `notation_omr` modularisation refactoring (FS-06/FS-07) is authorised.

## Findings
1. **Timing Refusal**: The canonical product pipeline (`score2gp convert`) strictly depends on an external MusicXML sidecar to provide all timing, rhythmic alignments, and rests.
2. **Missing Dependencies**: The private corpus (`Lesson-3` through `Lesson-7`) lacks any such MusicXML sidecars. Consequently, the pipeline systematically refuses conversion (`missing_musicxml`), making it impossible to produce a valid GP package with rhythmic duration or rest inference.
3. **No Uncommitted Runtime**: As verified in FS-02, no uncommitted local auto-OMR paths exist to mitigate this gap.
4. **Untraced Rests**: Since the product route cannot proceed without MusicXML, rests cannot be empirically traced through the ScoreIR and GP generation steps.

## Decision
**The baseline is NOT liveable.** 

The governance rules explicitly state: *"Do not call a baseline liveable while it still relies on timing refusal, untraced rests, or uncommitted runtime code."* 

Because the canonical path relies entirely on missing external dependencies for its core functionality (timing and rests) resulting in timing refusal, it cannot currently support the conversion claim for the target corpus.

## Authorisation
**FS-06 and FS-07 are NOT authorised.**
Refactoring the `whole_note_recogniser.py` (which is currently an isolated diagnostic tool) into a `notation_omr` module is premature. A liveable baseline must be established first—either by integrating an internal auto-OMR engine cleanly into the product route, or by obtaining the required MusicXML timing sidecars for the corpus. 

## Genuine Stop Condition Reached
The programme cannot proceed to FS-06/FS-07. No credible task or pivot remains inside this specific stabilisation programme to bypass the missing MusicXML dependencies without introducing unreviewed architectural changes. The programme stops here to request Reviewer/User intervention.
