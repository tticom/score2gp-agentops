# Active Task

**Task**: Task 92 — Real-Source Oracle Harness & Process Isolation (CRP-04)
**Status**: MERGED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/crp-04-real-source-oracle-harness`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0047-real-source-oracle-harness.md`

## Context

Task 91 (CRP-03) enabled page-continuous measure indexing and cumulative page offsets across score systems in `src/score2gp/pdf.py`.
Task 92 (CRP-04) is the fourth stage of the Conversion Recovery Programme. It enforces process-level reference isolation in `scripts/private_e2e_smoke.py` (preventing reference `.gp` paths from being passed as templates to `write_gp` during conversion generation) and establishes `tests/test_real_source_oracles.py` for post-conversion reference oracle validation and falsification against known-bad mutations.

## Goal

Enforce process-level reference isolation during PDF-to-GP generation in `scripts/private_e2e_smoke.py` and create `tests/test_real_source_oracles.py` to evaluate post-conversion output against reference `.gp` files without reference contamination during generation.

## Allowed Files

- `scripts/private_e2e_smoke.py`
- `tests/test_real_source_oracles.py`

## Non-goals

- Do not modify higher-level layout models or parsing heuristics.
- Do not pass reference `.gp` templates into `write_gp` during PDF conversion generation.
- Do not calibrate test assertions to hardcoded file hashes or arbitrary static coordinates.

## Acceptance

- `python3 scripts/private_e2e_smoke.py --pdf fixtures/private/Lesson-5.pdf` executes conversion generation without receiving or discovering reference `.gp` paths as template inputs.
- `pytest tests/test_real_source_oracles.py` passes cleanly.
- `python3 scripts/agent_verify.py` passes with zero regression.
