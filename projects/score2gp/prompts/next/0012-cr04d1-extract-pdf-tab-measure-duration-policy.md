# 0012 - CR-04D1 Extract PDF-Only Tab Measure-Duration Policy

## Objective

Perform the first behaviour-preserving refactor after merged product PR #385:
extract pure duration selection, measure-capacity, and remainder-rest
decomposition policy used by `build_ir_from_tabraw_only()`.

This is a Tier B Developer task authorising one bounded product refactor PR.

## Preconditions

1. Product PR #385 is externally merged.
2. Product `origin/main` contains
   `3715dbdb54c8387c77ab770430998c6160bf07d4`.
3. Governance and product worktrees are clean.
4. No later CR-04D prompt is active.

Stop if any precondition fails.

## Start

1. Work only in canonical Ubuntu WSL repositories.
2. Prove GitHub/Git identity is `tticom-automation`.
3. Read control files, Developer skill, product `AGENTS.md`, this prompt, and
   `plans/2026-07-26-cr04d-pdf-tab-measure-assembly-refactor-sequence.md`.
4. Fetch both repositories and record full product `origin/main`.
5. Run `.venv/bin/python scripts/agent_verify.py` before editing.
6. Branch `agy/cr04d1-extract-pdf-tab-measure-duration-policy` from product
   `origin/main`.

## Behaviour Baseline

Run before production edits:

```bash
.venv/bin/python -m pytest tests/test_pdf_only_tab.py \
  tests/test_pdf_only_tab_quarter_rest.py tests/test_cli_convert.py
```

Protect normal/editable duration selection, actual-duration refusal and error
details, explicit quarter rests, generated-rest names/ticks/order/IDs/onsets,
3840-tick completed bars, ScoreIR/GP validation, and CLI success/refusal.

## Required Refactor

Extract pure internal functions for:

1. grid spacing/notated name selection from event count and editable mode;
2. validating one actual event duration against 3840 ticks while preserving
   `BuildIrInputRiskError`; and
3. greedily decomposing a non-negative remainder into ordered un-dotted
   duration descriptors.

The remainder function must not construct `Event`, read files, mutate a bar, or
depend on candidates. `build_ir_from_tabraw_only()` still creates events and
observable metadata.

Preferred module: `src/score2gp/pdf_tab_measure_timing.py`. If that creates a
cycle or forces public exception movement, keep pure helpers in `build_ir.py`
and report; do not broaden scope.

## Approved Product Surface

- `src/score2gp/build_ir.py`
- `src/score2gp/pdf_tab_measure_timing.py` (new, if viable)
- one focused pure-policy test file
- existing PDF-only TabRaw tests only when needed for preserved coverage

Do not change CLI production, schemas, GP writers, MusicXML, notation OMR,
candidate grouping, public APIs, or event metadata.

## Acceptance

1. Baseline behavioural tests pass unchanged after extraction.
2. Pure tests cover 0, 60, 480, 960, 3840, and over-capacity.
3. Mixed note/rest refusal still reports accumulated ticks `4320`.
4. Rest descriptors remain greedy/deterministic and sum to the remainder.
5. `build_ir_from_tabraw_only()` has less inline duration-policy responsibility.
6. No observable output or schema change.

## Validation

```bash
.venv/bin/python -m pytest tests/test_pdf_only_tab.py \
  tests/test_pdf_only_tab_quarter_rest.py tests/test_cli_convert.py
.venv/bin/python scripts/agent_verify.py
.venv/bin/python -m pytest
.venv/bin/python -m score2gp.cli export-schema --out schemas
.venv/bin/python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json
.venv/bin/python scripts/artifact_audit.py
git diff --check origin/main...HEAD
git diff --exit-code -- schemas
git ls-files fixtures/private work
git status --short
git status --branch
```

## Deliverables

Commit/push one product branch, open one PR, record pre/post evidence and remote
head, and stop for independent review. Do not merge or begin CR-04D2.
