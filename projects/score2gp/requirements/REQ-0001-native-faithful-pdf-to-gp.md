# REQ-0001 — Native, faithful PDF → Guitar Pro conversion

- **Status:** `IN_DELIVERY` (current programme; milestone L3-NATIVE)
- **Owner:** maintainer (`tticom`)
- **Recorded in the register:** 2026-09-25. The requirement itself predates the register.

This entry registers an existing requirement. It does not restate it. The authoritative text is:

1. [Native PDF-to-GP programme](../plans/2026-08-19-native-pdf-to-gp-and-audiveris-retirement.md), §1 Outcome and §12 Definition of programme completion (maintainer priority, 2026-08-19).
2. [Lesson 3 working slice](../plans/2026-09-05-lesson3-native-working-slice.md), §2, obligations **U01–U14** (maintainer direction, 2026-09-05), and §3, the L3-NATIVE acceptance contract.

## Summary

Score2GP must read supported born-digital music PDFs and produce editable,
semantically faithful Guitar Pro files through its own recognition and
compilation pipeline, without Audiveris, Java or a mandatory MusicXML sidecar.
The PDF supplies musical truth. Uncertain input is diagnosed, repaired within
bounds, or refused, and never guessed.

## Related requirements

- [REQ-0002](REQ-0002-pluggable-gp-output-targets.md) extends U13 ("Additional explicitly supported Guitar Pro versions") into a pluggable, version-selectable output requirement.

## Acceptance

As defined in the two plans above. Per-input-class qualification and a zero false-success rate are required before any support claim broader than one source.

## Acceptance sources recorded against obligations

- **U09 (repeats, endings, barline kinds and navigation):** `Ex 2 Hands Up.pdf` with its GP7 and GP6 references (private corpus, added 2026-09-25): repeat barlines with alternate endings 1–4.
  - Maintainer direction (2026-09-25): the system must recognise bar ends and their meanings.
  - Baseline at product `71535f3`: production topology finds 3 systems and 17 measures against 11 reference MasterBars.
  - The independent GPIF reader refuses `<Repeat>` and so cannot yet check this source.
- **U03/U08 breadth:** `Can't Find My Way Home (open chord shenanigans).pdf` with a GP 8.1.4 reference, which uses chord diagrams, grace notes, ties, a tuplet, slides, hammer-ons/pull-offs, bends, vibrato, accents and mutes. Maintainer: reproducing it would be "a significant milestone".
