# ScoreToGP Research Report: Quarter-Rest GP Export Integration v0.1

## Prompt Chain
- Prompt manifest: None
- Operative prompt: projects/score2gp/research/architect-quarter-rest-gp-export-prompt.md
- Prompt files: projects/score2gp/research/architect-quarter-rest-gp-export-prompt.md

## Summary Verdict
**Outcome A Selected:** The existing GP export path can safely export quarter-rest ScoreIR events with a narrow Developer implementation task.

## Verified Metrics
- **Product Repository Inspected:** `tticom/score2gp` on branch `main` at merge commit `07b2552e625581771239f3178b24d9c7d25578f8` (Product PR #319)
- **Commands Executed:** `git checkout main`, `git pull --ff-only`, and static analysis via `git grep -n "class Event" src/score2gp`, `git grep -n "is_rest" src/score2gp`, `git grep -n "def _bars" src/score2gp`
- **Files Inspected:** `src/score2gp/ir.py`, `src/score2gp/gp_package.py`, `src/score2gp/gpif.py`, `tests/test_gp_writer.py`
- **Current Export Path Inventory:**
  - Entry point: `gp_package.py:write_gp`
  - Processing engine: `gpif.py:build_gpif` delegates measure processing to `_bars` where GP7 `<Beat>` elements are synthesized.
- **ScoreIR Representation:**
  - `Event` instances define rests via `is_rest=True`, explicitly enforcing an empty `notes` collection. 
  - Timing (`onset_ticks`, `duration_ticks`) operates identically to note events.

## Artifact Coherence
Our inspection of `gpif.py` confirms that the export architecture already includes explicit branches for rests:
- Rests suppress note extraction (avoiding generation of `<Notes>`/`<Note>` blocks inside a `<Beat>`).
- Rests are assigned a downward stem orientation (`TransposedPitchStemOrientation`) and bypass short-note beaming (`link_to_next` is suppressed).
- A specific XML attribute (`attrs["rest"] = "true"`) is injected into the `<Event>` configuration.
- Measure/timing validation applies symmetrically because the rest duration maps exactly as notes do through `_ticks_to_fraction` and `<Rhythm>`.

## First Fatal Failure
None. Structural support for rests exists in `gpif.py` and isolates rests from existing note logic safely.

## Systemic Failure Pattern
The sole current deficiency is test coverage: `tests/test_gp_writer.py` currently tests note events, ties, tuplets, formatting, and technique metadata, but **no rest tests exist**.

## Supported Hypotheses
- The existing ScoreIR-to-GP export mechanism can be safely extended (or is already capable of) emitting quarter rest durations without breaking existing multi-note timing, matching Outcome A.

## Unverified Hypotheses
- GP7 XML schema correctness: While `gpif.py` outputs structural rests (empty `<Beat>`), actual GP7 import validity for these exported files has not been functionally verified via unit tests containing rests.

## Recommended External Research Questions
None immediately required.

## Recommended Next Implementation Slice
**Developer Task:** Authorize a narrow implementation task targeting `tests/test_gp_writer.py`. The Developer must:
1. Write `test_gpif_rests` or equivalent utilizing a synthetic rest `ScoreIR` or the `QuarterRestThenNotes.pdf` public fixture.
2. Assert that the `.gp` zip payload encodes the rest `<Beat>` accurately without `<Notes>` tags and with correct rhythm.
3. Identify and fix any minor GP XML schema mismatch (e.g. if an explicit `<Rest>` tag is actually mandated inside the Beat) solely within `gpif.py`.

## Required Public Fixtures
No new fixtures are required. The existing public fixture `QuarterRestThenNotes.pdf` (or purely programmatic ScoreIR instantiation) is sufficient.

## Non-Goals and Invariants
- Existing note export behavior remains unaltered and protected by the established `test_gp_writer.py` regression suite.
- No new product features are demanded beyond correctly exporting what PR #319 already models.
- No private artifacts or unverified export claims are included.
