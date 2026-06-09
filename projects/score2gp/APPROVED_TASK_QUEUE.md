# Approved Task Queue: score2gp

This file contains ordered, human-approved, bounded task prompts.

`ACTIVE_TASK.md` remains the immediate execution contract. Agents may promote the next eligible approved queue item into `ACTIVE_TASK.md` without further human approval only when the previous task has been human-merged or explicitly human-closed, prerequisites are satisfied, and the task remains within its written scope.

Agents must not skip, reorder, invent, or materially modify queue items without human approval.

Human merge remains required for every PR.

Current product baseline after product PR #203:
`0b73bd90898bc1f5a1bda6f5e61920d1e952c7f9`

## Queue Status Values

- `APPROVED`: may be promoted into `ACTIVE_TASK.md` when prerequisites are met.
- `ACTIVE`: currently copied into `ACTIVE_TASK.md`.
- `BLOCKED`: cannot proceed without human decision.
- `DONE`: human-merged or explicitly human-closed and verified.
- `SUPERSEDED`: no longer valid because a later human-approved task replaced it.

---

## Completed pre-snapshot tasks

The following earlier queue items are recorded as complete on the post-#203 baseline:

- Task 1 — Synthetic standard-staff dense-margin fixture MVP — DONE.
- Task 2 — Synthetic sparse standard-staff baseline fixture — DONE.
- Task 3 — Synthetic wide-curve standard-staff fixture — DONE.
- Task 4 — Repair and merge complex standard-staff primitive-cluster fixture — DONE.
- Task 5 — Correct standard-staff fixture coverage review from product main — DONE.
- Task 6 — Diagnostics schema stability check before semantic candidates — DONE.

Completion basis:
- Product PRs #197-#203 are merged into product `main`.
- Product PR #203 added the Pydantic JSON schema snapshot gate for staff geometry diagnostics.
- The current baseline remains geometry-diagnostics only.
- No pitch, duration, voice, clef, key signature, rhythm interpretation, or ScoreIR event generation from standard-staff glyphs is approved.

---

## Post-schema-snapshot product backlog

## Task 7 — Record post-#203 product baseline

Status: DONE

Owning repo: score2gp-agentops

Branch:
review/post-schema-snapshot-product-baseline-v0.1

PR title:
docs(review): record post-schema-snapshot product baseline

Purpose:
Record the exact product baseline after PR #203 so later agents have a durable reference point.

Allowed governance files:
- projects/score2gp/reviews/2026-06-08-post-schema-snapshot-product-baseline.md
- projects/score2gp/APPROVED_TASK_QUEUE.md
- projects/score2gp/ACTIVE_TASK.md

Product repo access:
Read-only.

Required evidence:
- product main commit SHA
- recent merged PRs #197-#203
- fixture files present
- schema snapshot file present
- targeted tests
- full pytest if reasonable
- privacy/artifact check

Validation:
cd /home/tticom/work/score2gp-workspace/score2gp
git fetch --all --prune
git switch main
git pull --ff-only human main
git status --short
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py
.venv/bin/python -m pytest tests/test_pdf_staff_geometry_diagnostics.py
.venv/bin/python -m pytest

Acceptance criteria:
- baseline review record exists
- exact commit SHA recorded
- test evidence recorded
- known limitations recorded
- no product files changed

Stop conditions:
- product main is dirty
- tests fail
- product baseline cannot be verified

---

## Task 8 — Add schema snapshot regeneration helper

Status: ACTIVE

Owning repo: score2gp

Branch:
test/diagnostics-schema-snapshot-regenerator-v0.1

PR title:
test(pdf): add diagnostics schema snapshot regeneration helper

Purpose:
Add a small script that regenerates `fixtures/public/pdf_staff_geometry_diagnostics_schema.json` from `PdfStaffNotationGeometryDiagnostics`, so intentional schema changes have a reproducible update path.

Likely product files:
- tests/fixtures/pdf/make_pdf_staff_geometry_schema_snapshot.py
- fixtures/public/pdf_staff_geometry_diagnostics_schema.json
- tests/test_pdf_standard_staff_diagnostics_fixtures.py only if needed

