# Post-PR #227 Candidate Boundary Task List

Date: 2026-06-09

Product baseline:
- Product PR #227 (`feat(pdf): expose primitive-level geometry diagnostics`) was merged on 2026-06-09.
- Product PR #227 head SHA: `3276e27a6cd0877fdbdb0eaa3d8a5a0af67b6f02`.
- Product PR #227 merge commit: `44508b260fd9e7677faed8654a40ecdb4a1c94ef`.
- Task 36 is complete: primitive-level geometry evidence is now available in diagnostics.

Purpose:
Create the next safe work sequence after primitive-level geometry diagnostics. Do not jump straight into extraction. The next work must define the candidate boundary and model contracts first, using the new evidence arrays as source data.

Governance override:
- Older candidate-extraction queue items that predate PR #227 must not be promoted as-is.
- Any candidate task that relies on aggregate counts, placeholder coordinates, inferred positions, or fake geometry is superseded by this task list.
- Extraction work remains blocked until the candidate-boundary/model redesign task is reviewed and merged.

Hard constraints for all tasks in this list:
- No pitch, duration, clef, key signature, time signature, beat, rhythm, voice, chord, notehead, stem, or ScoreIR work.
- No extraction from aggregate counts.
- No synthesized plausible-looking coordinates.
- No private PDFs, GP files, logs, screenshots, or private outputs committed.
- Use only real serialized primitive evidence arrays from diagnostics as candidate inputs.
- Preserve `x0/y0/x1/y1`, `kind`, optional safe font metadata, staff identity, and source grouping provenance.
- Stop if required evidence is missing; create a prerequisite diagnostics task instead.

---

## Task 37 — Define geometry candidate boundary from primitive evidence

Status: ACTIVE

Owning repo: score2gp

Branch:
`docs/primitive-evidence-candidate-boundary-v0.1`

PR title:
`docs(pdf): define candidate boundary from primitive evidence`

Context:
PR #227 exposes real primitive-level evidence arrays in staff diagnostics. Candidate extraction must not proceed until the product repo defines a clean, geometry-only candidate boundary based on those arrays.

Goal:
Add a product architecture note that defines the candidate boundary, allowed model concepts, input evidence, non-goals, stop conditions, and fixture proof required before any extractor implementation.

Likely product files:
- `docs/testing/primitive-evidence-candidate-boundary.md`
- optionally update `docs/testing/staff-geometry-diagnostics.md` only if it already exists and is the right home

Required pre-flight checks:
```bash
cd /home/tticom/work/score2gp-workspace/score2gp
git fetch --all --prune
git switch main
git pull --ff-only human main
git status --short
git log --oneline --decorate --max-count=10
gh pr view 227
```

Implementation guidance:
The document must define candidate inputs from:
- `StaffLeftMarginAggregateDiagnostics.evidence`
- `XAlignedClusterAggregateDiagnostics.evidence`
- `PrimitiveGeometryEvidence`
- `XAlignedPrimitiveClusterEvidence`

The document must define only geometry/visual concepts. Suggested allowed names:
- `PrimitiveEvidenceCandidate`
- `LeftMarginPrimitiveCandidate`
- `XAlignedPrimitiveClusterCandidate`
- `TextSpanPrimitiveCandidate`
- `CurvePrimitiveCandidate`
- `VerticalStrokePrimitiveCandidate`
- `HorizontalStrokePrimitiveCandidate`
- `DiagonalStrokePrimitiveCandidate`
- `RectanglePrimitiveCandidate`

The document must explicitly reject older names that imply music semantics or pre-PR #227 aggregate inference.

Validation:
```bash
git diff --check
grep -R -i -E "notehead|stem|clef|pitch|duration|voice|chord|key_signature|time_signature|beat|rhythm|ScoreIR" docs/testing/primitive-evidence-candidate-boundary.md || true
git status --short
```

Acceptance criteria:
- Document exists in product repo.
- It names PR #227 evidence arrays as the required source of truth.
- It forbids aggregate-derived, placeholder, and synthetic candidate coordinates.
- It defines model/input/output boundaries before implementation.
- It includes stop conditions for missing evidence.
- It does not approve extraction implementation.

Stop conditions:
- PR #227 is not present on product `main`.
- Evidence arrays are missing from schema or public fixtures.
- The design requires semantic names or musical inference.
- The document would need private PDF examples.

Reporting format:
- Branch name
- PR link
- Files changed
- Commands run
- Validation result
- Known limitations
- Next recommended task

---

## Task 38 — Add primitive-evidence candidate model contracts

Status: APPROVED only after Task 37 is human-merged

Owning repo: score2gp

Branch:
`feature/primitive-evidence-candidate-models-v0.1`

PR title:
`feat(pdf): add primitive-evidence candidate models`

Goal:
Add frozen, geometry-only Pydantic models for candidate contracts. Do not implement extraction rules.

Likely product files:
- `src/score2gp/pdf_geometry_candidates.py`
- `tests/test_pdf_geometry_candidates.py`

Required model properties:
- source staff identity: `page_index`, `system_index`, `staff_index`
- source evidence bounds: `x0`, `y0`, `x1`, `y1`
- non-semantic kind copied from evidence
- provenance indicating left-margin evidence or x-aligned cluster evidence
- optional safe font metadata for text spans only

Non-goals:
- no extractor function
- no integration into `inspect_pdf`
- no ScoreIR
- no musical semantics

Validation:
```bash
git diff --check
.venv/bin/python -m pytest tests/test_pdf_geometry_candidates.py
.venv/bin/python -m pytest tests/test_pdf_staff_geometry_schema_contract.py
```

Acceptance criteria:
- Models are frozen and validate ordered bounds.
- Tests reject semantic names in model fields/schema.
- Candidate models can be constructed from real-style primitive evidence objects.
- No parser or diagnostics output changes.

