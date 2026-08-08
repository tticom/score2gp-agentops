# Investigation Report: Why the Current System Cannot Produce Accurate GP Files

**Date**: 2026-08-08  
**Author**: Antigravity (AI Coding Assistant)  
**Branch**: `agy/m5-final-report-investigation`  
**Repository**: `tticom/score2gp-agentops`

---

## 1. Executive Summary

Despite a test suite with 1,122 passing tests, the `score2gp` system fails to produce accurate Guitar Pro (`.gp`) files for real-world instructional inputs like `Lesson-5.pdf` and `Lesson-6.pdf`. 

This investigation reveals three critical architectural flaws:
1. **Local vs. Global Bar Indexing Mismatch**: Tab candidate extraction resets measure counting page-by-page, while standard OMR uses global numbering, lumping wrong pages together.
2. **Digit Over-Merging (Adjacent Notes)**: Chronologically adjacent fret numbers (e.g., `7` and `10` written as `7 10`) are merged horizontally into invalid numbers (e.g., `'710'`) and discarded.
3. **Agent Integration & Reversion Loop**: Automated governance loops silently revert correct fixes during branch promotions due to a lack of end-to-end integration validation.

---

## 2. Root Cause 1: Page-Boundary Local Indexing Mismatch

### The Symptom
Pitches and strings are completely garbled across page boundaries. Measure 17 onwards contains notes that belong to Measure 1, or is completely empty.

### The Mechanism
In [`pdf.py`](file:///home/tticom/work/score2gp-workspace/score2gp/src/score2gp/pdf.py), `_detect_tab_systems` originally initialized `next_bar_index = 1` on every page.
* Page 1 Tab Systems: assigned measure indices `1, 2, 3, ... 16`
* Page 2 Tab Systems: assigned measure indices `1, 2, 3, ... 16` (instead of `17, 18, 19...`)

However, standard staff notation OMR (`timeline.py`) processes standard staff measures globally (e.g. 1 to 38). When [`build_ir.py`](file:///home/tticom/work/score2gp-workspace/score2gp/src/score2gp/build_ir.py) alignments occur:
1. Candidate pools are queried by the global index: `pools.pop(measure.index)`
2. For global Measure 17 (on Page 2), the query returns an empty pool because the candidates on Page 2 were labeled local Measure 1.
3. For global Measure 1, the query returns a pool containing Page 1, Page 2, and Page 3 candidates all mixed together.
4. The alignment algorithm aligns the first measure's notes to candidates from Page 2 and Page 3, producing incorrect pitches.

### The Proposed Fix
Introduce a `running_bar_index` tracking mechanism that is passed across pages:
```python
# pdf.py
running_bar_index = 1
for page_number, page in enumerate(doc, start=1):
    systems = _detect_tab_systems(page, page_number, start_bar_index=running_bar_index)
    ...
    # Update running_bar_index based on maximum detected bar index
```

---

## 3. Root Cause 2: Digit Over-Merging (Horizontally Adjacent Notes)

### The Symptom
Massive numbers of notes are omitted from the output. In Lesson-5, the first measure is supposed to contain 12 notes (C major scale arpeggios), but only 6 notes are output.

### The Mechanism
Fret numbers on the same staff line written close to each other (e.g. `7 10` representing consecutive eighth/sixteenth notes) have small horizontal gaps (typically 3px to 5px). 

In `pdf.py`, the horizontal digit merge loop automatically merges digits if `gap <= 5.0` to form multi-digit numbers (like `'1'` and `'0'` into `'10'`).
However, because it lacked sanity bounds:
* Fret `7` and fret `10` were merged into `'710'`.
* Fret `8` and fret `12` were merged into `'812'`.
* Fret `10` and fret `7` were merged into `'107'`.

Since these merged values are greater than the maximum valid fret (36), the parser rejects them as non-playable text, completely discarding the notes.

### The Proposed Fix
Do not merge adjacent digits if the combined text represents an invalid guitar fret number (> 24):
```python
proposed = merged_text + d2["text"]
if proposed.isdigit() and int(proposed) <= 24:
    merged_text += d2["text"]
    ...
else:
    break  # Keep them as separate fret candidates
```

---

## 4. Root Cause 3: Test Suite Fallacy and Agent Reversions

### The Test Suite Fallacy
The 1,121 passing tests in the test suite create a false verification signal because:
* They use **isolated, synthetic fixtures** (e.g. single-measure PDFs or pre-aligned MusicXML files).
* They **mock** the OMR sidecars or run on static cached outputs (e.g. `deterministic_omr.musicxml` which contains hand-crafted or pre-baked notes).
* None of the tests run end-to-end integration on multi-page instructional vector PDFs.

### The Agent Reversion Loop
During M5 promotion cycles, different agents run concurrently on task branches.
* In our investigation, we discovered that `tticomgov-code` pushed a commit (`006fe118`) that **reverted** the page-sequential `running_bar_index` tracking fix in `pdf.py`, re-introducing the indexing bug.
* Because the test suite does not catch this regression (due to the test suite fallacy above), the broken code was promoted without warnings.

---

## 5. Code Changes Checklist for Correct Output
The following changes (committed on branch `agy/m5-final-report-investigation`) are required to produce correct GP files:

1. **[`src/score2gp/pdf.py`](file:///home/tticom/work/score2gp-workspace/score2gp/src/score2gp/pdf.py)**:
   - Implement `running_bar_index` tracking across PDF pages in `_extract_pdf_text_candidates`.
   - Update `_detect_tab_systems` signature to accept `start_bar_index`.
   - Constrain horizontal digit merging to `int(proposed) <= 24` inside the string merging loop.
2. **[`scripts/corpus_harness.py`](file:///home/tticom/work/score2gp-workspace/score2gp/scripts/corpus_harness.py)**:
   - Ensure OMR-generated `.mxl` sidecars are placed in `fixtures/private/` so that the harness does not fail due to missing sidecars or fallback path errors.