Non-goals:
- do not change schema fields
- do not change diagnostics models
- do not add semantic candidates
- do not change parser behaviour

Validation:
git diff --check
.venv/bin/python tests/fixtures/pdf/make_pdf_staff_geometry_schema_snapshot.py
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py

Acceptance criteria:
- script regenerates the committed schema snapshot byte-for-byte
- snapshot test remains green
- anti-semantic schema test remains green

---

## Task 9 — Add explicit schema required-field tests

Status: DONE

Owning repo: score2gp

Branch:
test/diagnostics-schema-required-fields-v0.1

PR title:
test(pdf): assert required staff diagnostics schema fields

Purpose:
Add tests that assert the diagnostic schema exposes the geometry fields agents depend on, without relying only on full JSON snapshot equality.

Likely product files:
- tests/test_pdf_staff_geometry_schema_contract.py

Fields to assert:
- staves
- staff
- primitives
- morphology
- clustering
- left_margin
- x_aligned_cluster_count
- max_primitives_per_x_aligned_cluster
- cluster_primitive_count_summary
- text_span_count
- curve_candidate_count
- vertical_stroke_candidate_count
- rectangle_candidate_count

Non-goals:
- no schema redesign
- no semantic fields
- no candidates
- no parser changes

Validation:
git diff --check
.venv/bin/python -m pytest tests/test_pdf_staff_geometry_schema_contract.py
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py

Acceptance criteria:
- field-level tests fail if required diagnostic fields disappear
- forbidden semantic names test remains active
- no product behaviour change

---

## Task 10 — Add diagnostics field glossary to product docs

Status: DONE

Owning repo: score2gp

Branch:
docs/staff-diagnostics-field-glossary-v0.1

PR title:
docs(pdf): add staff diagnostics field glossary

Purpose:
Create durable product documentation explaining each geometry diagnostics field, its intended meaning, and what it must not be used to infer yet.

Likely product files:
- docs/testing/standard-staff-fixtures.md
- or docs/testing/staff-geometry-diagnostics.md

Must include:
- field names
- geometry-only meanings
- examples from fixtures
- forbidden semantic interpretations
- how to update schema snapshot intentionally

Validation:
git diff --check
grep -R -i -E "pitch|duration|clef|voice|key signature|notehead" docs/testing/staff-geometry-diagnostics.md docs/testing/standard-staff-fixtures.md || true

Acceptance criteria:
- glossary is product-owned
- glossary is consistent with schema snapshot
- no instruction to infer musical semantics

---

## Task 11 — Add fixture manifest

Status: DONE

Owning repo: score2gp

Branch:
test/pdf-fixture-manifest-v0.1

PR title:
test(pdf): add manifest for synthetic standard-staff fixtures

Purpose:
Create a machine-readable manifest of synthetic PDF fixtures and their source JSON specs.

Likely product files:
- fixtures/public/standard_staff_fixture_manifest.json
- tests/test_pdf_standard_staff_fixture_manifest.py

Manifest entries:
- dense-margin
- sparse
- wide-curves
- complex-cluster

Each entry should include:
- fixture id
- JSON path
- PDF path
- generator script
- expected diagnostic focus
- synthetic=true
- private=false
- scanned=false
- ocr=false
- semantic_inference=false

Validation:
git diff --check
.venv/bin/python -m pytest tests/test_pdf_standard_staff_fixture_manifest.py
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py

Acceptance criteria:
- manifest paths exist
- manifest asserts all fixtures are synthetic
- no private/copyrighted/scanned/OCR fixture is listed

---

## Task 12 — Add manifest-driven fixture smoke test

Status: DONE

Owning repo: score2gp

Branch:
test/pdf-fixture-manifest-smoke-v0.1

PR title:
test(pdf): run standard-staff fixture smoke tests from manifest

Purpose:
Use the fixture manifest to run a generic smoke test over all standard-staff synthetic PDFs.