Stop conditions:
- Task 37 is not merged.
- Model design requires semantic names.
- Model design requires fields not available in PR #227 evidence arrays.

---

## Task 39 — Add candidate anti-semantic schema gate

Status: APPROVED only after Task 38 is human-merged

Owning repo: score2gp

Branch:
`test/primitive-evidence-candidate-anti-semantic-gate-v0.1`

PR title:
`test(pdf): guard primitive-evidence candidates against semantic leakage`

Goal:
Add a hard test gate that scans candidate model public names, fields, schema, docs snippets, and snapshots for forbidden semantic terminology.

Likely product files:
- `tests/test_pdf_geometry_candidates.py`
- optional `tests/test_pdf_candidate_semantic_gate.py`

Forbidden terms:
- `notehead`
- `stem`
- `clef`
- `pitch`
- `duration`
- `voice`
- `chord`
- `key_signature`
- `time_signature`
- `beat`
- `rhythm`
- `ScoreIR`

Validation:
```bash
git diff --check
.venv/bin/python -m pytest tests/test_pdf_geometry_candidates.py
```

Acceptance criteria:
- Test fails if semantic terms appear in candidate model schema or public field names.
- Allowed geometry terms remain usable.
- No product behaviour changes.

---

## Task 40 — Add candidate extraction design review

Status: APPROVED only after Task 39 is human-merged

Owning repo: score2gp-agentops

Branch:
`review/primitive-evidence-candidate-extraction-design-v0.1`

PR title:
`docs(review): review primitive-evidence candidate extraction design`

Goal:
Perform a hard governance review before any extraction implementation. Decide whether the candidate model boundary is ready for a minimal extractor skeleton.

Allowed governance files:
- `projects/score2gp/reviews/2026-06-09-primitive-evidence-candidate-extraction-design.md`
- `projects/score2gp/ACTIVE_TASK.md`
- `projects/score2gp/tasks/2026-06-09-post-227-candidate-boundary-task-list.md`

Product repo access:
Read-only.

Required evidence:
- product main SHA
- Task 37 PR link and merge commit
- Task 38 PR link and merge commit
- Task 39 PR link and merge commit
- files inspected
- tests run
- schema status
- anti-semantic gate result
- privacy/artifact check

Verdict options:
- ready for extractor skeleton
- needs model hardening
- needs diagnostics prerequisite
- cannot verify

Non-goals:
- do not implement extraction
- do not modify product code
- do not add semantic tasks

---

## Task 41 — Add primitive-evidence extractor skeleton

Status: APPROVED only after Task 40 verdict is `ready for extractor skeleton`

Owning repo: score2gp

Branch:
`feature/primitive-evidence-extractor-skeleton-v0.1`

PR title:
`feat(pdf): add primitive-evidence extractor skeleton`

Goal:
Add a pure extractor skeleton that accepts `NotationStaffDiagnostics` and returns an empty or pass-through typed candidate set. It must not implement classification rules yet.

Likely product files:
- `src/score2gp/pdf_geometry_candidate_extraction.py`
- `src/score2gp/pdf_geometry_candidates.py`
- `tests/test_pdf_geometry_candidate_extraction.py`

Non-goals:
- no left-margin extraction rules
- no x-aligned extraction rules
- no candidate reporting integration
- no ScoreIR
- no musical semantics

Validation:
```bash
git diff --check
.venv/bin/python -m pytest tests/test_pdf_geometry_candidate_extraction.py
.venv/bin/python -m pytest tests/test_pdf_geometry_candidates.py
```

Acceptance criteria:
- Pure function exists.
- Typed empty/pass-through return model exists.
- Tests prove no semantic leakage.
- Existing diagnostics behaviour is unchanged.

---

## Task 42 — Extract left-margin primitive evidence candidates

Status: BLOCKED until Task 41 is human-merged and reviewed

Owning repo: score2gp

Branch:
`feature/left-margin-primitive-evidence-candidates-v0.1`

PR title:
`feat(pdf): extract left-margin primitive evidence candidates`

Goal:
Extract geometry-only candidates directly from `StaffLeftMarginAggregateDiagnostics.evidence`.

Hard requirement:
Each candidate must carry exact source evidence bounds. No candidate may be created from aggregate counts.

Non-goals:
- no clef/key/time interpretation
- no marker meaning inference
- no ScoreIR

Stop conditions:
- evidence is absent, incomplete, or only aggregate counts are available
- candidate requires invented coordinates
- candidate would need semantic naming

---

## Task 43 — Extract x-aligned primitive cluster evidence candidates

Status: BLOCKED until Task 41 is human-merged and reviewed

Owning repo: score2gp

Branch:
`feature/x-aligned-primitive-evidence-candidates-v0.1`

PR title:
`feat(pdf): extract x-aligned primitive evidence candidates`

Goal:
Extract geometry-only cluster candidates directly from `XAlignedClusterAggregateDiagnostics.evidence`.

Hard requirement:
Cluster candidates must preserve cluster `x0/x1`, `primitive_count`, and every source primitive evidence item.

Non-goals:
- no notehead/stem inference
- no chord inference
- no rhythm/duration inference
- no ScoreIR

Stop conditions:
- evidence/count reconciliation fails
- primitive evidence arrays are missing
- candidate would require musical semantics

---

## Still explicitly not approved

The following remain outside scope:
- semantic candidate extraction
- pitch inference
- duration inference
- clef inference
- key signature inference
- time signature inference
- voice assignment
- rhythm interpretation
- chord inference
- ScoreIR event generation from standard-staff glyphs
- scanned/OCR PDF handling
- real/private/copyrighted PDF fixtures
