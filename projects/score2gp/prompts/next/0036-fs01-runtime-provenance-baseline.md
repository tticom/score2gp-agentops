# 0036 - FS-01 Runtime Provenance Baseline and Corpus Stabilisation Harness

## Objective

Implement bounded Developer task `FS-01` in `tticom/score2gp`, as authorized by the approved queue in `APPROVED_TASK_QUEUE.md` and programme contract `projects/score2gp/prompts/2026-07-19-teamwork-runtime-provenance-functional-stabilisation.md`.

Add commandable, private-safe runtime provenance recording for corpus conversion runs. Record product git SHA, working tree clean/dirty status, resolved executable and import paths, exact command invocation, input classification, sidecar path/hash/provenance, output/report paths, exit status, refusal codes, and sanitized structural counts.

## Authorized Product Files

- `src/score2gp/runtime_provenance.py`
- `scripts/private_e2e_smoke.py`
- `scripts/private_diagnostic_smoke.py`
- `tests/test_runtime_provenance.py`

No other product files in `src/` or `tests/` may be edited in this task.

## Start

1. Work only in the canonical Ubuntu WSL repositories below `/home/tticom-automation/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `projects/score2gp/AGENT_CONTROL.md`, `projects/score2gp/ACTIVE_TASK.md`, `projects/score2gp/prompts/next/0036-fs01-runtime-provenance-baseline.md`, `APPROVED_TASK_QUEUE.md`, and product repository `AGENTS.md`.
4. Require clean governance and product worktrees.
5. Create product branch `agy/fs01-runtime-provenance-baseline` in `tticom/score2gp`.
6. Run `python scripts/agent_verify.py` in `score2gp` before making code modifications.

## Implementation Scope & Seam Contract

1. **`src/score2gp/runtime_provenance.py`**:
   - Implement `RuntimeProvenanceRecord` model and helper functions to capture execution environment metadata, git commit SHA, dirty status, and sanitized conversion telemetry without leaking private corpus file contents or paths.

2. **`scripts/private_e2e_smoke.py` & `scripts/private_diagnostic_smoke.py`**:
   - Integrate `RuntimeProvenanceRecord` into corpus smoke test scripts to record durable provenance sidecars alongside test runs.

3. **`tests/test_runtime_provenance.py`**:
   - Add public unit and integration tests asserting schema validation, committed vs `uncontrolled_runtime` classification, and sanitized provenance serialization.

## Validation Commands

1. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python -m pytest tests/test_runtime_provenance.py`
2. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python scripts/agent_verify.py`

## Non-goals

- Do not alter core OMR conversion logic or score building behavior.
- Do not check private corpus fixtures or private output files into Git.
