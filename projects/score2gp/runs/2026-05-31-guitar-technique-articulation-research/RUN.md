# Run Record: Guitar Technique and Articulation Conversion Blocker Research

- **Date:** 2026-05-31
- **Branch:** `research/guitar-technique-articulation-empty-staff-v0.1`
- **Status:** Research & Diagnosis Phase Complete
- **Target Deliverables:**
  - `docs/domain/guitar-technique-articulation.md` (Domain definition, safe fallbacks, synthetic test plans)
  - `docs/domain/README.md` (Reading list update)
  - `docs/domain/domain-test-matrix.md` (Test matrix mapping)

---

## 1. Key Diagnostic Investigation Findings

### A. Earliest Defective Stage
The earliest defective stage is **Stage 1 (PDF visual inspection) & Stage 2 (fret candidate classification / staff grouping)** in `src/score2gp/pdf.py`.
- ** ब्लॉक (Blocker):** In `Melodic Soloing Masterclass.pdf`, the horizontal lines representing the 6-line tab staff are drawn with a spacing gap of **exactly 26.575 points**.
  - `_tab_line_groups()` has a strict gap boundary `if gap < 6.0 or gap > 24.0: continue` which rejects these lines.
  - `classify_staff_line_group()` restricts 6-line staves to a median gap within `5.5-7.2` or `9.5-15.0` points, rejecting them even if they were grouped.
- **Impact:** 0 tab systems are detected on the page. All fret digit candidates (`"1"`, `"2"`, `"5"`, etc.) fail system and string assignment and are filtered out, resulting in **0 playable candidates** written to `tabraw.json`.
- **Outcome:** The pipeline writes a structurally valid but musically empty staff in both ScoreIR and the `.gp` package.

### B. Candidate Extraction Counts (Private-Safe)
- **Total detected text/geometry candidates:** `133`
- **Playable fret candidates:** `0` (lack of system/string assignment)
- **Non-playable text/technique candidates:** `133`
- **Candidates with string assignment:** `0`
- **Candidates with bar assignment:** `0`
- **Candidates excluded by reason code:**
  - `pdf_fret_page_or_legend_number_excluded`: 23 (digits representing page numbers/legends)
  - `pdf_tuning_standard_detected`: 2
  - `pdf_tuning_label_outside_system`: 6
  - `pdf_non_playable_text_not_string_assigned`: 102 (includes fret digits, chord symbols, and techniques like `H`, `P`, `sl.`, `full`)
- **Candidates preserved into ScoreIR:** `0`
- **Candidates serialized into GPIF:** `0`

### C. Technique Marks Impact
- Fret digits and technique marks (`H`, `P`, `sl.`, `full`) are extracted successfully by MuPDF, but because no tab system was inferred, the entire page’s contents are treated as unassigned/non-playable. Technique marks are ignored harmlessly at Stage 3 without causing events to be deleted, as there are no playable events to construct.

### D. Model & Writer Support Verification
- **ScoreIR:** Extensive support already exists in `src/score2gp/ir.py` via `SlideTechnique`, `BendTechnique`, `HammerOnTechnique`, `PullOffTechnique`, `TieTechnique`, `SlurTechnique`, etc.
- **GPIF Writer (`gpif.py`):** Fully supports serializing these techniques using relational properties (e.g. `<HO>`, `<PO>`, `<Slide>`, `<Bend>`, `<Bended>`).
- **Timing:** Standard notation rhythm and MusicXML timing are safely matched, but the lack of tab candidates leaves the staff empty of fretted notes.

---

## 2. Safe Fallback Behavior (Preservation Contract)
We defined a **Preservation Contract** in our new domain guide:
1. **Never Delete Playable Notes Silently:** Playable notes with safe pitches/strings/frets must be written to ScoreIR even if associated techniques are unsupported.
2. **Warn Loudly:** Technique marks that cannot be serialized must trigger warning codes (`scoreir-technique-skipped`) instead of silent note erasure.
3. **Fail on Unsafe Timing Only:** Structural timing issues (e.g., overfull measures) remain the only justification for compile refusal.

---

## 3. Public Synthetic Fixture Plan
Specified four public-safe synthetic test fixtures to develop and test technique conversions:
- `synthetic_hammer_pull.xml` / `synthetic_hammer_pull.json`
- `synthetic_slides.xml` / `synthetic_slides.json`
- `synthetic_bends.xml` / `synthetic_bends.json`
- `synthetic_mixed_rhythms.xml` / `synthetic_mixed_rhythms.json`

---

## 4. Local Verification Commands
All pytest and CLI tests passed successfully:
- Pytest suite: **406 passed** cleanly.
- Private-safety invariant is pristine (only `fixtures/private/.gitkeep` tracked).
