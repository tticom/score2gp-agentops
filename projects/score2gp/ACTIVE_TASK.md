# Active Task

**Task**: Req-126 / Task 64: Generate public bass and alto clef fixtures
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## Status
APPROVED

## Task Authorised
Yes

## Completion Evidence
Developer must create the smallest deterministic public PDF fixtures needed to unblock Req-125 multi-clef classification, commit them with focused tests or manifest updates, push the branch, and open a product PR.

## 1. Baseline
- Req-125 / Task 62 is blocked because the available public and approved private fixture corpus contains no bass or alto clef PDF evidence.
- The blocker is recorded in `projects/score2gp/reports/2026-07-09-req-125-missing-fixtures-blocker.md`.
- Without real generated PDF primitives for bass and alto clefs, any multi-clef classifier would be untestable or would rely on invented mock success.

## 2. Context
This is a blocker pivot task. The correct project action is not to stop; it is to create the smallest approved fixture evidence that makes Req-125 testable.

## 3. Goal
Generate deterministic public fixtures containing:

- at least one standard 5-line notation staff with a bass clef;
- at least one standard 5-line notation staff with an alto clef.

The fixtures should be minimal and designed for candidate extraction evidence, not musical completeness.

## 4. Non-goals
- Do not implement bass or alto clef classification.
- Do not infer pitch, duration, rhythm, voice, or timeline.
- Do not map clefs into ScoreIR or GP output.
- Do not add private fixture expectations.
- Do not broaden into full multi-staff OMR support.

## 5. Product Scope
Allowed likely files:

- `tests/fixtures/pdf/` fixture generation helpers and generated PDFs
- fixture manifest files, if present
- focused tests that prove the new fixtures exist and are readable by existing diagnostics

Stop before changing:

- semantic classifier logic
- ScoreIR generation
- GP writer output
- private fixture repositories
- governance files outside the follow-up review/promotion step

## 6. Suggested Product Work Branch
`test/req-126-bass-alto-clef-fixtures-v0.1`

## 7. Required Validation

Run at minimum:

```bash
cd /home/tticom/work/score2gp-workspace/score2gp
git diff --check
.venv/bin/python -m pytest -q tests/test_pdf_fixture_manifest_smoke.py tests/test_pdf_standard_staff_fixture_manifest.py tests/test_pdf_standard_staff_diagnostics_fixtures.py
.venv/bin/python scripts/artifact_audit.py
```

Run `make verify` if practical.

## 8. Acceptance Criteria
- New public bass and alto clef PDF fixtures are committed in the product repo.
- Existing diagnostics can open/read the fixtures without crashing.
- Tests or manifest entries prove the fixtures are tracked and intentionally public.
- The task does not implement classifier logic.
- Artifact audit passes.

## 9. Next Steps
- After this product PR is merged and reviewed, promote Req-125 / Task 62 again so the multi-clef classifier has deterministic fixture evidence.
