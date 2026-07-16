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

Status: DONE

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
- no fixture outside approved public/private fixture locations is listed

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

Status: DONE

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

Status: DONE

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

Status: DONE

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

Status: DONE

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

Status: DONE

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

Status: DONE

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

Status: DONE

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

Status: DONE

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

Status: DONE, but only if Task 18 or 19 stop conditions prove it is needed

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

Status: DONE

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

Status: DONE

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

Status: DONE

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

Status: DONE

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

Status: DONE

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

Status: DONE

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

Status: DONE

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

Status: DONE

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

Status: DONE

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

Status: DONE

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

Status: DONE

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

Status: DONE

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

Outcome:
- review report merged in governance PR #260
- geometry-only boundary approved for research/backlog continuation
- semantic implementation explicitly not approved
- page-level geometry candidate export gap identified for Task 37

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

Status: DONE

Owning repo: score2gp

Branch:
docs/semantic-boundary-research-v0.1

PR title:
docs(pdf): propose semantic boundary for standard-staff interpretation

Purpose:
Research and document the smallest safe semantic interpretation boundary after geometry candidates are proven.

Unblock evidence:
Task 37 was completed and merged in product PR #346. Page-level `geometry_candidates` now transfers populated diagnostic candidates into `GeometryCandidateSet`, and all four public geometry candidate snapshots contain non-empty candidate output.

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

Status: DONE

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
- unapproved PDF fixture artifacts

## Task 36 — feat(pdf): expose primitive-level geometry diagnostics

Status: DONE

Goal:
Ensure `PrimitiveGeometry` instances (with real `x0/y0/x1/y1` fields) are cleanly serialized and made available to downstream processes, thereby removing the reliance on aggregate counts and unblocking the optical candidate extraction sequence.

Non-goals:
- Do not build candidate extractors themselves yet.
- Do not implement complex heuristic geometric mapping.

---

## Task 37 — Populate page-level geometry candidate export

Status: DONE

Owning repo: score2gp

Branch:
feature/populate-geometry-candidate-export-v0.1

PR title:
feat(pdf): populate geometry candidate export

Purpose:
Make `inspect_pdf()["pages"][...]["geometry_candidates"]` contain the existing read-only geometry candidate data from `NotationStaffDiagnostics`, rather than always serializing empty `GeometryCandidateSet` objects.

Requirement:
Req-118

Evidence basis:
- Req-110 review report: `projects/score2gp/reports/2026-07-08-geometry-candidate-layer-review.md`
- `NotationStaffDiagnostics.left_margin_candidates` and `NotationStaffDiagnostics.x_aligned_cluster_candidates` are already populated from diagnostic evidence.
- `extract_geometry_candidates()` currently returns an unconditional empty `GeometryCandidateSet()`.

Allowed product files:
- `src/score2gp/pdf_geometry_candidate_extraction.py`
- `tests/test_pdf_geometry_candidate_extraction.py`
- `tests/test_pdf_geometry_candidate_snapshots.py`
- `tests/test_pdf_geometry_candidate_reporting.py`
- `tests/test_pdf_candidate_semantic_gate.py`
- `tests/fixtures/pdf/make_geometry_candidate_snapshots.py`
- `fixtures/public/expected_geometry_candidates_*.json`

Non-goals:
- no semantic interpretation
- no ScoreIR event generation
- no pitch, duration, voice, rhythm, clef, key signature, or time signature inference
- no private fixtures
- no broad OCR/scanned PDF support

Validation:
cd /home/tticom/work/score2gp-workspace/score2gp
git diff --check
.venv/bin/python -m pytest -q tests/test_pdf_geometry_candidate_extraction.py tests/test_pdf_geometry_candidate_snapshots.py tests/test_pdf_geometry_candidate_reporting.py tests/test_pdf_candidate_semantic_gate.py
.venv/bin/python scripts/artifact_audit.py

Acceptance criteria:
- `extract_geometry_candidates()` transfers existing diagnostic candidates into `GeometryCandidateSet`
- tests prove populated transfer, not just presence of an empty list
- public geometry candidate snapshots are intentionally regenerated if fixture output changes
- anti-semantic leakage tests remain green
- artifact audit passes

Outcome:
- product PR #346 merged
- full product test suite passed before merge: 886 passed, 1 skipped
- GitHub checks passed before merge
- public geometry candidate snapshots are now non-empty across all four standard-staff fixtures
- Reviewer conformance found no required implementation fixes

---

## Task 38 — Review Req-118 geometry candidate export implementation

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/post-req-118-implementation-review-v0.1

