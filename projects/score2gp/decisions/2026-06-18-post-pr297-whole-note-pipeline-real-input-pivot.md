# 2026-06-18: Post-PR297 Whole-Note Pipeline Real-Input Pivot

## Context
Two product PRs have now merged in `tticom/score2gp`:
* PR #296: [Product: Whole-Note Staff Association](https://github.com/tticom/score2gp/pull/296) (Merge commit: `e7523a8450c99d5e919fb60c39fd1f7d0d6d0796`)
* PR #297: [feat(recognition): map whole-note candidates to intermediate representation](https://github.com/tticom/score2gp/pull/297) (Merge commit: `87afec98f812e7309d415ff21b21d298b5636ab1`)

These PRs represent useful internal progress for the intermediate representation pipeline, proving that clean generated fixtures can map whole-note candidates through staff association and into bounded intermediate notes.

However, the user has provided a real mixed notation/tab example containing a visible whole note that Score2GP still does not recognise. The current project state must explicitly pivot away from internal synthetic-only iterations and target real-user acceptance.

## Capability Accepted
* Staff-positioned whole-note candidates can be extracted from clean generated vector fixtures.
* These candidates can be mapped to bounded intermediate whole-note representations (`symbol_type="whole_note"`).
* Mapping gracefully fails closed on ambiguous/missing indices or failed staff association.

## Strict Limitations
* Current evidence does not prove real-score whole-note recognition.
* Synthetic public fixtures passing is not sufficient to claim whole-note recognition works on real user inputs.
* The system still lacks proven staff association, staff-position indexing, and semantic note creation on real mixed notation/tab sources.
* No pitch naming or ScoreIR score construction is proven.
* No GP export is proven.
* Raster/vision whole-note detection is not proven.

## Why Synthetic Fixture Evidence is Insufficient
Iterating exclusively on clean generated PDFs hides real-world failure modes (e.g., raster overlays, complex bounding boxes, fragmented geometry, mixed tab staves). The real-input blocker must be resolved to deliver a user-visible feature.

## Current Real-Input Blocker
Score2GP fails to recognise a visible whole note in a real mixed notation/tab example provided by the user.

## Next Authorised Complete Feature Task
**Real-input whole-note recognition acceptance for mixed notation/tab source**

The next product task must:
* Use the original PDF export if available, otherwise use the supplied screenshot as local-only diagnostic input.
* Perform a pipeline-stage diagnosis to find where the whole note is lost.
* Implement a bounded fix if the vector path is viable.
* Prove exactly why the current approach cannot support the source type (and what replacement path is required) if it is not viable.

## Explicit Non-Authorised Work
* Do not create another synthetic-only internal increment.
* Do not authorise GP export.
* Do not authorise pitch naming as the main goal.
* Do not claim raster recognition is solved.
* Do not commit the user screenshot or original PDF.
