# Approved Task Queue: score2gp

This file contains ordered, human-approved, bounded task prompts.

`ACTIVE_TASK.md` remains the immediate execution contract. Agents may promote the next eligible approved queue item into `ACTIVE_TASK.md` without further human approval only when the previous task has been human-merged or explicitly human-closed, prerequisites are satisfied, and the task remains within its written scope.

Agents must not skip, reorder, invent, or materially modify queue items without human approval.

Human merge remains required for every PR.

## Queue Status Values

- `APPROVED`: may be promoted into `ACTIVE_TASK.md` when prerequisites are met.
- `ACTIVE`: currently copied into `ACTIVE_TASK.md`.
- `BLOCKED`: cannot proceed without human decision.
- `DONE`: human-merged or explicitly human-closed and verified.
- `SUPERSEDED`: no longer valid because a later human-approved task replaced it.

---

## Task 1 — Synthetic standard-staff dense-margin fixture MVP

Status: APPROVED

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

---

## Task 2 — Synthetic sparse standard-staff baseline fixture

Status: APPROVED

Owning repo: `score2gp`

Branch:
`feature/standard-staff-sparse-fixture-v0.1`

PR title:
`test(pdf): add sparse standard-staff diagnostics fixture`

Purpose:
Add a minimal synthetic standard-staff fixture to prove fallback/baseline diagnostics behaviour when the staff has almost no extra primitives.

Prerequisites:

* Task 1 is human-merged and verified on product `main`.

Allowed product files:

* `fixtures/public/generated_standard_staff_sparse.json`
* `tests/fixtures/pdf/make_standard_staff_diagnostics_pdfs.py`
* generated synthetic sparse PDF if fixture convention requires committing it
* `tests/test_pdf_standard_staff_diagnostics_fixtures.py`

Non-goals:

* Do not alter dense-margin behaviour except if a bug is exposed.
* Do not add wide curves or complex clusters.
* Do not infer musical semantics.

Implementation guidance:

* Reuse the generator from Task 1.
* Add one sparse 5-line standard-staff fixture.
* Keep the fixture deliberately minimal.
* Add focused assertions for low primitive counts / absence of dense margin behaviour.
* Assertions must be robust to small geometry-count changes but should catch obvious regression.

Validation:

```bash
git diff --check
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py
.venv/bin/python -m pytest tests/test_pdf_staff_geometry_diagnostics.py
```

Acceptance criteria:

* Sparse fixture JSON exists.
* Sparse generated PDF exists if convention requires.
* Focused tests pass.
* No semantic inference or private artifacts.

Stop conditions:
Same as Task 1.

Reporting:
Same as Task 1.

---

## Task 3 — Synthetic wide-curve standard-staff fixture

Status: APPROVED

Owning repo: `score2gp`

Branch:
`feature/standard-staff-wide-curves-fixture-v0.1`

PR title:
`test(pdf): add wide-curve standard-staff diagnostics fixture`

Purpose:
Add a synthetic fixture with wide Bezier-like curves to validate geometry diagnostics around ties/slurs-like shapes without interpreting them musically.

Prerequisites:

* Task 2 is human-merged and verified on product `main`.

Allowed product files:

* `fixtures/public/generated_standard_staff_wide_curves.json`
* `tests/fixtures/pdf/make_standard_staff_diagnostics_pdfs.py`
* generated synthetic wide-curve PDF if convention requires
* `tests/test_pdf_standard_staff_diagnostics_fixtures.py`

Non-goals:

* Do not classify ties or slurs semantically.
* Do not infer duration, voice, pitch, or articulation.
* Do not change parser or ScoreIR behaviour.

Implementation guidance:

* Extend the existing standard-staff diagnostics generator to support `wide_curves`.
* Draw broad curve primitives spanning across staff content.
* Add tests that validate geometry-only curve diagnostics.
* Use `curve_candidate_count` only for actual curve primitives.
* Keep assertions tied to diagnostics fields, not musical meaning.

Validation:

```bash
git diff --check
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py
.venv/bin/python -m pytest tests/test_pdf_staff_geometry_diagnostics.py
```

Acceptance criteria:

* Wide-curve fixture exists.
* Tests prove curve handling without semantic interpretation.
* Relevant tests pass.

Stop conditions:
Same as Task 1.

Reporting:
Same as Task 1.

---

## Task 4 — Synthetic complex primitive-cluster standard-staff fixture

Status: APPROVED