PR title:
docs(review): approve Req-118 geometry candidate export implementation

Purpose:
Record implementation conformance and PR readiness evidence for product PR #346 before promoting Req-111 research.

Evidence basis:
- product PR #346
- `projects/score2gp/reviews/2026-07-08-req-118-implementation-conformance.md`

Outcome:
- implementation conformance verdict: approve implementation
- PR readiness status: READY
- next active task promoted to Req-111 / Task 34

---

## Task 39 — Review Req-111 semantic boundary proposal

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/post-req-111-semantic-boundary-review-v0.1

PR title:
docs(review): review Req-111 semantic boundary proposal

Purpose:
Approve the semantic boundary proposal from PR #347 and update ACTIVE_TASK.md to authorise Req-112.

Evidence basis:
- product PR #347
- `projects/score2gp/reviews/2026-07-08-req-111-semantic-boundary-review.md`

Outcome:
- governance PR #263 merged

---

## Task 40 — Implement semantic boundary validation gate

Status: DONE

Owning repo: score2gp

Branch:
feature/logical-clef-semantic-boundary-v0.1

PR title:
feat(pdf): implement semantic boundary validation gate

Purpose:
Create the foundational logic that transitions `left_margin_primitives` into a `LogicalClefCandidate` failing-closed, based on the Architect's proposal.

Requirement:
Req-112

Evidence basis:
- `docs/testing/standard-staff-semantic-boundary.md`
- `src/score2gp/pdf_candidate_semantic_gate.py`
- `tests/test_pdf_candidate_semantic_gate_logic.py`

Outcome:
- product PR #348 merged

---

## Task 41 — Review Req-112 semantic gate implementation

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/post-req-112-implementation-review-v0.1

PR title:
docs(review): approve Req-112 semantic gate implementation

Purpose:
Record implementation conformance and PR readiness evidence for product PR #348 before promoting Req-113 research.

Evidence basis:
- product PR #348
- `projects/score2gp/reviews/2026-07-08-req-112-semantic-gate-review.md`

Outcome:
- implementation conformance verdict: approve implementation
- PR readiness status: READY
- next active task promoted to Req-113 / Task 42

---

## Task 42 — Research logical clef recognition classification heuristics

Status: DONE

Owning repo: score2gp

Branch:
docs/logical-clef-recognition-v0.1

PR title:
docs(pdf): propose logical clef classification heuristics

Purpose:
Research how to deterministically classify a logical clef candidate into Treble or Bass without modifying underlying geometry logic.

Requirement:
Req-113

Evidence basis:
- `docs/testing/logical-clef-recognition.md`

Outcome:
- product PR #349 merged

---

## Task 43 — Review Req-113 logical clef recognition proposal

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/post-req-113-proposal-review-v0.1

PR title:
docs(review): approve Req-113 logical clef recognition proposal

Purpose:
Review the Architect's proposal for logical clef recognition.

Evidence basis:
- product PR #349
- `projects/score2gp/reviews/2026-07-08-req-113-logical-clef-recognition-review.md`

Outcome:
- governance PR #265 merged

---

## Task 44 — Implement logical clef recognition integration

Status: DONE

Owning repo: score2gp

Branch:
feature/logical-clef-recognition-integration-v0.1

PR title:
feat(pdf): integrate logical clef recognition heuristics

Purpose:
Implement the Developer phase of Req-113 by integrating `classify_logical_clef_candidate` into `evaluate_logical_clef_gate`.

Requirement:
Req-113

Evidence basis:
- `docs/testing/logical-clef-recognition.md`
- `projects/score2gp/ACTIVE_TASK.md`

Outcome:
- Developer implementation PR merged

---

## Task 45 — Review Req-113 logical clef recognition implementation

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/post-req-113-implementation-review-v0.1

PR title:
docs(review): approve Req-113 logical clef recognition implementation

Purpose:
Review the Developer's integration of logical clef heuristics.

Evidence basis:
- product PR #350
- `projects/score2gp/reviews/2026-07-08-req-113-logical-clef-recognition-implementation-review.md`

Outcome:
- governance PR merged

---

## Task 46 — Research quarter rest extraction

Status: DONE

Owning repo: score2gp

Branch:
docs/quarter-rest-recognition-v0.1

PR title:
docs(pdf): propose quarter rest extraction heuristics

Purpose:
Research how to deterministically classify quarter rests from stable staff body geometry.

Requirement:
Req-114

Evidence basis:
- `docs/testing/quarter-rest-recognition.md`
- `projects/score2gp/ACTIVE_TASK.md`

Outcome:
- Architect proposal PR merged

