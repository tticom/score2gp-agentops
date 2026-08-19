# Active Plan: Native PDF-to-GP and Audiveris Retirement

The active product direction is defined by:

`projects/score2gp/plans/2026-08-19-native-pdf-to-gp-and-audiveris-retirement.md`

## Outcome

Build a native, evidence-preserving pipeline that extracts the musical and
document meaning present in supported PDFs, resolves missing facts from
explicit caller parameters and versioned defaults, and produces semantically
faithful, independently validated Guitar Pro files without Audiveris or a
mandatory MusicXML sidecar.

## Operating posture

- Extract and classify text as semantic evidence, including title/credits,
  instrument and track labels, tuning, capo, tempo, meter, key, chord symbols,
  lyrics, techniques, repeats, endings, and navigation instructions.
- Treat page geometry as evidence to diagnose and reconstruct. When topology
  is incomplete or contradictory, identify why, attempt bounded repair or
  cross-lane reconciliation, and expose correction candidates.
- Refuse only after evidence-preserving repair, reconciliation, and configured
  correction paths cannot resolve an ambiguity safely.
- Preserve uncertainty and provenance; never force a plausible-looking score
  by widening tolerances, scaling durations, inventing measures, or fabricating
  string/fret assignments.
- Prefer explicit PDF evidence over caller parameters, and caller parameters
  over versioned Score2GP defaults, independently for every field.
- Define success through source fidelity, musical invariants, GP referential
  integrity, independent parsing, and Guitar Pro open/save/reopen acceptance.

The previous PDF-only Tab-to-GP MVP is archived at
`projects/score2gp/archive/2026-08-19-retired-pdf-only-tab-to-gp-active-plan.md`.
