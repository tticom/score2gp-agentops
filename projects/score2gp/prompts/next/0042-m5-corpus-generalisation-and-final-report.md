# 0042 - M5: Corpus Generalisation and Final Report

## Objective

Run the complete corpus conversion smoke matrix on the updated `score2gp` pipeline. Audit and cluster conversion outcomes and failures by capability (such as timing, duration/rests, layout, sidecar integration, or key/time signatures) rather than by file name. Produce a structured, durable final report detailing conversion status, quality metrics, and remaining blockers.

## Start

1. Work only in the canonical Ubuntu WSL repositories below `/home/tticom-automation/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `projects/score2gp/ACTIVE_TASK.md`, product repository `AGENTS.md`, and `projects/score2gp/programmes/2026-07-16-teamwork-corpus-conversion-accuracy.md`.
4. Require clean governance and product worktrees.
5. Create product branch `agy/m5-corpus-generalisation-and-report` in `tticom/score2gp`.
6. Run `python scripts/agent_verify.py` in `score2gp` before making modifications.

## Implementation Scope & Seam Contract

This is a governance and analysis task, not a product code implementation task. You are authorized to edit only documentation and report files in governance, and run diagnostic/conversion commands in the product repository.

1. **Run Corpus Conversion**: Convert the selected private/public corpus files using the current main branch pipeline, recording:
   - Output produced (successful `.gp` file or refusal).
   - Pipeline stage / refusal code.
   - Quality metrics for duration/rests/dots, barlines/layout, and techniques.
2. **Cluster Failures**: Group conversion failures and refusal categories by functional capability (e.g. key signature errors, timing overlaps, Pydantic constraints) rather than file by file.
3. **Final Report**: Write the comprehensive findings to `projects/score2gp/reports/2026-08-08-m5-corpus-generalisation-final-report.md` in the governance repository.

## Validation Commands

1. Run the corpus conversion script:
   ```bash
   PYTHONPATH=. .venv/bin/python3 scripts/corpus_harness.py --in-dir fixtures/public --out work/m5-report/
   ```
2. Verify all unit/integration tests pass on the product codebase:
   ```bash
   PYTHONPATH=. .venv/bin/python3 -m pytest
   ```
3. Run `python scripts/agent_verify.py` to confirm verification checks pass.

## Deliverables

1. Commit only governance report artifacts under `projects/score2gp/reports/`.
2. Update `ACTIVE_TASK.md` to set task status to `MERGED` once the report is finalized.
