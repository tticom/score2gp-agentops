# Clef Evidence Audit

**Status:** PROPOSED
**Date:** 2026-06-09

## 1. Purpose
This audit visually inspects authorised reference images to establish treble-clef visual reference evidence. This is not a recogniser implementation; rather, it aims to verify that the required symbol exists visually before attempting to map diagnostic candidates to it.

## 2. Public fixture snapshot audit
**Verdict on public fixtures:** Public fixture snapshots alone are insufficient for clef evidence. The generic geometric primitives present in current `left_margin_candidates` lack explicitly documented clef counterparts.

## 3. Reference image visual inspection
**Reference directory:** `reference/tab-notation-reference-images/2026-06-09`

A representative subset of 11 images was visually inspected using the multimodal `view_file` tool.

| File | Treble clef visible? | Key signature visible? | Time signature visible? | Visual notes |
|---|---:|---:|---:|---|
| `Screenshot 2026-06-09 103745.png` | yes | no | no | Treble clef is present at the far left of the standard staff. |
| `Screenshot 2026-06-09 104455.png` | yes | no | no | Treble clef appears at the far left margin before any notes. |
| `Screenshot 2026-06-09 105117.png` | yes | no | no | Treble clef is at the start of the staff. |
| `Screenshot 2026-06-09 103532.png` | yes | no | no | Treble clef opens the standard staff. |
| `Screenshot 2026-06-09 103613.png` | yes | no | no | Treble clef at the left margin. |
| `Screenshot 2026-06-09 104714.png` | yes | no | no | Treble clef at the left margin. |
| `Screenshot 2026-06-09 103956.png` | yes | no | no | Treble clef opens the standard staff. |
| `Screenshot 2026-06-09 104225.png` | yes | no | no | Treble clef at the left margin. |
| `Screenshot 2026-06-09 104819.png` | yes | yes | no | Treble clef is at the far left, followed immediately by a one-flat key signature. |
| `Screenshot 2026-06-09 103505.png` | yes | no | no | Treble clef at the left margin. |
| `Screenshot 2026-06-09 104612.png` | yes | no | no | Treble clef at the left margin. |

## 4. Treble clef visual characteristics learned
Based on the visual evidence, the treble clef exhibits the following traits for future diagnostic mapping:
* The treble clef is the ornate G-clef symbol at the far left of the standard staff.
* It appears before key signature and time signature when those are present.
* It is taller than most noteheads/text glyphs and spans multiple staff lines.
* It has a curled/looped form, unlike sharp signs, numerals, stems, or TAB digits.
* It is associated with the standard notation staff, not the TAB staff.
* It should be treated as visual reference evidence only until diagnostics candidates are mapped.

## 5. Updated verdict
**Verdict: public fixture snapshot evidence remains insufficient, but the new reference images provide sufficient visually confirmed treble-clef reference evidence to proceed to a diagnostics-mapping task.**

## 6. What is now unblocked
**Task 48 — Map diagnostics candidates against visually confirmed treble-clef reference regions.**

This next task should run the existing diagnostics pipeline over the relevant source/reference material and map extracted `left_margin_candidates` / `x_aligned_cluster_candidates` to the visually confirmed treble-clef regions.

## 7. What remains blocked
* Product recogniser implementation remains blocked until diagnostics extraction proves real, reproducible candidate evidence.
* ScoreIR emission remains blocked.
* Key signature recognition remains blocked unless separately visually and diagnostically verified.
* Time signature recognition remains blocked unless separately visually and diagnostically verified.
* Semantic grouping remains blocked until separately designed.
