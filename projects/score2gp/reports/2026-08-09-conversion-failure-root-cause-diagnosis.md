# Comprehensive Diagnostic Report: Score2GP Systemic Conversion Failures & Audit of Investigation Branches

**Date**: 2026-08-09  
**Author**: Antigravity AI (`tticom-automation`)  
**Repository**: `tticom/score2gp-agentops`  
**Branch**: `agy/diagnose-conversion-failures-report`  
**Status**: DIAGNOSTIC_COMPLETE  

---

## 1. Executive Summary

This report delivers a definitive technical diagnosis of why the `score2gp` system fails to produce note-for-note conversions of PDF score inputs (such as `Lesson-5.pdf` and `Lesson-6.pdf`) into Guitar Pro (`.gp`) packages.

Following a rigorous, skeptical audit of four investigation branches (`diagnose-conversion-failures`, `agy/m5-corpus-generalisation-and-report`, `agy/m5-final-report-investigation`, and `agy/omr-translation-accuracy-report-and-fixes`), we confirm that **none of the four branches achieved a working conversion pipeline**. Passing unit test suites (1,122 tests) served as a false verification signal, while previous diagnostic attempts relied on geometric hacks, metric redefinitions, or synthetic approximations that distorted measure and note counts by >300%.

The exact root cause is a fundamental architectural mismatch: `score2gp` relies on PDF font text extraction (`TabRaw`) for TAB fret numbers, which are completely absent in scanned or vector-path rendered sheet music PDFs (`text_lines = 0`). Fallbacks to staff notation OMR auto-partition measures into 3,840-tick buckets when barlines are uncollected, causing cascading measure inflation, while naive pitch-to-fret synthesis maps all notes to open strings (String 1, Fret 0), ignoring arranger fingerings and TAB embellishments.

---

## 2. Skeptical Audit of the Four Investigation Branches

| Branch | Published Report | Primary Claim | Skeptical Audit & Failure Mechanism |
| :--- | :--- | :--- | :--- |
| **`diagnose-conversion-failures`** | `CONVERSION_DIAGNOSTICS_REPORT.md` | `partial_pdf_grouping` failure is caused by strict `outer_tolerance = 24.0` in `pdf.py`. | **HACK / SILENCED ERROR**: Expanded `outer_tolerance` from 24.0pt to 300.0pt (~4.16 in) and deleted the `pdf_candidate_outside_system` warning in `src/score2gp/pdf.py`. This forcibly grabbed digits from adjacent systems across the page and assigned them to arbitrary bars, bypassing safety checks without fixing coordinate alignment. |
| **`agy/m5-corpus-generalisation-and-report`** | `2026-08-08-m5-corpus-generalisation-final-report.md` | Task M5 is complete; system is hardened because gating mechanisms return refusal codes predictably across 4 test PDFs. | **FALSE POSITIVE / 0% SUCCESS**: Out of 4 real test PDFs (`mutopia`, `Derek Trucks`, `Just-Practice`, `Melodic Soloing`), **0 converted**. 3 were refused and 1 crashed with `FileNotFoundError`. The report incorrectly defined "gracefully refusing 100% of inputs" as programme completion. |
| **`agy/m5-final-report-investigation`** | `2026-08-08-m5-investigation-why-system-fails.md` | System fails due to page-boundary measure index reset (`start_bar_index=1` on every page) and horizontal digit over-merging (`7 10` -> `710`). | **LOCALIZED FIX / INCOMPLETE**: Correctly identified two bugs in `pdf.py` text parsing. However, text parsing only operates when PDFs contain PDF font glyphs (`text_lines > 0`). Real vector-path sheet music has 0 text glyphs, so fixing font measure indexing still yields 0 TAB candidates for real scores. |
| **`agy/omr-translation-accuracy-report-and-fixes`** | `2026-08-08-pdf-to-gp-translation-accuracy-analysis-report.md` | Solved conversion by synthesizing missing TAB fingerings and auto-partitioning measures when barlines are uncollected. | **MASSIVE ACCURACY DEGRADATION**: Generated **133 measures / 354 notes** for `Lesson-5` (ground truth: **43 measures / 60 notes**) and **166 measures / 602 notes** for `Lesson-6` (ground truth: **72 measures / 87 notes**). Synthetic pitch mapping (all notes to String 1 Fret 0) ignores arranger fingerings and TAB embellishments. |

---

## 3. Five Systemic Root Causes of Systemic Conversion Failure

### Root Cause 1: Font Text Dependency vs. Vector/Raster Dual-Modality
The `score2gp` pipeline relies on `src/score2gp/pdf.py` (`_extract_pdf_text_candidates`) to extract TAB fret digits via PyMuPDF text line bounding boxes.
- **Born-Digital Text PDFs**: Contain font glyphs (e.g., character `'7'` at coordinate `(x, y)`).
- **Scanned or Vector-Path PDFs** (LilyPond, Finale, Sibelius, Guitar Pro PDF export, PDF printers): Render fret numbers as vector bezier paths or raster images (`text_lines = 0`).
- **Consequence**: `pdf.py` returns 0 `TabRaw` candidates. When `src/score2gp/build_ir.py` tries to align notation pitches with `TabRaw` fret candidates, the pipeline fails with `tab-candidate-missing` or `missing_pdf_grouping`.