---

## Task 47 — Review Req-114 quarter rest extraction proposal

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/post-req-114-proposal-review-v0.1

PR title:
docs(review): approve Req-114 quarter rest extraction proposal

Purpose:
Review the Architect's proposal for quarter rest extraction.

Evidence basis:
- product PR #351
- `projects/score2gp/reviews/2026-07-08-req-114-quarter-rest-recognition-review.md`

Outcome:
- governance PR #267 merged

---

## Task 48 — Implement quarter rest extraction

Status: DONE

Owning repo: score2gp

Branch:
feature/quarter-rest-extraction-v0.1

PR title:
feat(pdf): implement quarter rest extraction

Purpose:
Implement the Developer phase of Req-114 by extracting quarter rest candidates from `x_aligned_clusters`.

Requirement:
Req-114

Evidence basis:
- `docs/testing/quarter-rest-recognition.md`
- `projects/score2gp/ACTIVE_TASK.md`

Outcome:
- Developer implementation PR merged

---

## Task 49 — Review Req-114 quarter rest extraction implementation

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/post-req-114-implementation-review-v0.1

PR title:
docs(review): approve Req-114 quarter rest extraction implementation

Purpose:
Review the Developer's integration of quarter rest heuristics.

Evidence basis:
- product PR #352
- `projects/score2gp/reviews/2026-07-08-req-114-quarter-rest-recognition-implementation-review.md`

Outcome:
- governance PR merged

---

## Task 50 — Implement semantic candidate JSON snapshot tests

Status: DONE

Owning repo: score2gp

Branch:
feature/req-119-semantic-snapshot-tests-v0.1

PR title:
feat(pdf): implement semantic candidate JSON snapshot tests

Purpose:
Implement the Developer phase of Req-119 by creating deterministic JSON snapshot tests for current semantic candidate outputs:
- logical clef candidate outputs
- quarter rest candidate outputs

Requirement:
Req-119

Evidence basis:
- `projects/score2gp/ACTIVE_TASK.md`

Outcome:
- Developer implementation PR merged

---

## Task 51 — Review Req-119 semantic candidate snapshot tests implementation

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/req-119-review-v0.1

PR title:
docs(review): approve Req-119 semantic candidate snapshot tests implementation

Purpose:
Review the Developer's integration of deterministic public JSON snapshot tests for current semantic candidate outputs.

Requirement:
Req-119

Evidence basis:
- product PR #353
- `projects/score2gp/reviews/2026-07-09-req-119-semantic-snapshot-tests-review.md`

Outcome:
- governance PR merged

---

## Task 52 — Implement semantic candidate CLI/reporting smoke path

Status: DONE

Owning repo: score2gp

Branch:
feature/req-120-semantic-cli-smoke-path-v0.1

PR title:
feat(pdf): implement semantic candidate CLI/reporting smoke path

Purpose:
Implement the Developer phase of Req-120 by exposing semantic candidate extraction through the diagnostics CLI.

Requirement:
Req-120

Evidence basis:
- `projects/score2gp/ACTIVE_TASK.md`

Outcome:
- Developer implementation PR merged

---

## Task 53 — Review Req-120 semantic candidate CLI/reporting smoke path implementation

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/req-120-review-v0.1

PR title:
docs(review): approve Req-120 semantic candidate CLI/reporting smoke path implementation

Purpose:
Review the Developer's integration of semantic candidates into CLI/reporting diagnostics.

Requirement:
Req-120

Evidence basis:
- product PR #354
- `projects/score2gp/reviews/2026-07-09-req-120-semantic-cli-smoke-path-review.md`

Outcome:
- governance PR merged

---

## Task 54 — Implement fail-closed semantic coverage expansion

Status: DONE

Owning repo: score2gp

Branch:
feature/req-121-fail-closed-semantic-coverage-v0.1

PR title:
feat(pdf): implement fail-closed semantic coverage expansion

Purpose:
Implement the Developer phase of Req-121 by expanding semantic candidate extraction coverage to verify fail-closed handling on complex rests (whole rests, half rests) and overlapping/polyphonic geometry clusters.

Requirement:
Req-121

Evidence basis:
- `projects/score2gp/ACTIVE_TASK.md`

Outcome:
- Developer implementation PR merged

---

## Task 55 — Review Req-121 fail-closed semantic coverage expansion implementation

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/req-121-review-v0.1

PR title:
docs(review): approve Req-121 fail-closed semantic coverage expansion implementation

Purpose:
Review the Developer's integration of fail-closed checks for whole rests, half rests, and overlapping/polyphonic geometry clusters.

