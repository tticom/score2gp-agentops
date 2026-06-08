# ACTIVE_TASK

Status: APPROVED

Title: Synthetic standard-staff dense-margin fixture MVP

Owning repo: `score2gp`

Branch:
`feature/standard-staff-dense-margin-fixture-v0.1`

PR title:
`test(pdf): add synthetic standard-staff dense-margin fixture`

Purpose:
Implement the first small slice of the standard-staff fixture expansion plan. Prove the product-owned JSON-spec → synthetic PDF → geometry-only diagnostics test loop using one dense left-margin standard-staff fixture.

Prerequisites:
- Product PR #197 is merged.
- Governance validation permission is merged.
- Product repo `main` is clean and up to date.

Allowed product files:
- `fixtures/public/generated_standard_staff_dense_margin.json`
- `tests/fixtures/pdf/make_standard_staff_diagnostics_pdfs.py`
- generated synthetic PDF under `tests/fixtures/pdf/` if this repo convention expects generated PDFs to be committed
- one focused test file, preferably:
  `tests/test_pdf_standard_staff_diagnostics_fixtures.py`
  or an existing relevant diagnostics test file if inspection shows that is the established convention
- product docs only if a tiny clarification is required:
  `docs/testing/standard-staff-fixtures.md`

Non-goals:
- Do not implement all planned fixtures.
- Do not add sparse, wide-curve, or complex-cluster fixtures yet.
- Do not infer pitch, duration, key, clef, voice, rhythm, or musical semantics.
- Do not use real, private, copyrighted, scanned, or OCR PDFs.
- Do not refactor unrelated diagnostics code.
- Do not modify parser or ScoreIR behaviour unless a minimal test-facing hook is strictly required and justified.
- Do not commit large/generated artifacts unless already consistent with existing fixture conventions.

Implementation guidance:
- Inspect existing JSON fixture conventions under `fixtures/public/`.
- Inspect existing PDF fixture generator conventions under `tests/fixtures/pdf/`.
- Create one JSON spec for a synthetic standard staff with dense left-margin text clusters.
- Add or extend a fitz-based generator script to render that JSON into a synthetic born-digital PDF.
- The fixture should include a 5-line standard staff and dense text-like left-margin markers.
- The markers must be geometric/test symbols only. They must not encode musical semantics.
- The test should load the generated PDF and assert `NotationStaffDiagnostics` geometry fields.
- Dense-margin assertions should target text-margin counters such as:
  - `left_margin.text_span_count`
  - `left_margin.distinct_font_count`
  - `left_margin.max_text_spans_for_single_font`
- Do not assert `curve_candidate_count` for a text-based dense-margin fixture.

Validation:
Agents may run relevant non-destructive validation without per-test approval.

Required minimum:
```bash
git diff --check
.venv/bin/python -m pytest tests/test_pdf_staff_geometry_diagnostics.py
```

Also run the new focused test:

```bash
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py
```

If the test file name differs, run the actual new/changed targeted test file.

If fixture generation is script-based, run the generator command and report exact command and output.

Before PR:

```bash
git status --short
git diff --stat
```

Acceptance criteria:

* One dense-margin synthetic standard-staff JSON fixture exists.
* One generated synthetic PDF exists if generated PDFs are committed by existing convention.
* One focused test proves the diagnostic behaviour.
* Test assertions remain geometry-only.
* No private/copyrighted/scanned/OCR files are used.
* Relevant tests pass.
* PR is opened against product `main`.

Stop conditions:
Stop and report if:

* existing fixture conventions are unclear
* the generator would require committing large artifacts
* PyMuPDF/fitz usage differs from expected repo conventions
* diagnostics do not expose the required counters
* implementation would require semantic music inference
* tests fail for unclear reasons
* repo is dirty before work starts
* branch push or PR creation is blocked

Reporting:
Report:

* branch name
* PR link
* commit hash
* files changed
* generated files
* commands run
* tests run and results
* privacy/artifact check result
* known limitations
* next recommended task