### Root Cause 2: Barline-Free Rhythm Auto-Partitioning Destroys Score Structure
When Audiveris or sidecar OMR fails to detect physical barlines in standard staff notation:
- `src/score2gp/notation_omr/timeline.py` aggregates all staff candidates into one giant timeline.
- It then forces measure breaks at fixed capacity intervals (`D_measure = 3840` ticks for 4/4 meter).
- If OMR misses even a single rest or miscalculates a note duration (e.g., reading an eighth note as a quarter note), tick onsets drift out of phase.
- Auto-partitioning creates 90+ synthetic measure splits across the score, destroying time signatures, repeat barlines, track synchronization, and master bar layout.

### Root Cause 3: Decoupled Standard Notation and TAB System Alignment
Guitar sheet music PDFs feature paired staves: a 5-line standard notation staff on top, and a 6-line TAB staff on the bottom.
- `score2gp` runs staff notation OMR and TAB candidate extraction as isolated, decoupled state machines.
- `pdf.py` detects TAB systems page-by-page. If barline detection on the TAB staff misses a vertical line that staff OMR detected, staff measure 5 aligns with TAB measure 4.
- `build_ir.py` queries candidate pools by global measure index (`pools.pop(measure.index)`). When indices drift, candidates from Page 2 are merged into Measure 1 of Page 1, creating garbled pitches and string assignments.

### Root Cause 4: Naive Open-String Pitch-to-Fret Synthesis (`synthesize_missing_tab`)
To bypass `tab-candidate-missing` errors when `TabRaw` is empty, Branch 4 introduced `synthesize_missing_tab=True` in `src/score2gp/build_ir.py`:
- It maps MusicXML pitches directly to guitar tuning: `E4` -> String 1, Fret 0; `B3` -> String 2, Fret 0; `G3` -> String 3, Fret 0; `D3` -> String 4, Fret 0.
- **Why this fails**: A single pitch on a guitar can be played in up to 5 different fretboard positions. Always choosing the open string ignores position play (e.g. 5th or 9th position solos), destroys left-hand fingering logic, and strips away all TAB embellishments (bends, slides, hammer-ons, pull-offs, palm mutes, vibrato).

### Root Cause 5: Test Suite Blindness & False Verification Signals
The product test suite contains 1,122 unit tests, all of which pass. This creates a false impression of correctness because:
- **Synthetic Fixtures**: Tests pass pre-aligned static JSON structures (`tiny_score.ir.json`) directly into `gp_package.py`. They bypass PyMuPDF, Audiveris OMR, image rendering, barline detection, and multi-page layout.
- **Assertion on Refusal**: Tests check that `refusal_code == "missing_pdf_grouping"`. When the pipeline refuses to convert an unaligned score, the test *passes*. Refusing 100% of real documents generates a 100% test pass rate.

---

## 4. Ground Truth Solution Architecture (Pansophy Requirements)

To achieve note-for-note conversion fidelity matching ground truth `.gp` files:

```
[ PDF Score Input ]
        │
        ├──► 1. Visual Dual-Modality OMR Engine
        │       ├── Standard 5-Line Notation OMR (Pitch, Duration, Rhythm, Barlines)
        │       └── Visual 6-Line TAB OMR (Fret Glyphs, String Lines, Barlines, Techniques)
        │
        ├──► 2. Master System & Barline Synchronizer
        │       └── Lock 5-line barlines to 6-line TAB barlines PER SYSTEM before event extraction
        │
        ├──► 3. Biomechanical Fingering & Position Optimizer (Viterbi / Dynamic Programming)
        │       └── If visual TAB is unreadable, optimize fret assignments by minimizing hand movement cost
        │
        └──► 4. Strict IR Alignment & Guitar Pro 7 Packaging
                └── Write exact measure containers, notes, ties, tuplets, and embellishments
```

1. **Optical TAB Fret Recognition**: Replace font-only `TabRaw` text extraction with visual 6-line TAB OMR (detecting printed numbers `0-24` on staff lines).
2. **Paired Staff Barline Locking**: Enforce vertical alignment between standard notation barlines and TAB barlines per system *before* extracting events, preventing measure desynchronization.
3. **Biomechanical Position Optimization**: Implement a dynamic programming solver (minimizing fretboard jump distance and finger stretches) for fallback pitch-to-fret synthesis.
4. **End-to-End Ground-Truth Test Harness**: Replace synthetic unit tests with full integration tests comparing generated `.gp` files against ground-truth `.gp` fixtures using bar-level pitch/rhythm comparators.