Likely product files:
- tests/test_pdf_standard_staff_fixture_manifest.py
- or tests/test_pdf_standard_staff_diagnostics_fixtures.py

Non-goals:
- do not replace focused fixture tests
- do not add new fixtures
- do not infer semantics

Validation:
git diff --check
.venv/bin/python -m pytest tests/test_pdf_standard_staff_fixture_manifest.py
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py

Acceptance criteria:
- every manifest fixture loads through inspect_pdf
- diagnostics status is success
- exactly expected minimum staff count is asserted
- manifest and focused tests pass

---

## Task 13 — Add expected diagnostics snapshots for four fixtures

Status: ACTIVE

Owning repo: score2gp

Branch:
test/pdf-diagnostics-fixture-snapshots-v0.1

PR title:
test(pdf): add diagnostics snapshots for standard-staff fixtures

Purpose:
Commit small expected diagnostic JSON snapshots for the four synthetic fixtures to make diagnostic drift visible.

Likely product files:
- fixtures/public/expected_diagnostics_dense_margin.json
- fixtures/public/expected_diagnostics_sparse.json
- fixtures/public/expected_diagnostics_wide_curves.json
- fixtures/public/expected_diagnostics_complex_cluster.json
- tests/test_pdf_standard_staff_diagnostics_snapshots.py

Non-goals:
- no full inspect_pdf output if it includes unstable/noisy fields
- no private paths
- no semantic fields

Validation:
git diff --check
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_snapshots.py
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py

Acceptance criteria:
- stable expected diagnostics snapshots exist
- tests compare current stable subset against snapshots
- no semantic fields appear

---

## Task 14 — Add diagnostics snapshot regeneration helper

Status: APPROVED

Owning repo: score2gp

Branch:
test/pdf-diagnostics-snapshot-regenerator-v0.1

PR title:
test(pdf): add diagnostics snapshot regeneration helper

Purpose:
Add a script to regenerate expected diagnostics snapshots intentionally.

Likely product files:
- tests/fixtures/pdf/make_standard_staff_expected_diagnostics.py
- fixtures/public/expected_diagnostics_*.json
- tests/test_pdf_standard_staff_diagnostics_snapshots.py

Validation:
git diff --check
.venv/bin/python tests/fixtures/pdf/make_standard_staff_expected_diagnostics.py
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_snapshots.py

Acceptance criteria:
- generator regenerates committed snapshots byte-for-byte
- output is stable
- final newlines present
- no volatile paths

---

## Task 15 — Add multi-staff synthetic fixture

Status: APPROVED

Owning repo: score2gp

Branch:
test/pdf-standard-staff-multi-staff-fixture-v0.1

PR title:
test(pdf): add multi-staff standard diagnostics fixture

Purpose:
Add a synthetic PDF with two standard staves on one page to test staff indexing and per-staff diagnostics.

Likely product files:
- fixtures/public/generated_standard_staff_multi_staff.json
- tests/fixtures/pdf/generated_standard_staff_multi_staff.pdf
- tests/fixtures/pdf/make_standard_staff_diagnostics_pdfs.py
- tests/test_pdf_standard_staff_diagnostics_fixtures.py

Non-goals:
- do not infer grand staff
- do not infer instrument grouping
- do not infer clef or pitch
- do not add ScoreIR events

Validation:
git diff --check
.venv/bin/python tests/fixtures/pdf/make_standard_staff_diagnostics_pdfs.py
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py
.venv/bin/python -m pytest tests/test_pdf_staff_geometry_diagnostics.py

Acceptance criteria:
- two staves detected
- staff_index behaviour is tested
- diagnostics are independent per staff

---

## Task 16 — Add multi-system synthetic fixture

Status: APPROVED

Owning repo: score2gp

Branch:
test/pdf-standard-staff-multi-system-fixture-v0.1

PR title:
test(pdf): add multi-system standard diagnostics fixture

Purpose:
Add a synthetic PDF with two systems on one page to test system indexing and staff diagnostics separation.

