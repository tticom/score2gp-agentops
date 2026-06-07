Title: Strengthen PDF staff notation diagnostics contract tests

Context:
You are working in `tticom/score2gp` after product PR #182 merged. The project goal is born-digital PDF guitar TAB to playable Guitar Pro without mandatory MusicXML/MXL. Standard notation staff evidence is the future source of reliable rhythm. TAB spacing must not be treated as authoritative timing. OCR, Audiveris, scanned PDF support, and reference GP input dependency remain excluded.

Current verified state:
PR #182 merged into main as `402a12f22588a4fc893d9f2b6b626cb24fdc4ba8`.
It added:
- `src/score2gp/pdf_staff_geometry.py`
- `src/score2gp/pdf_staff_notation_diagnostics.py`
- changes to `src/score2gp/pdf.py`
- `tests/test_pdf_staff_geometry_diagnostics.py`

Reviewer inspection found:
- New schema module is focused.
- New diagnostics builder is mostly focused.
- `pdf.py` is already oversized and now has diagnostic orchestration.
- `_detect_notation_staff_groups()` silently catches `Exception` and returns empty diagnostics.
- `inspect_pdf()` silently catches diagnostic build failures and emits `{"staves": []}`.
- Existing tests only call `build_notation_diagnostics()` directly and do not prove the full `inspect_pdf()` output contract.
- Do not move to smoke refresh until tests prove the diagnostic contract.

Branch:
Create from product `main`:
`test/pdf-staff-notation-diagnostics-contract-v0.1`

Goal:
Strengthen tests for `pdf_staff_notation_diagnostics` without adding parsing capability and without changing GP output behaviour.

Non-goals:
- No duration extraction.
- No notehead/rest/beam/flag/dot/tie/tuplet parser.
- No SMuFL PUA-to-duration mapping.
- No vector glyph classifier.
- No visual spacing as authoritative rhythm.
- No broad rewrite of `pdf.py`.
- No private/generated artifacts committed.

Constraints:
- Keep output schema stable unless a diagnostic failure status is deliberately added and tested.
- Do not emit raw span text, PUA strings, individual primitive coordinates, screenshots, overlays, raw diagnostics, local paths, private fixture names, or private PDF content.
- Use synthetic/mocked data only for public tests.
- Keep changes small and reviewable.

Required pre-flight checks:
```bash
cd /home/tticom/work/score2gp-workspace/score2gp
git fetch --all --prune
git switch main
git pull --ff-only origin main
git status
gh pr view 182 --web=false
git ls-files fixtures/private work
git status --ignored
find . -path "./.git" -prune -o -type f -size +10M -print
```

Implementation guidance:

Add tests that serialize PdfStaffNotationGeometryDiagnostics via model_dump() or the project’s supported Pydantic compatibility path and assert:
no raw span text appears,
no PUA/private-use glyph strings appear,
no individual primitive coordinate dumps appear,
only aggregate primitive counts and font-name counts are emitted.
Add tests for outside-staff filtering:
text outside the padded staff zone is ignored,
drawings outside the padded staff zone are ignored,
empty/whitespace text spans are ignored.
Add tests for staff_index preservation and stable output shape:
staff_index == 1,
output contains staves,
each staff contains staff and primitives,
primitives.text_span_count_by_font is a count map only.
Add at least one test covering the inspect_pdf() integration boundary if practical with monkeypatching:
pdf_staff_notation_diagnostics key exists in page output,
diagnostics are serialized under that key,
no raw text is present under that diagnostics key.
Inspect the broad exception handling:
If possible, replace silent diagnostic failure with a private-safe diagnostic failure status or warning.
If that would require schema change beyond the test branch, stop and report a cleanup branch recommendation instead.
Do not hide broken diagnostics as indistinguishable empty staves without at least a test documenting the current behaviour.

Validation:

env PYTHONPATH=src .venv/bin/python3 -m pytest tests/test_pdf_staff_geometry_diagnostics.py -v
env PYTHONPATH=src .venv/bin/python3 -m pytest -q
git diff --check
git status
git ls-files fixtures/private work
find . -path "./.git" -prune -o -type f -size +10M -print

Acceptance criteria:

Tests prove private-safe output.
Tests prove out-of-zone filtering.
Tests prove staff_index.
Tests prove stable pdf_staff_notation_diagnostics output shape.
No raw text/PUA/private glyph strings or individual primitive coordinate dumps are emitted by diagnostics.
Existing tests pass.
No private/generated artifacts are tracked.

Stop conditions:

Stop if local main is not synced.
Stop if PR #182 is not present on main.
Stop if private/generated files are tracked.
Stop if strengthening tests requires broad pdf.py rewrite.
Stop if you discover diagnostics failures are being silently hidden and cannot fix safely in a small test/cleanup patch.

Reporting format:
Verdict:
Files changed:
Commands run:
Test results:
Privacy invariant result:
Contract behaviours now covered:
Known limitations:
Commit hash:
PR link:
Next recommended task:


My practical recommendation: do this test-contract branch first. After that, do a separate cleanup branch for the silent exception handling if the tests expose it as a real behaviour problem. Then run the private-safe smoke refresh.
