# Post-PR #191 Next Priorities v0.1

## Current baseline

Product PR #191 is merged. The project now has a pure standard-staff coordinate position indexing helper in `pdf_geometry.py`. It remains geometry-only and does not infer pitch, clef, noteheads, rhythm, duration, voices, or ScoreIR events.

## Priority sequence

1. Run a post-merge product smoke after syncing `main`.
   - Verify full test suite.
   - Verify public `validate-ir`.
   - Verify privacy checks.
   - Do not create a governance PR unless the smoke finds something worth recording.

2. Research staff-local primitive clustering diagnostics v0.1.
   - Goal: define private-safe, staff-local, left-to-right primitive cluster diagnostics using existing morphology counts and staff-position indexing.
   - This must not infer notes, pitch, rhythm, duration, voices, beats, measures, or ScoreIR events.
   - Preferred task name:
     `research/pdf-standard-staff-primitive-clustering-diagnostics-v0.1`

3. Add an architectural guardrail against diagnostics leaking into playback/timing.
   - Start with a lightweight test or research task.
   - Goal: ensure ScoreIR/build/timing/TAB modules do not import standard-staff diagnostics modules.
   - Do not introduce a new linter dependency unless research justifies it.

4. Defer font-density boundary diagnostics until after primitive clustering research.
   - If pursued, frame it as left-margin font/text density diagnostics.
   - Do not classify clefs, time signatures, key signatures, or musical symbols yet.

5. Defer localized warping/scanned-PDF support.
   - The current target remains born-digital PDFs.
   - Do not complicate the coordinate helper for warped/scanned inputs without evidence.

6. Defer pitch mapping and notehead candidate scanning.
   - Staff-position indexes are geometry.
   - Pitch requires clef/transposition/context.
   - Notehead scanning risks semantic interpretation.
   - These should not be next unless a research task proves the boundary is safe.

## Recommended next task

Next recommended task:

`research/pdf-standard-staff-primitive-clustering-diagnostics-v0.1`

This should be research-only in `tticom/score2gp-agentops`.

The research must define:
- what a staff-local primitive cluster is,
- what geometry primitives may be included,
- how clusters are ordered left-to-right,
- whether `compute_staff_position_index(...)` can be used safely for cluster centroid diagnostics,
- what private-safe schema could be added later,
- what must not be serialized,
- what tests would prove the behaviour,
- exact Developer prompt only if implementation is safe.

## Hard boundaries

Do not implement or imply:
- pitch inference,
- clef handling,
- notehead parsing,
- duration extraction,
- rhythm inference,
- voice assignment,
- bar-local timing grids,
- ScoreIR event creation,
- scanned/OCR PDF support.

## Privacy rules

Do not commit:
- private PDFs,
- GP/GPIF/MusicXML/MXL private files,
- generated diagnostics,
- raw coordinate dumps,
- screenshots,
- overlays,
- local absolute paths,
- private filenames,
- large generated artifacts.