Likely product files:
- fixtures/public/generated_standard_staff_multi_system.json
- tests/fixtures/pdf/generated_standard_staff_multi_system.pdf
- tests/fixtures/pdf/make_standard_staff_diagnostics_pdfs.py
- tests/test_pdf_standard_staff_diagnostics_fixtures.py

Non-goals:
- no musical continuity
- no bar sequence inference
- no score structure semantics

Validation:
git diff --check
.venv/bin/python tests/fixtures/pdf/make_standard_staff_diagnostics_pdfs.py
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py

Acceptance criteria:
- two systems detected or represented according to current diagnostics
- indexes remain stable
- no semantic interpretation

Stop condition:
If current diagnostics cannot expose system separation reliably, stop and recommend a diagnostics schema task instead of forcing assertions.

---

## Task 17 — Add left-margin threshold edge fixture

Status: APPROVED

Owning repo: score2gp

Branch:
test/pdf-left-margin-threshold-edge-fixture-v0.1

PR title:
test(pdf): add left-margin threshold edge fixture

Purpose:
Add a fixture where text/curve/rectangle markers sit just inside and just outside the left-margin threshold to test boundary behaviour.

Likely product files:
- fixtures/public/generated_standard_staff_left_margin_threshold.json
- tests/fixtures/pdf/generated_standard_staff_left_margin_threshold.pdf
- tests/fixtures/pdf/make_standard_staff_diagnostics_pdfs.py
- tests/test_pdf_standard_staff_diagnostics_fixtures.py

Validation:
git diff --check
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py

Acceptance criteria:
- inside-threshold primitives counted
- outside-threshold primitives not counted
- assertion explains geometry boundary
- no semantic meaning assigned

---

## Task 18 — Add curve-position classification fixture

Status: APPROVED

Owning repo: score2gp

Branch:
test/pdf-curve-position-diagnostics-fixture-v0.1

PR title:
test(pdf): add curve position diagnostics fixture

Purpose:
Separate left-margin curve candidates from staff-body curve primitives using synthetic geometry.

Likely product files:
- fixtures/public/generated_standard_staff_curve_positions.json
- tests/fixtures/pdf/generated_standard_staff_curve_positions.pdf
- tests/fixtures/pdf/make_standard_staff_diagnostics_pdfs.py
- tests/test_pdf_standard_staff_diagnostics_fixtures.py

Non-goals:
- no tie/slur classification
- no articulation semantics

Validation:
git diff --check
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py

Acceptance criteria:
- left-margin curve count is asserted
- staff/body curve primitive count is asserted if exposed
- if body curve count is not exposed, stop and recommend schema extension

---

## Task 19 — Add rectangle-position diagnostics fixture

Status: APPROVED

Owning repo: score2gp

Branch:
test/pdf-rectangle-position-diagnostics-fixture-v0.1

PR title:
test(pdf): add rectangle position diagnostics fixture

Purpose:
Add a fixture that distinguishes left-margin rectangle candidates from body rectangles.

Likely product files:
- fixtures/public/generated_standard_staff_rectangle_positions.json
- tests/fixtures/pdf/generated_standard_staff_rectangle_positions.pdf
- tests/fixtures/pdf/make_standard_staff_diagnostics_pdfs.py
- tests/test_pdf_standard_staff_diagnostics_fixtures.py

Non-goals:
- no rest/note/glyph interpretation

Validation:
git diff --check
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py

Acceptance criteria:
- rectangle_candidate_count is tested for margin
- body rect counts are tested through primitives or clustering
- no semantic labels

---

## Task 20 — Add text-font diversity fixture

Status: APPROVED

Owning repo: score2gp

Branch:
test/pdf-text-font-diversity-fixture-v0.1

PR title:
test(pdf): add text font diversity diagnostics fixture

Purpose:
Add a synthetic fixture using multiple fonts/sizes in the left margin to prove distinct font diagnostics are stable.

Likely product files:
- fixtures/public/generated_standard_staff_text_font_diversity.json
- tests/fixtures/pdf/generated_standard_staff_text_font_diversity.pdf
- tests/fixtures/pdf/make_standard_staff_diagnostics_pdfs.py
- tests/test_pdf_standard_staff_diagnostics_fixtures.py

