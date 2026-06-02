# Run Record: PDF Technique X-Proximity Assignment v0.1

Durable record of the PDF-to-ScoreIR technique visual x-proximity attachment logic, test suite, and private quality audit verification.

## Metadata
- **Run ID**: `2026-06-02-gpif-technique-proximity-assignment-v0.1`
- **Product Repository**: `tticom/score2gp`
- **Governance Repository**: `tticom/score2gp-agentops`
- **Product Branch**: `feature/pdf-technique-x-proximity-assignment-v0.1`
- **Agentops Branch**: `agent/pdf-technique-x-proximity-assignment-v0.1`

---

## 1. Architectural Strategy & Implementation

We improved the technique-text attachment logic in `_attach_symbols_and_techniques` in `src/score2gp/build_ir.py`.

### Key Refinements in `src/score2gp/build_ir.py`

1. **Ambiguity Epsilon Constant**:
   - Defined `TECHNIQUE_ATTACHMENT_AMBIGUITY_EPSILON = 2.0` units.

2. **Note Coordinate Helper**:
   - Implemented `_get_note_x(note: Note) -> float | None` which retrieves the visual `x` coordinate from the note's provenance raw data. It does not infer `x` from onset ticks.

3. **Slide Technique Attachment**:
   - Matches a slide candidate to the closest unambiguous note in the bar using visual `x` coordinate proximity if `candidate.x` is present.
   - Ambiguity checks refuse alignment and issue warnings if the distance difference between the closest and second-closest note is less than the epsilon.
   - Falls back to the original exact single-note check if visual coordinates are missing.

4. **Hammer-On / Pull-Off Technique Attachment**:
   - Collects candidate note pairs sharing the same bar, same track, same voice, and same string, that are chronologically adjacent (consecutive) and playable (non-rest), where both notes have valid visual `x` coordinates.
   - Pairs are sorted by the distance of their midpoint `(x1 + x2) / 2` to `candidate.x`.
   - Ambiguity checks refuse alignment and issue warnings if the distance difference between the closest and second-closest pair is less than the epsilon.
   - Falls back to the original exact two-note check if visual coordinates are missing.

### Key Additions in `tests/test_symbol_attachment.py`

1. **`test_proximity_technique_attachment_cases`**:
   - Verifies slide visual proximity matching, ambiguity handling, and fallback behavior.
   - Verifies hammer-on visual proximity matching, ambiguity handling, and fallback behavior.
   - Uses dynamically generated MusicXML files to construct test cases with 1, 2, or 3 notes to isolate and assert all behavior permutations.

---

## 2. Public Test Results

All 444 public tests passed cleanly in the WSL environment:

```text
============================= 444 passed in 33.29s =============================
```

---

## 3. Private Smoke & Quality Audit Results

The quality audit was successfully executed across all private inputs under default `allow_remediation=False` path.

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

All Lessons 3–7 and melodic soloing passed with zero regressions.

---

## 4. Verification & Testing

### Executed Validation Command Block & Outcomes
We executed the following validation command block locally to verify the correctness of the changes:

```bash
# 1. Run unit and integration tests
wsl env PYTHONPATH=. .venv/bin/pytest tests/test_symbol_attachment.py
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
1. **Specific Proximity Attachment Tests**: `wsl env PYTHONPATH=. .venv/bin/pytest tests/test_symbol_attachment.py`
   - **Result**: `6 passed` in `16.12s`.
2. **Full Public Test Suite**: `wsl env PYTHONPATH=. .venv/bin/pytest`
   - **Result**: `444 passed` in `33.29s`.
3. **Quality Audit**: `wsl env PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py`
   - **Result**: Output verified with zero regressions.
4. **Schema Export**: `wsl env PYTHONPATH=. .venv/bin/python3 -m score2gp.cli export-schema --out schemas`
   - **Result**: Executed successfully. `git diff -- schemas` produced zero differences.
5. **IR Format Validation**: `wsl env PYTHONPATH=. .venv/bin/python3 -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
   - **Result**: Validated successfully with no format errors.
6. **Git Whitespace Check**: `git diff --check`
   - **Result**: Completed successfully with no trailing whitespace or formatting errors.
7. **Private-Safety Invariant Audit**: `git ls-files fixtures/private work`
   - **Result**: Output is exactly:
     ```text
     fixtures/private/.gitkeep
     ```
     No private inputs, generated GP packages, or intermediate JSON files are tracked in version control.