Requirement:
Req-121

Evidence basis:
- product PR #355
- `projects/score2gp/reviews/2026-07-09-req-121-fail-closed-semantic-coverage-review.md`

Outcome:
- governance PR merged

---

## Task 56 — Implement semantic candidate no-ScoreIR leakage gate

Status: DONE

Owning repo: score2gp

Branch:
feature/req-122-no-scoreir-leakage-gate-v0.1

PR title:
feat(pdf): implement semantic candidate no-ScoreIR leakage gate

Purpose:
Implement the Developer phase of Req-122 by adding/verifying a strict gate test proving that the presence of semantic candidates does not alter the legacy ScoreIR output or playable GP package.

Requirement:
Req-122

Evidence basis:
- `projects/score2gp/ACTIVE_TASK.md`

Outcome:
- Developer implementation PR merged

---

## Task 57 — Review Req-122 semantic candidate no-ScoreIR leakage gate implementation

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/req-122-review-v0.1

PR title:
docs(review): approve Req-122 semantic candidate no-ScoreIR leakage gate implementation

Purpose:
Review the Developer's integration of a strict isolation gate test for ScoreIR and GP packages.

Requirement:
Req-122

Evidence basis:
- product PR #356
- `projects/score2gp/reviews/2026-07-09-req-122-no-scoreir-leakage-gate-review.md`

Outcome:
- governance PR merged

---

## Task 58 — Real-world / approved-corpus audit for semantic candidates

Status: DONE

Owning repo: score2gp

Branch:
feature/req-123-corpus-audit-v0.1

PR title:
feat(pdf): perform real-world / approved-corpus semantic candidate audit

Purpose:
Perform the Developer phase of Req-123 by auditing the semantic candidate extraction model across public and private fixtures.

Requirement:
Req-123

Evidence basis:
- `projects/score2gp/ACTIVE_TASK.md`

Outcome:
- Developer implementation PR merged

---

## Task 59 — Review Req-123 real-world / approved-corpus audit for semantic candidates implementation

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/req-123-review-v0.1

PR title:
docs(review): approve Req-123 real-world / approved-corpus audit for semantic candidates implementation

Purpose:
Review the Developer's strategic audit report on semantic candidate extraction performance.

Requirement:
Req-123

Evidence basis:
- `projects/score2gp/reviews/2026-07-09-req-123-corpus-audit-review.md`

Outcome:
- governance PR merged

---

## Task 60 — Implement semantic candidate model consolidation and schema hardening

Status: DONE

Owning repo: score2gp

Branch:
feature/req-124-semantic-model-schema-hardening-v0.1

PR title:
feat(pdf): consolidate semantic candidate models and harden schemas

Purpose:
Implement the Developer phase of Req-124 by refining the LogicalClefCandidate and QuarterRestCandidate schemas and consolidating pydantic models based on the Req-123 audit results.

Requirement:
Req-124

Evidence basis:
- `projects/score2gp/ACTIVE_TASK.md`

Outcome:
- Developer implementation PR merged

---

## Task 61 — Review Req-124 semantic candidate model consolidation and schema hardening implementation

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/req-124-review-v0.1

PR title:
docs(review): approve Req-124 semantic candidate model consolidation and schema hardening implementation

Purpose:
Review the Developer's consolidation and validation hardening for LogicalClefCandidate and QuarterRestCandidate models.

Requirement:
Req-124

Evidence basis:
- `projects/score2gp/reviews/2026-07-09-req-124-semantic-model-schema-hardening-review.md`

Outcome:
- governance PR merged

---

## Task 62 — Multi-clef candidate classification (Bass and Alto)

Status: DONE

Owning repo: score2gp

Branch:
feature/req-125-multi-clef-candidate-v0.1

PR title:
feat(pdf): implement multi-clef candidate classification (bass and alto)

Purpose:
Implement the Developer phase of Req-125 by extending left-margin heuristics to detect and classify Bass and Alto clef geometries without OCR.

Requirement:
Req-125

Evidence basis:
- `projects/score2gp/ACTIVE_TASK.md`

Outcome:
- Developer implementation PR merged

---

## Task 63 — Review Req-125 multi-clef candidate classification implementation

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/req-125-review-v0.1

PR title:
docs(review): approve Req-125 multi-clef candidate classification implementation

Purpose:
Review the Developer's multi-clef candidate classification heuristics and test coverage.

Requirement:
Req-125

Evidence basis:
- `projects/score2gp/reviews/2026-07-09-req-125-multi-clef-candidate-review.md`

Outcome:
- governance PR merged

---

