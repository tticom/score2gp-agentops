# 0029 - MXS-10 Formalize Assisted Sidecar Ingestion & Provenance Manifest Contract

## Objective

Implement Developer slice `MXS-10` on the sidecar ingestion pipeline in `tticom/score2gp`, as authorized by the merged Architecture Decision Record `projects/score2gp/reviews/2026-08-03-mxs09-architecture-decision-record.md`.

Extend `score2gp convert` to support `--sidecar-manifest <path>`, validating sidecar SHA-256 hashes against `SidecarEvaluationResult`, requiring `eval_status == "passed"`, and embedding sidecar provenance into generated HTML conversion reports.

## Authorized Product Files

- `src/score2gp/cli.py`
- `src/score2gp/sidecar_evaluator.py`
- `src/score2gp/report.py`
- `tests/test_mxs10_sidecar_ingestion_manifest.py`

No other product files in `src/` or `tests/` may be edited in this task.

## Start Protocol

1. Work only in the canonical Ubuntu WSL repositories below `/home/tticom-automation/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `projects/score2gp/AGENT_CONTROL.md`, `projects/score2gp/ACTIVE_TASK.md`, `projects/score2gp/prompts/next/0029-mxs10-assisted-sidecar-ingestion-manifest.md`, and product repository `AGENTS.md`.
4. Require clean governance and product worktrees.
5. Create product branch `agy/mxs10-assisted-sidecar-ingestion-manifest` in `tticom/score2gp`.
6. Run `.venv/bin/python scripts/agent_verify.py` in `score2gp` before making code modifications.

## Implementation Scope & Contract

1. **`src/score2gp/sidecar_evaluator.py`**:
   - Add `SidecarProvenanceManifest` Pydantic model containing:
     - `generator_tool: Literal["pdftomusic_pro", "photoscore_ultimate", "scanscore", "musescore_manual", "other"]`
     - `generator_version: str`
     - `operator_id: str`
     - `operator_labor_minutes: float`
     - `sidecar_sha256: str`
     - `pdf_sha256: str | None`
     - `eval_status: str`
   - Add `validate_sidecar_manifest(manifest_path: Path, sidecar_path: Path) -> SidecarProvenanceManifest` helper. Fail closed if `sidecar_sha256` mismatch occurs or `eval_status != "passed"`.

2. **`src/score2gp/cli.py`**:
   - Add optional `--sidecar-manifest <path>` flag to `score2gp convert`.

3. **`src/score2gp/report.py`**:
   - Update HTML report generation to render Sidecar Provenance Manifest metadata section when present.

4. **`tests/test_mxs10_sidecar_ingestion_manifest.py`**:
   - Add unit tests covering:
     - Manifest validation success with `generated_tiny_tab.musicxml`.
     - Rejection of manifests with mismatched `sidecar_sha256`.
     - Rejection of manifests with `eval_status != "passed"`.
     - CLI `--sidecar-manifest` conversion execution.

## Validation Commands

1. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python -m pytest tests/test_mxs10_sidecar_ingestion_manifest.py`
2. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python scripts/agent_verify.py`

## Non-goals

- No change to default PDF-only processing when no `--musicxml` sidecar is specified.
- No third-party network API calls or unapproved dependency additions.
