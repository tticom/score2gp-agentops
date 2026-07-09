# Active Task

**Task**: Req-128 / Task 66: Whole and half rest semantic candidate extraction
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## Status
APPROVED

## Task Authorised
Yes

## Completion Evidence
Developer must implement diagnostic-only whole rest and half rest candidate extraction, commit focused tests and snapshots, push the branch, and open a product PR. After the product PR is merged, the Reviewer must complete Task 67 and promote the next credible continuation instead of resetting to `NO_ACTIVE_TASK_APPROVED`.

## 1. Baseline
- Req-125 multi-clef candidate classification is complete.
- Existing tests already prove whole and half rest shapes fail closed as quarter rests.
- The post-semantic strategy identified whole/half rest candidate extraction as the next safe semantic coverage expansion before pitch mapping, rhythm timelines, voice assignment, or ScoreIR integration.
- Diagnostic semantic candidates must remain isolated from playable output.

## 2. Context
This is a post-completion continuation task. The correct project action is not to stop after Req-125; it is to keep expanding bounded diagnostic candidate coverage where the evidence already exists and the scope remains fail-closed.

Req-126 was used as a blocker-pivot fixture task for bass/alto clefs. This task therefore uses Req-128 for the originally planned whole/half rest coverage expansion to avoid requirement-id collision.

## 3. Goal
Add diagnostic-only semantic candidates for:

- whole rests;
- half rests.

The candidates should be derived from existing geometry primitives and existing public fixtures where possible. They must be observable in semantic candidate outputs and snapshots, but must not alter ScoreIR, Guitar Pro export, rhythm timelines, or playable conversion behavior.

## 4. Non-goals
- Do not infer duration timelines.
- Do not inject rests into ScoreIR.
- Do not alter GP writer output.
- Do not implement voice assignment or polyphonic rest resolution.
- Do not infer pitch.
- Do not broaden into eighth/sixteenth rest recognition unless required only as a fail-closed negative test.
- Do not relax existing quarter-rest fail-closed behavior.

## 5. Product Scope
Allowed likely files:

- `src/score2gp/pdf_candidate_semantic_gate.py`
- new or existing `src/score2gp/pdf_candidate_*rest*.py` modules
- `src/score2gp/pdf.py` and CLI/reporting paths only if required to expose diagnostic candidates consistently
- `tests/test_pdf_candidate_quarter_rest.py`
- `tests/test_pdf_candidate_semantic_gate.py`
- `tests/test_pdf_semantic_candidate_snapshots.py`
- `tests/test_semantic_cli_reporting.py`
- `tests/test_no_scoreir_leakage_gate.py`
- semantic candidate snapshot fixtures under `fixtures/public/`
- generated public PDF fixture specs/PDFs only if existing fixtures are insufficient

Stop before changing:

- ScoreIR event generation
- GP writer output
- notation bridge sequencing
- pitch mapping or clef-aware note conversion
- rhythm timeline inference
- private fixture repositories

## 6. Suggested Product Work Branch
`feature/req-128-whole-half-rest-semantic-candidates-v0.1`

## 7. Required Validation

Run at minimum:

```bash
cd /home/tticom/work/score2gp-workspace/score2gp
git diff --check
.venv/bin/python -m pytest -q tests/test_pdf_candidate_quarter_rest.py tests/test_pdf_candidate_semantic_gate.py tests/test_pdf_semantic_candidate_snapshots.py tests/test_semantic_cli_reporting.py tests/test_no_scoreir_leakage_gate.py tests/test_semantic_model_hardening.py
.venv/bin/python scripts/artifact_audit.py
```

Run `make verify` if practical before merging.

## 8. Acceptance Criteria
- Whole rest and half rest candidates are represented by explicit diagnostic semantic candidate models or fields.
- Existing public fixtures or newly generated public fixtures prove both candidate types are detected.
- Quarter-rest extraction remains fail-closed and does not misclassify whole/half rests as quarter rests.
- Semantic candidate snapshots include the new diagnostic candidate fields.
- CLI/reporting surfaces the new diagnostic candidates consistently if the existing semantic candidate output path supports rest candidates.
- No ScoreIR, GP writer, notation bridge, pitch, rhythm, or voice behavior changes.
- No-ScoreIR leakage tests pass.
- Artifact audit passes.

## 9. Next Steps
- After this product PR is merged and reviewed, perform the post-completion continuation audit.
- Likely next candidates are a review of Req-128, then either eighth/sixteenth rest fail-closed candidate research or clef-aware pitch mapping schema research, depending on what the Req-128 implementation reveals.
