# Run Record: Palm Mute / Let Ring Minimal Support v0.1

Durable record of the PDF-to-ScoreIR palm mute and let ring technique classification, proximity attachment, GPIF serialization, and parser recovery implementation.

## Metadata
- **Run ID**: `2026-06-02-pdf-palm-mute-let-ring-minimal-v0.1`
- **Product Repository**: `tticom/score2gp`
- **Governance Repository**: `tticom/score2gp-agentops`
- **Product Branch**: `feature/pdf-palm-mute-let-ring-minimal-v0.1`
- **Agentops Branch**: `agent/pdf-palm-mute-let-ring-minimal-v0.1`

---

## 1. Architectural Strategy & Implementation

We implemented minimal note-level support for palm mute (`palm-mute`) and let ring (`let-ring`) technique candidates.

### Key Refinements in `src/score2gp/build_ir.py`

1. **`_classify_technique`**:
   - Added conservative classification mappings:
     - `"palm-mute"`, `"p.m."`, `"p.m"`, `"pm"`, `"palm mute"` -> `"palm-mute"`
     - `"let-ring"`, `"l.r."`, `"l.r"`, `"lr"`, `"let ring"` -> `"let-ring"`

2. **`_attach_symbols_and_techniques`**:
   - Extended the single-note technique visual x-proximity attachment logic (originally slide-only) to also handle `"palm-mute"` and `"let-ring"`.
   - On match, instantiates `PalmMuteTechnique()` and `LetRingTechnique()` respectively.
   - Preserves exact-count single-note fallback when coordinates are missing.

### Key Refinements in `src/score2gp/gpif.py`

1. **`_find_span_notes`**:
   - Extended to collect direct note-level `PalmMute` and `LetRing` coordinates (where `end_event_id` is `None`) into the respective set lists (`palm_mute_notes`, `let_ring_notes`) so they serialize correctly as `<PalmMute>` and `<LetRing>` XML elements in the GPIF document.

### Key Refinements in `src/score2gp/gp_package.py`

1. **Relational Path Deserialization (`_extract_score_ir_from_relational_gpif_root`)**:
   - Added parsing support for `<PalmMute>` and `<LetRing>` using explicit typed models `PalmMuteTechnique()` and `LetRingTechnique()`.
   - Corrected existing `vibrato`, `tie`, and `slide` parsing to use explicit typed models (`VibratoTechnique`, `TieTechnique`, `SlideTechnique`) rather than calling union-wrapped Annotated types as callables.

2. **Classic Path Deserialization (`_extract_score_ir_from_gpif_root`)**:
   - Added parsing support for `<PalmMute>` and `<LetRing>` using explicit typed models `PalmMuteTechnique()` and `LetRingTechnique()`.
   - Corrected classic `slide` parsing to use explicit `SlideTechnique()` instantiation.

---

## 2. Public Test Results

All 446 public tests passed cleanly in the WSL environment:

```text
============================= 446 passed in 29.00s =============================
```

### Key Additions in Test Suites

1. **`tests/test_symbol_attachment.py`**:
   - Added `test_proximity_palm_mute_let_ring_attachment` verifying proximity alignment, alternate classifications, midpoint ambiguity refusals, and single-note fallback behavior for both palm mute and let ring.

2. **`tests/test_gp_writer.py`**:
   - Added `test_gpif_palm_mute_let_ring_roundtrip` verifying that both techniques roundtrip correctly through GPIF serialization, that direct `<PalmMute>` and `<LetRing>` elements are present in the resulting GPIF XML, and that they recover successfully via both the classic and relational parsing paths.

---

## 3. Private Smoke & Quality Audit Results

The quality audit was successfully executed across all private inputs:

### Post-Serialization Quality Audit Table

| Input Label | Status | Quality Category | ScoreIR Notes | GPIF Notes | Matched Frets |
| :--- | :---: | :--- | :---: | :---: | :---: |
| `private_input_1` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 |
| `private_input_2` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 |
| `private_input_custom` | `fail` | `gp_output_empty_or_near_empty` | 0 | 0 | 0 |
| `private_input_custom_lesson_3` | `pass` | `gp_output_technique_loss_expected` | 451 | 451 | 451 |
| `private_input_custom_lesson_4` | `pass` | `gp_output_technique_loss_expected` | 546 | 546 | 546 |
| `private_input_custom_lesson_5` | `pass` | `gp_output_technique_loss_expected` | 295 | 295 | 295 |
| `private_input_custom_lesson_6` | `pass` | `gp_output_technique_loss_expected` | 115 | 115 | 115 |
| `private_input_custom_lesson_7` | `pass` | `gp_output_technique_loss_expected` | 624 | 624 | 624 |
| `private_input_custom_melodic_soloing` | `pass` | `gp_output_fret_matching_suspect` | 16 | 16 | 16 |

All Lessons 3–7 and melodic soloing passed with zero regressions and remained fully stable.

---

## 4. Verification & Testing

### Executed Validation Command Block & Outcomes

```bash
# 1. Run unit and integration tests
wsl env PYTHONPATH=. .venv/bin/pytest tests/test_symbol_attachment.py
wsl env PYTHONPATH=. .venv/bin/pytest tests/test_gp_writer.py -k "palm or mute or let or ring"
wsl env PYTHONPATH=. .venv/bin/pytest

# 2. Run private pipeline and quality audit
wsl env PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py

# 3. Export and diff schemas
wsl env PYTHONPATH=. .venv/bin/python3 -m score2gp.cli export-schema --out schemas
git diff -- schemas

# 4. Validate output IR files
wsl env PYTHONPATH=. .venv/bin/python3 -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json

# 5. Check workspace whitespace/diff check
git diff --check

# 6. Verify git tracked private files
git ls-files fixtures/private work
```

### Outcomes & Evidence:
1. **Specific Proximity Tests**: `wsl env PYTHONPATH=. .venv/bin/pytest tests/test_symbol_attachment.py` -> `7 passed`.
2. **Specific Roundtrip Tests**: `wsl env PYTHONPATH=. .venv/bin/pytest tests/test_gp_writer.py -k "palm or mute or let or ring"` -> `5 passed`.
3. **Full Public Test Suite**: `wsl env PYTHONPATH=. .venv/bin/pytest` -> `446 passed`.
4. **Quality Audit**: `wsl env PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py` -> Zero regressions.
5. **Schema Export**: `wsl env PYTHONPATH=. .venv/bin/python3 -m score2gp.cli export-schema --out schemas` -> Executed successfully, zero schema diffs.
6. **IR Format Validation**: `wsl env PYTHONPATH=. .venv/bin/python3 -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json` -> Validated successfully.
7. **Git Whitespace Check**: `git diff --check` -> Completed successfully.
8. **Private-Safety Invariant Audit**: `git ls-files fixtures/private work` -> Output is exactly:
   ```text
   fixtures/private/.gitkeep
   ```

---

## 5. Known Limitations
- Palm mute and let ring are note-level only in this branch.
- Long-range spans, continuation lines, repeated text, and vector markings are not inferred.