Owning repo: `score2gp`

Branch:
`feature/standard-staff-complex-cluster-fixture-v0.1`

PR title:
`test(pdf): add complex standard-staff primitive cluster fixture`

Purpose:
Add a synthetic dense primitive cluster fixture to validate standard-staff primitive clustering around notehead-like, accidental-like, stem-like, and ledger-line-like shapes without semantic interpretation.

Prerequisites:

* Task 3 is human-merged and verified on product `main`.

Allowed product files:

* `fixtures/public/generated_standard_staff_complex_cluster.json`
* `tests/fixtures/pdf/make_standard_staff_diagnostics_pdfs.py`
* generated synthetic complex-cluster PDF if convention requires
* `tests/test_pdf_standard_staff_diagnostics_fixtures.py`

Non-goals:

* Do not assign pitch.
* Do not assign duration.
* Do not assign voices.
* Do not identify chords semantically.
* Do not alter ScoreIR event generation.
* Do not perform OCR/scanned PDF work.

Implementation guidance:

* Add generator support for `note_clusters` as purely geometric grouped primitives.
* Simulate noteheads using filled circles/rectangles or text-like primitive markers according to existing fitz conventions.
* Simulate stems and ledger lines geometrically.
* Simulate accidentals as text or path primitives only to stress clustering.
* Add tests for diagnostic cluster counts/bounds or equivalent exposed diagnostic fields.
* If existing diagnostics do not expose enough stable fields, stop and report with a recommended diagnostic schema follow-up rather than inventing semantic assertions.

Validation:

```bash
git diff --check
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py
.venv/bin/python -m pytest tests/test_pdf_staff_geometry_diagnostics.py
```

Acceptance criteria:

* Complex cluster fixture exists.
* Geometry-only tests prove dense primitive cluster handling.
* No semantic interpretation is introduced.
* Relevant tests pass.

Stop conditions:
Same as Task 1, plus:

* stop if required diagnostics fields are not exposed.

Reporting:
Same as Task 1.

---

## Task 5 — Standard-staff fixture coverage review and next implementation decision

Status: APPROVED

Owning repo: `score2gp-agentops`

Branch:
`review/standard-staff-fixture-coverage-v0.1`

PR title:
`docs(review): record standard-staff fixture coverage review`

Purpose:
Review the four synthetic standard-staff fixture slices after Tasks 1–4 and decide whether the fixture system is sufficient to support the next product implementation step.

Prerequisites:

* Task 4 is human-merged and verified on product `main`.

Allowed governance files:

* `projects/score2gp/reviews/2026-06-08-standard-staff-fixture-coverage-review.md`
* `projects/score2gp/APPROVED_TASK_QUEUE.md`
* `projects/score2gp/ACTIVE_TASK.md`

Product repo access:
Read-only inspection and validation only.

Non-goals:

* Do not modify product code.
* Do not add fixtures.
* Do not infer musical semantics.
* Do not start implementation of pitch, rhythm, voice, or ScoreIR event generation.

Implementation guidance:

* Inspect product fixture files added by Tasks 1–4.
* Run targeted diagnostics tests and optionally full pytest.
* Review whether fixture coverage now exercises:

  * dense left margins
  * sparse baseline
  * wide curves
  * complex primitive clusters
* Identify whether diagnostics schema is stable enough for the next implementation stage.
* Recommend the next bounded task.

Validation:

```bash
cd /home/tticom/work/score2gp-workspace/score2gp
git status --short
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py
.venv/bin/python -m pytest tests/test_pdf_staff_geometry_diagnostics.py
```

If reasonable, also run:

```bash
.venv/bin/python -m pytest
```

Acceptance criteria:

* Review record exists in governance repo.
* Review gives a clear verdict:

  * fixtures sufficient for next stage
  * fixtures need more coverage
  * diagnostics schema needs hardening first
  * cannot verify
* Commands and test results are recorded.
* Next task recommendation is concrete and bounded.

Stop conditions:
Stop and report if:

* product tests fail for unclear reasons
* fixture coverage cannot be inspected
* generated artifacts appear unsafe/private/large
* review would require product edits

Reporting:
Same as normal review format.

---

## Deferred / not approved in this queue

The following remain explicitly not approved:

* pitch inference
* duration inference
* clef inference
* key signature inference
* voice assignment
* ScoreIR event generation from standard-staff glyphs
* scanned/OCR PDF handling
* real copyrighted/private PDF fixtures