## Task 64 — Generate public bass and alto clef fixtures

Status: DONE

Owning repo: score2gp

Branch:
test/req-126-bass-alto-clef-fixtures-v0.1

PR title:
test(pdf): add bass and alto clef fixtures

Purpose:
Generate the smallest deterministic public PDF fixtures containing bass and alto clefs so Req-125 multi-clef classification can be implemented against real fixture evidence.

Requirement:
Req-126

Evidence basis:
- `projects/score2gp/reports/2026-07-09-req-125-missing-fixtures-blocker.md`
- `projects/score2gp/ACTIVE_TASK.md`

Acceptance:
- at least one public bass clef PDF fixture is committed
- at least one public alto clef PDF fixture is committed
- existing diagnostics can open/read the fixtures without crashing
- fixture manifests or focused tests prove the fixtures are intentional public test inputs
- no semantic classifier logic, ScoreIR output, GP writer behavior, pitch inference, or rhythm inference is changed

Outcome:
- product PR merged

---

## Task 65 — Review Req-126 bass and alto clef fixture implementation

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/req-126-review-v0.1

PR title:
docs(review): approve Req-126 bass and alto clef fixtures

Purpose:
Review the Developer's bass and alto clef fixture implementation, confirm it safely resolves the Req-125 blocker, and promote Req-125 again if deterministic fixture evidence is now available.

Requirement:
Req-126

Evidence basis:
- `projects/score2gp/reviews/2026-07-09-req-126-bass-alto-clef-fixture-review.md`

Outcome:
- governance PR merged

---

## Task 66 — Whole and half rest semantic candidate extraction

Status: DONE

Owning repo: score2gp

Branch:
feature/req-128-whole-half-rest-semantic-candidates-v0.1

PR title:
feat(pdf): add whole and half rest semantic candidates

Purpose:
Implement diagnostic-only whole rest and half rest semantic candidate extraction so rest coverage expands beyond quarter rests without changing ScoreIR, GP export, pitch inference, rhythm timelines, or voice assignment.

Requirement:
Req-128

Evidence basis:
- `projects/score2gp/reports/2026-07-09-post-semantic-candidate-strategy-and-backlog-architecture.md`
- `projects/score2gp/reviews/2026-07-09-req-125-multi-clef-candidate-review.md`
- `projects/score2gp/ACTIVE_TASK.md`

Acceptance:
- whole rest and half rest candidates have explicit diagnostic semantic candidate representation
- public fixtures or generated public fixtures prove both candidate types are detected
- quarter-rest extraction remains fail-closed for whole/half rests
- semantic candidate snapshots include the new diagnostic fields
- CLI/reporting surfaces the candidates consistently where semantic candidates are already exposed
- no ScoreIR, GP writer, notation bridge, pitch, rhythm, or voice behavior changes
- no-ScoreIR leakage tests and artifact audit pass

Outcome:
- product PR merged

---

## Task 67 — Review Req-128 whole and half rest semantic candidate extraction

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/req-128-review-v0.1

PR title:
docs(review): approve Req-128 whole and half rest semantic candidates

Purpose:
Review the Developer's diagnostic-only whole and half rest candidate extraction, verify no ScoreIR/GP leakage, and promote the next credible continuation through the post-completion continuation protocol.

Requirement:
Req-128

Evidence basis:
- `projects/score2gp/reviews/2026-07-09-req-128-whole-half-rest-candidates-review.md`

Outcome:
- governance PR merged

---

## Task 68 — Define clef-aware pitch mapping schema

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/req-127-pitch-mapping-schema-v0.1

PR title:
docs(pitch): design clef-aware pitch mapping schema

Purpose:
Design the lookup tables and metadata schema for mapping staff positions to MIDI pitches based on the detected clef candidate (treble, bass, alto) as requested by Req-127.

Requirement:
Req-127

Evidence basis:
- `projects/score2gp/reports/2026-07-09-post-semantic-candidate-strategy-and-backlog-architecture.md`
- `projects/score2gp/reviews/2026-07-09-req-125-multi-clef-candidate-review.md`

Acceptance:
- Pitch translation lookup document completed and approved.
- Details the mapping formulas and lookup tables for Treble, Bass, and Alto clefs.

Outcome:
- governance PR merged

---

## Task 69 — Review Req-127 clef-aware pitch mapping schema

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/req-127-review-v0.1

PR title:
docs(review): approve Req-127 pitch mapping schema

Purpose:
Review the designed pitch mapping tables and lookup document for Treble, Bass, and Alto clefs.

Requirement:
Req-127

