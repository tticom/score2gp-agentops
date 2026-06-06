# Active Plan: PDF-Only Tab-to-GP MVP

This document outlines the active project plan to establish a direct PDF-to-GP pathway in `score2gp`, enabling conversion of born-digital PDF tabs directly into Guitar Pro (`.gp`) files without requiring a MusicXML/MXL timing sidecar.

## 1. Product Goal

The core product goal of `score2gp` is to take a born-digital vector PDF guitar tab and produce a playable Guitar Pro (`.gp`) package, without requiring a matching MusicXML/MXL timing sidecar as a mandatory input.

## 2. Current Verified State & Baseline

- **Current Baseline**: PDF tab extraction, visual grouping diagnostics, GP writing, validation, and a local PDF-only implementation spike exist.
- **Current Issue**: The PDF-only implementation spike was completed before the active plan was fully reviewed and accepted. Therefore, the implementation is treated as a **draft implementation spike** (under draft PR #176) and is not yet merged.
- **Lesson 3 Sanitized Evidence**: PDF tab extraction on `Lesson 3` successfully recovered:
  - 512 total candidates
  - 461 playable fret candidates
  - 461 fret candidates with system, bar, and string assignment
  - 23 systems
  - 64 bar boxes
  - 0 unassigned string candidates
  - 0 ambiguous string candidates
- **Current Blockers**: The standard `convert` path remains blocked by layout safety gates on `Lesson 3` because of global grouping warnings (e.g. global grouping confidence / partial grouping / `pdf_timing_mapping_not_implemented`) and the lack of a timing/rhythm generation path.

## 3. MVP Definition

The PDF-only tab-to-GP MVP is achieved when:
- Given a supported born-digital PDF tab with safe tab geometry,
- the pipeline compiles a validated `.gp` package without requiring a MusicXML/MXL timing sidecar,
- the resulting GP file opens and validates structurally,
- frets, strings, and notes are mostly equivalent to the source notation,
- rhythmic durations are deterministic and explicitly labelled as inferred from the layout,
- any layout safety gate failures exit with specific, actionable diagnostic codes.

## 4. Safety Model

- **Refusal Conditions**: Unsafe or missing layout geometry must refuse compilation.
- **Ambiguity Gate**: Ambiguous string or bar assignments must refuse compilation.
- **Content Hygiene**: Non-playable text candidates must be excluded and not converted to notes.
- **File Integrity**: Output file generation or intermediate validation does not equate to correctness.
- **Privacy Gate**: Private benchmarks (PDFs, oracle GP files) must remain local and must never be committed to either repository.

## 5. Planned Milestones

The project will proceed through the following milestones sequentially:

- **Milestone A: Active plan**
  - Document the goals, blockers, safety rules, and milestones in this active plan.
- **Milestone B: Draft product PR review**
  - Perform a rigorous code and architectural review of the local implementation spike (draft product PR #176) against this active plan.
- **Milestone C: Public fixture proof**
  - Verify the PDF-only pipeline on a public generated PDF fixture with safe tab geometry, ensuring it compiles a valid `.gp` package with layout-inferred timing warnings.
- **Milestone D: Lesson 3 page-1 private smoke**
  - Run the PDF-only pathway locally on Page 1 of the private `Lesson 3` PDF, ensuring it either produces a valid GP or refuses with a specific, actionable grouping reason.
- **Milestone E: Lesson 3 full-score private smoke**
  - Run the PDF-only pipeline on the entire `Lesson 3` score and evaluate GP output layout and metrics against a reference GP.
- **Milestone F: Rhythm improvement**
  - Upgrade the inferred rhythm policy from a naive density grid toward spacing-aware and x-distance-relative grids.
- **Milestone G: Technique/layout expansion**
  - Support expressive techniques only after the basic notes, measures, strings, and frets are validated.

## 6. Non-MVP Boundaries

The following capabilities are out-of-scope for the MVP:
- No Optical Character Recognition (OCR) support.
- No scanned/non-vector PDF support.
- No arbitrary handwritten or custom layouts.
- No perfect rhythm or tempo guarantees.
- No dependency on Audiveris.
- No dependency on private reference GP files as inputs.

## 7. Plan Change Policy

This plan is a living document and is expected to evolve as evidence emerges. Every update must be driven by concrete code run evidence, PR review comments, or fixture results. Update the active blocker and next task when evidence invalidates a current design assumption.