Validation:
git diff --check
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py

Acceptance criteria:
- distinct_font_count > 1
- max_text_spans_for_single_font asserted
- no semantic interpretation of symbols

---

## Task 21 — Add diagnostic schema extension for body primitive aggregates if needed

Status: APPROVED, but only if Task 18 or 19 stop conditions prove it is needed

Owning repo: score2gp

Branch:
feature/body-primitive-aggregate-diagnostics-v0.1

PR title:
feat(pdf): expose body primitive aggregate diagnostics

Purpose:
Expose stable geometry-only aggregate fields for non-margin staff-body primitives if current diagnostics cannot distinguish them robustly.

Likely product files:
- src/score2gp/pdf_staff_geometry.py
- src/score2gp/pdf_staff_notation_diagnostics.py
- tests/test_pdf_staff_geometry_schema_contract.py
- tests/test_pdf_standard_staff_diagnostics_fixtures.py
- fixtures/public/pdf_staff_geometry_diagnostics_schema.json if schema changes
- schema regeneration script if present

Non-goals:
- no semantic candidates
- no pitch/duration/voice
- no ScoreIR

Validation:
git diff --check
.venv/bin/python -m pytest tests/test_pdf_staff_geometry_schema_contract.py
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py
.venv/bin/python -m pytest tests/test_pdf_staff_geometry_diagnostics.py

Acceptance criteria:
- new fields are geometry-only
- schema snapshot intentionally updated
- forbidden semantic-name test passes
- fixtures use the new fields only if stable

---

## Task 22 — Add product architecture note for geometry candidate boundary

Status: APPROVED

Owning repo: score2gp

Branch:
docs/geometry-candidate-boundary-v0.1

PR title:
docs(pdf): define geometry candidate boundary

Purpose:
Document the boundary between raw diagnostics and future geometry candidate extraction.

Likely product files:
- docs/testing/geometry-candidate-boundary.md
- or docs/testing/staff-geometry-diagnostics.md

Must define allowed candidate terms:
- CircularMarkerCandidate
- VerticalStrokeCandidate
- HorizontalStrokeCandidate
- CurveMarkerCandidate
- RectangleMarkerCandidate
- TextMarkerCandidate
- XAlignedPrimitiveCluster

Must explicitly forbid:
- NoteheadCandidate
- StemCandidate
- ClefCandidate
- PitchCandidate
- DurationCandidate
- VoiceCandidate
- ChordCandidate

Validation:
git diff --check

Acceptance criteria:
- document gives naming rules
- document explains why musical names are deferred
- document names the required diagnostics fields

---

## Task 23 — Add geometry candidate data models

Status: APPROVED

Owning repo: score2gp

Branch:
feature/geometry-candidate-models-v0.1

PR title:
feat(pdf): add geometry candidate data models

Purpose:
Add frozen Pydantic models for geometry-only candidate extraction from diagnostics.

Likely product files:
- src/score2gp/pdf_geometry_candidates.py
- tests/test_pdf_geometry_candidates.py

Allowed model names:
- GeometryCandidate
- CircularMarkerCandidate
- VerticalStrokeCandidate
- HorizontalStrokeCandidate
- CurveMarkerCandidate
- RectangleMarkerCandidate
- TextMarkerCandidate
- XAlignedPrimitiveClusterCandidate

Non-goals:
- do not use notehead/stem/clef/pitch/duration/voice names
- do not integrate into parser
- do not emit ScoreIR
- do not infer music semantics

Validation:
git diff --check
.venv/bin/python -m pytest tests/test_pdf_geometry_candidates.py
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py

Acceptance criteria:
- models are frozen/typed
- no semantic names
- tests cover construction and schema
- no integration yet

---

## Task 24 — Add anti-semantic tests for geometry candidate models

Status: APPROVED

Owning repo: score2gp

Branch:
test/geometry-candidate-anti-semantic-gate-v0.1