Evidence basis:
- `projects/score2gp/reviews/2026-07-09-req-127-pitch-mapping-review.md`

Outcome:
- governance PR merged

---

## Task 70 — Implement clef-aware pitch mapping

Status: DONE

Owning repo: score2gp

Branch:
feature/req-127-pitch-mapping-v0.1

PR title:
feat(pdf): implement clef-aware pitch mapping

Purpose:
Implement the Developer phase of Req-127 by translating notehead staff positions to MIDI pitches using the active clef candidate.

Requirement:
Req-127

Evidence basis:
- `projects/score2gp/reports/2026-07-09-req-127-pitch-mapping-schema.md`
- `projects/score2gp/reviews/2026-07-09-req-127-pitch-mapping-review.md`
- `projects/score2gp/ACTIVE_TASK.md`

Acceptance:
- Pitch mapping translation logic is implemented in product code.
- Covered by unit tests for Treble, Bass, and Alto clefs, and ledger lines.
- No ScoreIR/GP writer changes.

Outcome:
- product PR merged

---

## Task 71 — Review Req-127 clef-aware pitch mapping implementation

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/req-127-implementation-review-v0.1

PR title:
docs(review): approve Req-127 pitch mapping implementation

Purpose:
Review the Developer's pitch mapping implementation and unit test coverage.

Requirement:
Req-127

Evidence basis:
- `projects/score2gp/reviews/2026-07-09-req-127-pitch-mapping-implementation-review.md`

Outcome:
- governance PR merged

---

## Task 72 — Apply clef-aware pitch mapping to read-only note diagnostics

Status: DONE

Owning repo: score2gp

Branch:
feature/req-129-read-only-clef-aware-pitch-diagnostics-v0.1

PR title:
feat(pdf): apply clef-aware pitch mapping to read-only diagnostics

Purpose:
Wire the approved clef-aware pitch mapping helper into read-only note-candidate diagnostics so treble, bass, and alto clef evidence can enrich note candidates without changing ScoreIR, GP export, rhythm timelines, or voice assignment.

Requirement:
Req-129

Evidence basis:
- `projects/score2gp/reports/2026-07-09-req-127-pitch-mapping-schema.md`
- `projects/score2gp/reviews/2026-07-09-req-127-pitch-mapping-implementation-review.md`
- `projects/score2gp/ACTIVE_TASK.md`

Acceptance:
- read-only note candidates can be enriched using `map_staff_step_to_midi_pitch`
- treble, bass, and alto clef evidence are each covered by tests
- diagnostic output includes stable pitch evidence, preferably both MIDI pitch and note name if existing output contracts allow it
- unknown, missing, or ambiguous clef evidence fails closed without pitch enrichment
- ledger-line support remains bounded by existing staff-position/ledger validation rules
- no ScoreIR, GP writer, MusicXML oracle, rhythm, timeline, or voice behavior changes
- no-ScoreIR leakage tests and artifact audit pass

Outcome:
- product PR merged

---

## Task 73 — Review Req-129 read-only clef-aware pitch diagnostics

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/req-129-review-v0.1

PR title:
docs(review): approve Req-129 read-only pitch diagnostics

Purpose:
Review the Developer's read-only clef-aware pitch diagnostic integration, verify strict non-leakage to ScoreIR/GP output, and promote the next credible continuation through the required continuation audit.

Requirement:
Req-129

Evidence basis:
- `projects/score2gp/reviews/2026-07-09-req-129-read-only-pitch-diagnostics-review.md`

Outcome:
- governance PR merged

---

## Task 74 — Design accidental and key signature pitch mapping schema

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/req-130-accidental-schema-v0.1

PR title:
docs(pitch): design accidental and key signature schema

Purpose:
Design the lookup tables, metadata schema, and modifier rules for modifying base MIDI pitches based on accidental candidates (sharps, flats, naturals) and key signatures under Req-130.

Requirement:
Req-130

Evidence basis:
- `projects/score2gp/reviews/2026-07-09-req-129-read-only-pitch-diagnostics-review.md`

Acceptance:
- Accidental and key signature schema document completed and approved.
- Details the modifiers for natural notes, accidental lookup tables, and key signatures.

Outcome:
- governance PR merged

---

## Task 75 — Review accidental and key signature pitch mapping schema

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/req-130-review-v0.1

PR title:
docs(review): approve accidental and key signature schema design

Purpose:
Review the accidental and key signature pitch modifier schema design.

Requirement:
Req-130

Evidence basis:
- `projects/score2gp/reviews/2026-07-09-req-130-accidental-review.md`

Outcome:
- governance PR merged

