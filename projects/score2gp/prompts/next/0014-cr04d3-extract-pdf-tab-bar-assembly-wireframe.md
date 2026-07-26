# 0014 - CR-04D3 Extract PDF-Only Tab Bar Assembly

## Objective

Extract assembly of one already-selected PDF-only TabRaw source bar into an
internal module, preserving every observable field and refusal. This is a
Tier B Developer task authorising one bounded product PR.

## Preconditions

1. PR #387 is externally merged as
   `36b30167ad9719e461a8c6b4a6e49f669faf5f4b`.
2. Product `origin/main` contains `pdf_tab_measure_timing.py` and
   `pdf_tab_event_factory.py`.
3. Product and governance worktrees are clean.
4. Prompt 0015 is not active.

Stop if any precondition fails.

## Start

1. Work only in canonical Ubuntu WSL repositories.
2. Prove GitHub/Git identity is `tticom-automation`.
3. Read control files, Developer skill, product `AGENTS.md`, the CR-04D plan,
   and this prompt.
4. Fetch both repositories and record product `origin/main`.
5. Run `.venv/bin/python scripts/agent_verify.py` before editing.
6. Branch `agy/cr04d3-extract-pdf-tab-bar-assembly` from product `origin/main`.

## Required Refactor

Create `src/score2gp/pdf_tab_bar_assembler.py` with a cohesive internal
constructor for one source bar's already-selected candidates. The module must
use the merged D1 duration-policy functions, the D2 event factory, and
`PdfOnlyChordEventGrouper`.

The constructor must accept explicit context: source-bar candidates,
output-bar index, track ID, editable-draft flag, tempo and explicit-tempo
state, and chord-grouping tolerance. It must return one `Bar` without mutating
caller-owned collections or diagnostics.

The assembler owns:

- empty-bar whole-rest construction;
- candidate subgrouping and the 64-event safety limit;
- duration/grid selection;
- event construction and onset advancement;
- capacity checking;
- deterministic remainder-rest construction;
- final 4/4 `Bar` construction.

`build_ir_from_tabraw_only()` retains input/layout gating, source-bar key
selection and candidate filtering, `output_bar_to_frets`, iteration across
source bars, public `BuildIrInputRiskError` construction, warnings,
diagnostics, `ScoreIR` construction, and all external behavior.

Do not move the public exception. If the assembler detects too many events or
overcapacity, it must raise a small internal structured exception carrying the
facts needed for `build_ir_from_tabraw_only()` to translate it into the exact
existing `BuildIrInputRiskError` category, stage, message, and details. Stop
rather than introduce a circular import.

Preserve exactly:

- source-bar and output-bar ordering and indexes;
- subgroup and event order, event/rest IDs, track IDs, and onsets;
- note/rest timing, notated duration, confidence, provenance, and text;
- duplicate-string grouping behavior;
- 64-event refusal and measure-overcapacity refusal payloads;
- unreachable empty-bar behavior;
- remainder-rest order and fields;
- warnings, diagnostics, ScoreIR, GPIF, schemas, and public interfaces.

## Approved Surface

- `src/score2gp/build_ir.py`
- `src/score2gp/pdf_tab_bar_assembler.py` (new)
- `tests/test_pdf_tab_bar_assembler.py` (new)
- existing PDF-only behavioral tests only when necessary

Do not change timing or recognition policy, candidate grouping semantics,
public exception/schema types, CLI production, MusicXML, notation OMR, GP
writers, diagnostics, or public APIs.

## Acceptance

1. Focused tests characterize empty, single-note, chord, sequential,
   duplicate-string, explicit-rest, mixed-overcapacity, and 65-event refusal
   cases.
2. Existing multi-bar and cross-page public tests pass unchanged.
3. Independent fixed expectations or a reproducible baseline/head comparison
   prove normalized `Bar` values are identical for representative public
   single-event, chord, explicit-rest, and multi-event scenarios.
4. Refusal tests prove exact category, stage, message, and details remain
   unchanged after translation.
5. `build_ir_from_tabraw_only()` retains only cross-bar orchestration and has
   materially less per-bar assembly responsibility.
6. No observable output, warning, diagnostic, refusal, schema, or GPIF change.

## Validation

```bash
.venv/bin/python -m pytest tests/test_pdf_tab_bar_assembler.py \
  tests/test_pdf_only_tab.py \
  tests/test_pdf_only_chord_event_grouper_event_grouping.py \
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

Commit/push one product branch, open one PR, record exact remote head and
pre/post evidence, and stop for independent review. Do not merge or start D4.
