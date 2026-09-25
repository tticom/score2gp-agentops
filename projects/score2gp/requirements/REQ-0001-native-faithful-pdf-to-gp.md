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