---

## Task 76 — Implement accidental and key signature pitch mapping

Status: DONE

Owning repo: score2gp

Branch:
feature/req-130-accidental-mapping-v0.1

PR title:
feat(pdf): implement accidental and key signature pitch mapping

Purpose:
Implement the modifier calculation and local/key signature mapping engine inside `score2gp`, enriching read-only notes with modified MIDI pitches and names, covered by unit tests.

Clarification:
If visual accidental or key-signature candidate extraction is not already available, implement the pure modifier engine and bounded read-only diagnostic integration against structured inputs/mocks. Do not stop merely because visual accidental detection is a future dependency.

Requirement:
Req-130

Evidence basis:
- `projects/score2gp/reports/2026-07-09-req-130-accidental-schema.md`
- `projects/score2gp/reviews/2026-07-09-req-130-accidental-review.md`
- `projects/score2gp/ACTIVE_TASK.md`

Acceptance:
- Modifier calculation logic is implemented.
- Correctly handles local accidentals (measure-local scopes and barline resets) and key signatures.
- Covered by unit tests for sharps, flats, and naturals.
- If visual accidental/key-signature candidates are not available, structured-input tests prove the modifier engine and the implementation report records the deferred visual-detection dependency.
- No ScoreIR, GP writer, MusicXML oracle, rhythm, timeline, or voice behavior changes.
- `make verify` passes.

Outcome:
- product PR merged

---

## Task 77 — Review accidental and key signature pitch mapping implementation

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/req-130-implementation-review-v0.1

PR title:
docs(review): approve accidental and key signature pitch mapping implementation

Purpose:
Review the implementation of accidental and key signature modifier logic and unit test coverage.

Requirement:
Req-130

Evidence basis:
- `projects/score2gp/reviews/2026-07-09-req-130-accidental-implementation-review.md`

Outcome:
- governance PR merged

---

## Task 78 — Design rest mapping and rhythm timeline reconstruction schema

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/req-131-rest-timeline-schema-v0.1

PR title:
docs(rhythm): design rest mapping and rhythm timeline schema

Purpose:
Design the schema, voice alignment cursor rules, and duration reconstruction formulas for injecting quarter, half, and whole rests into ScoreIR and GP7 packages under Req-131.

Requirement:
Req-131

Evidence basis:
- `projects/score2gp/reviews/2026-07-09-req-130-accidental-implementation-review.md`

Acceptance:
- Rest mapping and rhythm timeline schema document completed and approved.
- Details voice cursors, polyphonic alignments, and rest insertion rules.

Outcome:
- governance PR merged

---

## Task 79 — Review rest mapping and rhythm timeline reconstruction schema

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/req-131-review-v0.1

PR title:
docs(review): approve rest mapping and rhythm timeline schema design

Purpose:
Review the rest mapping and rhythm timeline schema design.

Requirement:
Req-131

Evidence basis:
- `projects/score2gp/reviews/2026-07-09-req-131-rhythm-review.md`

Outcome:
- governance PR merged

---

## Task 80 — Implement read-only rhythm timeline diagnostics

Status: DONE

Owning repo: score2gp

Branch:
feature/req-131-rhythm-diagnostics-v0.1

PR title:
feat(pdf): implement read-only rhythm timeline diagnostics

Purpose:
Implement the `build_staff_timeline_preview` helper in `whole_note_recogniser.py`, reconstructing the measure-local tick timelines and rest assignments as read-only diagnostic metadata, covered by unit and integration tests.

Requirement:
Req-131

Evidence basis:
- `projects/score2gp/reports/2026-07-09-req-131-rest-timeline-schema.md`
- `projects/score2gp/reviews/2026-07-09-req-131-rhythm-review.md`
- `projects/score2gp/ACTIVE_TASK.md`

Acceptance:
- Timeline preview logic is implemented.
- Assigns quarter, half, and whole rests to voice cursors based on vertical/middle line position.
- Clusters notes into time slices within tick duration limits.
- Barlines reset voice cursors to 0.
- All timeline info is output strictly under `"timeline_preview"` and is read-only.
- No ScoreIR, GP writer/package, or downstream conversion changes.
- `make verify` passes.

Outcome:
- product PR merged

---

## Task 81 — Review read-only rhythm timeline diagnostics

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/req-131-implementation-review-v0.1

PR title:
docs(review): approve read-only rhythm timeline diagnostics implementation

Purpose:
Review the implementation of read-only rhythm timeline diagnostics.

Requirement:
Req-131

Evidence basis:
- `projects/score2gp/reviews/2026-07-09-req-131-implementation-review.md`