PR title:
test(pdf): guard geometry candidates against semantic leakage

Purpose:
Add tests that fail if geometry candidate models or schemas contain forbidden semantic names.

Likely product files:
- tests/test_pdf_geometry_candidates.py
- tests/test_pdf_staff_geometry_schema_contract.py

Forbidden words:
- notehead
- stem
- clef
- pitch
- duration
- voice
- chord
- key_signature
- time_signature
- beat
- rhythm

Validation:
git diff --check
.venv/bin/python -m pytest tests/test_pdf_geometry_candidates.py

Acceptance criteria:
- forbidden words are checked against model schema and public names
- geometry-only terms remain allowed

---

## Task 25 — Add candidate extractor skeleton

Status: APPROVED

Owning repo: score2gp

Branch:
feature/geometry-candidate-extractor-skeleton-v0.1

PR title:
feat(pdf): add geometry candidate extractor skeleton

Purpose:
Add a pure function that accepts `NotationStaffDiagnostics` and returns an empty or minimal `GeometryCandidateSet`, without implementing extraction rules yet.

Likely product files:
- src/score2gp/pdf_geometry_candidates.py
- src/score2gp/pdf_geometry_candidate_extraction.py
- tests/test_pdf_geometry_candidate_extraction.py

Non-goals:
- no real extraction rules beyond pass-through metadata
- no parser integration
- no ScoreIR
- no semantic candidates

Validation:
git diff --check
.venv/bin/python -m pytest tests/test_pdf_geometry_candidate_extraction.py
.venv/bin/python -m pytest tests/test_pdf_geometry_candidates.py

Acceptance criteria:
- function exists
- typed return model exists
- tests prove no semantic leakage
- no current diagnostics behaviour changes

---

## Task 26 — Extract left-margin geometry candidates

Status: APPROVED

Owning repo: score2gp

Branch:
feature/left-margin-geometry-candidates-v0.1

PR title:
feat(pdf): extract left-margin geometry candidates

Purpose:
Extract geometry-only candidates from `StaffLeftMarginAggregateDiagnostics`.

Likely product files:
- src/score2gp/pdf_geometry_candidate_extraction.py
- tests/test_pdf_geometry_candidate_extraction.py
- tests/test_pdf_standard_staff_diagnostics_fixtures.py if needed

Allowed outputs:
- TextMarkerCandidate summary
- CurveMarkerCandidate summary
- VerticalStrokeCandidate summary
- RectangleMarkerCandidate summary

Non-goals:
- no clef/key/time interpretation
- no semantic label for what markers mean

Validation:
git diff --check
.venv/bin/python -m pytest tests/test_pdf_geometry_candidate_extraction.py
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py

Acceptance criteria:
- dense-margin fixture produces expected geometry candidates
- sparse fixture produces no margin candidates
- anti-semantic tests pass

---

## Task 27 — Extract x-aligned primitive cluster candidates

Status: APPROVED

Owning repo: score2gp

Branch:
feature/x-aligned-cluster-geometry-candidates-v0.1

PR title:
feat(pdf): extract x-aligned primitive cluster candidates

Purpose:
Extract geometry-only cluster candidates from `XAlignedClusterAggregateDiagnostics`.

Likely product files:
- src/score2gp/pdf_geometry_candidate_extraction.py
- tests/test_pdf_geometry_candidate_extraction.py

Non-goals:
- no note/chord inference
- no duration
- no voice
- no ScoreIR

Validation:
git diff --check
.venv/bin/python -m pytest tests/test_pdf_geometry_candidate_extraction.py
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py

Acceptance criteria:
- complex-cluster fixture produces cluster candidate summary
- max primitive count is preserved
- no musical names appear

---

## Task 28 — Extract curve geometry candidates

Status: APPROVED

Owning repo: score2gp

Branch:
feature/curve-geometry-candidates-v0.1

PR title:
feat(pdf): extract curve geometry candidates

Purpose:
Extract geometry-only curve candidates from diagnostics/primitive summaries.

