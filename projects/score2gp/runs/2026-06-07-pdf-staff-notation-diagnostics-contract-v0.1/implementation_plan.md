# Implementation Plan - Strengthen PDF Staff Notation Diagnostics Contract Tests

This plan describes how we will strengthen contract tests for `pdf_staff_notation_diagnostics` inside the product repository on branch `test/pdf-staff-notation-diagnostics-contract-v0.1` without changing existing Guitar Pro output or adding parsing capabilities.

## User Review Required

> [!NOTE]
> Following your recommendation, we will first implement the contract tests on this branch, including documenting the current behavior of silent exception handling (catching exceptions and returning `{"staves": []}`).
> We will then recommend a separate cleanup branch for handling silent exceptions.

## Proposed Changes

### Tests

#### [MODIFY] [test_pdf_staff_geometry_diagnostics.py](file:///home/tticom/work/score2gp-workspace/score2gp/tests/test_pdf_staff_geometry_diagnostics.py)

We will add the following tests:
1. **`test_diagnostics_private_safety_serialization`**:
   - Build diagnostics using a mock page containing sensitive-looking text (e.g. private lyrics, PUA characters like `\ue000` or SMuFL names, coordinates).
   - Dump using Pydantic serialization (`model_dump()`).
   - Validate that no raw span texts (except font names), PUA glyph strings, or individual coordinate dumps of the drawings are present in the serialized output.
   - Assert only aggregate primitive counts and font-name counts exist.
2. **`test_diagnostics_out_of_zone_filtering`**:
   - Provide drawings and text spans that are outside the padded staff zone (`y0 - 20.0` to `y1 + 20.0` and `x0` to `x1`).
   - Verify they are correctly ignored.
   - Provide empty/whitespace text spans within the zone and verify they are ignored.
3. **`test_diagnostics_shape_and_staff_index`**:
   - Verify that `staff_index == 1` is preserved across systems.
   - Verify the stable output schema shape where each element in `staves` contains exactly `staff` and `primitives`, and `text_span_count_by_font` is only a count map.
4. **`test_inspect_pdf_integration_boundary`**:
   - Use `monkeypatch` to mock `fitz.open` or mock page retrieval in `inspect_pdf()`.
   - Run `inspect_pdf` and verify that the `pdf_staff_notation_diagnostics` key exists in the page output and contains serialized staves, and that no raw text is present under that key.
5. **`test_silent_exception_handling_behavior`**:
   - Verify that when `build_notation_diagnostics` or PyMuPDF calls raise exceptions, `inspect_pdf()` catches the exception and falls back to `{"staves": []}`.

---

## Verification Plan

### Automated Tests
- Run the target test file:
  ```bash
  env PYTHONPATH=src .venv/bin/python3 -m pytest tests/test_pdf_staff_geometry_diagnostics.py -v
  ```
- Run the full test suite to ensure no regressions:
  ```bash
  env PYTHONPATH=src .venv/bin/python3 -m pytest -q
  ```
- Run git diff checks and find command checks to ensure code is clean and no private/large files are tracked:
  ```bash
  git diff --check
  git status
  git ls-files fixtures/private work
  find . -path "./.git" -prune -o -type f -size +10M -print
  ```