Outcome:
- governance PR merged

---

## Task 82 — Design consolidated diagnostics schema and CLI reporting format

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/req-132-consolidated-diagnostics-schema-v0.1

PR title:
docs(diagnostics): design consolidated diagnostics and CLI reporting schema

Purpose:
Design the JSON schema, CLI display parameters, and output formats for consolidating semantic candidates, pitch mapping, and timeline previews into a single diagnostic report under Req-132.

Requirement:
Req-132

Evidence basis:
- `projects/score2gp/reviews/2026-07-09-req-131-implementation-review.md`

Acceptance:
- Consolidated diagnostics schema document completed and approved.
- Defines fields, CLI table formatting, and validation constraints.

Outcome:
- governance PR merged

---

## Task 83 — Review consolidated diagnostics schema and CLI reporting format

Status: DONE

Owning repo: score2gp-agentops

Branch:
governance/req-132-review-v0.1

PR title:
docs(review): approve consolidated diagnostics and CLI reporting schema design

Purpose:
Review the consolidated diagnostics and CLI reporting schema design.

Requirement:
Req-132

Evidence basis:
- `projects/score2gp/reviews/2026-07-09-req-132-diagnostics-review.md`

Outcome:
- governance PR merged

---

## Task 84 — Implement consolidated diagnostics and CLI reporting format

Status: ACTIVE

Owning repo: score2gp

Branch:
feature/req-132-diagnostics-implementation-v0.1

PR title:
feat(pdf): implement consolidated diagnostics and CLI reporting format

Purpose:
Implement the formatted console print table and consolidated JSON reports inside the diagnostics CLI commands in `cli.py` under Req-132.

Requirement:
Req-132

Evidence basis:
- `projects/score2gp/reports/2026-07-09-req-132-consolidated-diagnostics-schema.md`
- `projects/score2gp/reviews/2026-07-09-req-132-diagnostics-review.md`
- `projects/score2gp/ACTIVE_TASK.md`

Acceptance:
- note-candidate diagnostics CLI commands correctly return the consolidated JSON format when `--json` is enabled.
- note-candidate diagnostics CLI commands output a clean, formatted text table summary showing staves, pitches, and timeline measures when `--json` is false.
- Covered by CLI integration tests.
- No changes to ScoreIR, GP writer/package, or downstream conversion behavior.
- `make verify` passes.

Outcome:
- product PR pending

---

## Task 85 — Review consolidated diagnostics and CLI reporting implementation

Status: APPROVED

Owning repo: score2gp-agentops

Branch:
governance/req-132-implementation-review-v0.1

PR title:
docs(review): approve consolidated diagnostics and CLI reporting implementation

Purpose:
Review the implementation of consolidated diagnostics and CLI reporting format.

Requirement:
Req-132

Evidence basis:
- `projects/score2gp/reviews/2026-07-09-req-132-implementation-review.md`

Outcome:
- governance PR pending

---

## Task 87 — Teamwork corpus conversion accuracy programme

Status: ACTIVE

Owning repos: score2gp-agentops and score2gp

Programme contract:
`projects/score2gp/programmes/2026-07-16-teamwork-corpus-conversion-accuracy.md`

Purpose:
Deliver measured, visibly correct improvement to deterministic conversion for
the approved guitar-PDF corpus, starting from Lesson-3 and Lesson-4 but
rejecting fixture-specific overfitting. This supersedes the pending Req-132
diagnostic workflow as the active delivery vehicle; its diagnostics remain
usable evidence.

Authorised capabilities:
- deterministic recognition and conversion changes needed by the programme;
- no-reference MusicXML/ScoreIR/GPIF generation;
- duration, rests, dots, ties, barlines, system breaks, key/time/tempo,
  guitar-position inference, and bounded embellishment work when selected by
  the programme decision gates;
- guarded autonomous merge of qualifying PRs as defined in `AGENT_CONTROL.md`.

Acceptance:
- a reusable bar-level output comparator exists and is used as the primary
  acceptance instrument;
- Lesson-3 and Lesson-4 have fresh no-reference conversions with a durable,
  truthful mismatch ledger;
- each claimed repair is proven at bar level and checked against a distinct
  corpus input;
- no reference-GP data affects generation;
- each milestone produces a reviewable PR and no private artifacts enter Git;
- the final report distinguishes fixed, improved, deferred, and still-failing
  corpus capabilities.

Stop/pivot condition:
- a capability may be deferred only after its evidence and a smallest credible
  pivot have been recorded. Green aggregate metrics or file creation are not
  completion evidence.