Likely product files:
- src/score2gp/pdf_geometry_candidate_extraction.py
- tests/test_pdf_geometry_candidate_extraction.py

Non-goals:
- no tie/slur classification
- no phrase/articulation inference

Validation:
git diff --check
.venv/bin/python -m pytest tests/test_pdf_geometry_candidate_extraction.py
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py

Acceptance criteria:
- wide-curve fixture produces curve candidate counts
- left-margin curve and staff-body curve are distinguishable only if diagnostics support it
- stop if diagnostics are insufficient

---

## Task 29 — Add candidate extraction JSON snapshot tests

Status: APPROVED

Owning repo: score2gp

Branch:
test/geometry-candidate-snapshots-v0.1

PR title:
test(pdf): add geometry candidate snapshot tests

Purpose:
Commit expected geometry candidate snapshots for the synthetic fixtures.

Likely product files:
- fixtures/public/expected_geometry_candidates_dense_margin.json
- fixtures/public/expected_geometry_candidates_sparse.json
- fixtures/public/expected_geometry_candidates_wide_curves.json
- fixtures/public/expected_geometry_candidates_complex_cluster.json
- tests/test_pdf_geometry_candidate_snapshots.py

Non-goals:
- no musical semantics
- no ScoreIR

Validation:
git diff --check
.venv/bin/python -m pytest tests/test_pdf_geometry_candidate_snapshots.py
.venv/bin/python -m pytest tests/test_pdf_geometry_candidate_extraction.py

Acceptance criteria:
- candidate snapshots are stable
- no semantic fields
- snapshot tests fail on candidate drift

---

## Task 30 — Add candidate snapshot regeneration helper

Status: APPROVED

Owning repo: score2gp

Branch:
test/geometry-candidate-snapshot-regenerator-v0.1

PR title:
test(pdf): add geometry candidate snapshot regeneration helper

Purpose:
Add a script to regenerate expected geometry candidate snapshots intentionally.

Likely product files:
- tests/fixtures/pdf/make_geometry_candidate_snapshots.py
- fixtures/public/expected_geometry_candidates_*.json

Validation:
git diff --check
.venv/bin/python tests/fixtures/pdf/make_geometry_candidate_snapshots.py
.venv/bin/python -m pytest tests/test_pdf_geometry_candidate_snapshots.py

Acceptance criteria:
- regeneration is deterministic
- final newlines present
- no private paths
- no semantic fields

---

## Task 31 — Add candidate extraction CLI/reporting smoke path

Status: APPROVED

Owning repo: score2gp

Branch:
feature/geometry-candidate-reporting-v0.1

PR title:
feat(pdf): expose geometry candidate reporting for diagnostics

Purpose:
Expose geometry candidate output in a safe diagnostic/reporting path, not in ScoreIR conversion.

Likely product files:
- src/score2gp/pdf.py or relevant diagnostics/reporting module after inspection
- src/score2gp/pdf_geometry_candidate_extraction.py
- tests/test_pdf_geometry_candidate_reporting.py

Non-goals:
- no default semantic conversion
- no ScoreIR events
- no production parser behaviour change unless explicitly diagnostic-only

Validation:
git diff --check
.venv/bin/python -m pytest tests/test_pdf_geometry_candidate_reporting.py
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py

Acceptance criteria:
- candidates can be emitted in diagnostics output
- existing inspect_pdf behaviour remains compatible
- no semantic candidate fields

Stop condition:
If exposing the output would change public API too broadly, stop and propose an API design note first.

---

## Task 32 — Add backwards compatibility test for diagnostics output

Status: APPROVED

Owning repo: score2gp

Branch:
test/pdf-diagnostics-backcompat-v0.1

PR title:
test(pdf): guard diagnostics output backwards compatibility

Purpose:
Ensure existing diagnostics keys remain available after candidate reporting additions.

Likely product files:
- tests/test_pdf_diagnostics_backcompat.py
- fixtures/public/expected_diagnostics_*.json if already present

Validation:
git diff --check
.venv/bin/python -m pytest tests/test_pdf_diagnostics_backcompat.py
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py

Acceptance criteria:
- established diagnostics keys remain present
- schema snapshot remains valid
- no semantic fields

---

## Task 33 — Add product architecture review for geometry candidates

Status: APPROVED

Owning repo: score2gp-agentops

Branch:
review/geometry-candidate-layer-review-v0.1

PR title:
docs(review): review geometry candidate layer

Purpose:
Review Tasks 23-32 and decide whether the geometry candidate layer is ready for a first semantic research task.

Prerequisites:
- Task 32 merged and verified on product main

Allowed governance files:
- projects/score2gp/reviews/2026-06-08-geometry-candidate-layer-review.md
- projects/score2gp/APPROVED_TASK_QUEUE.md
- projects/score2gp/ACTIVE_TASK.md

Product access:
Read-only.

Required evidence:
- product main SHA
- PRs reviewed
- files inspected
- tests run
- schema snapshot status
- anti-semantic test status
- candidate snapshot status
- privacy/artifact check
- clear verdict

Verdict options:
- geometry candidate layer ready for semantic research
- more geometry coverage needed
- schema needs hardening
- cannot verify

Non-goals:
- do not add semantic tasks unless review evidence supports it
- do not modify product code

Validation:
cd /home/tticom/work/score2gp-workspace/score2gp
git status --short
.venv/bin/python -m pytest tests/test_pdf_geometry_candidate_extraction.py
.venv/bin/python -m pytest tests/test_pdf_geometry_candidate_snapshots.py
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py
.venv/bin/python -m pytest

---

## Task 34 — Research-only semantic boundary proposal

Status: APPROVED only after Task 33 says ready

Owning repo: score2gp

Branch:
docs/semantic-boundary-research-v0.1

PR title:
docs(pdf): propose semantic boundary for standard-staff interpretation

Purpose:
Research and document the smallest safe semantic interpretation boundary after geometry candidates are proven.

Likely product files:
- docs/testing/standard-staff-semantic-boundary.md

Non-goals:
- no implementation
- no candidate classes
- no ScoreIR
- no pitch/duration/voice logic

Must answer:
- what semantic unit, if any, is safe to attempt first
- what fixtures prove readiness
- what diagnostics/candidates are inputs
- what must remain deferred
- what acceptance criteria would be needed for implementation

Validation:
git diff --check

Acceptance criteria:
- document is product-owned
- clearly separates research from implementation
- identifies first implementation candidate or says not ready

---

## Task 35 — Governance backlog refresh after geometry candidate review

Status: APPROVED

Owning repo: score2gp-agentops

Branch:
governance/post-geometry-candidate-backlog-refresh-v0.1

PR title:
docs(governance): refresh backlog after geometry candidate review

Purpose:
Update the control-plane queue after Task 33/34, based on evidence.

Allowed governance files:
- projects/score2gp/APPROVED_TASK_QUEUE.md
- projects/score2gp/ACTIVE_TASK.md
- projects/score2gp/reviews/*.md

Non-goals:
- do not invent semantic implementation tasks without product research evidence
- do not mark unmerged work done

Validation:
git diff --check
git status --short
git diff --stat

Acceptance criteria:
- completed tasks marked DONE
- blocked/deferred tasks clearly marked
- next active task is evidence-based

---

## Deferred / not approved yet

The following remain explicitly not approved:

- pitch inference
- duration inference
- clef inference
- key signature inference
- voice assignment
- rhythm interpretation
- ScoreIR event generation from standard-staff glyphs
- scanned/OCR PDF handling
- real/private/copyrighted PDF fixtures

## Task 35 — feat(pdf): expose primitive-level geometry diagnostics

Status: APPROVED

Goal:
Ensure `PrimitiveGeometry` instances (with real `x0/y0/x1/y1` fields) are cleanly serialized and made available to downstream processes, thereby removing the reliance on aggregate counts and unblocking the optical candidate extraction sequence.

Non-goals:
- Do not build candidate extractors themselves yet.
- Do not implement complex heuristic geometric mapping.

