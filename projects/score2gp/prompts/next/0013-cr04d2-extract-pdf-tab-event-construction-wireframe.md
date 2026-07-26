# 0013 - CR-04D2 Extract PDF-Only Tab Event Construction

## Objective

Extract conversion of one grouped PDF-only TabRaw subgroup into a note or
explicit-rest `Event`, preserving every observable field. This is a Tier B
Developer task authorising one bounded product PR.

## Preconditions

1. PR #386 is externally merged as
   `56eddc2d9132763d271f45cfbc399d44696bdd9d`.
2. Product `origin/main` contains `pdf_tab_measure_timing.py`.
3. Product and governance worktrees are clean.
4. Prompt 0014 is not active.

Stop if any precondition fails.

## Start

1. Work only in canonical Ubuntu WSL repositories.
2. Prove GitHub/Git identity is `tticom-automation`.
3. Read control files, Developer skill, product `AGENTS.md`, the CR-04D plan,
   and this prompt.
4. Fetch both repositories and record product `origin/main`.
5. Run `.venv/bin/python scripts/agent_verify.py` before editing.
6. Branch `agy/cr04d2-extract-pdf-tab-event-construction` from product
   `origin/main`.

## Required Refactor

Extract a cohesive internal constructor for one already-grouped candidate
subgroup. It must accept explicit context (bar/event indexes, onset, selected
duration, editable annotation inputs) and return one `Event` without hidden
mutation. `build_ir_from_tabraw_only()` retains grouping, capacity checking,
onset advancement, remainder rests, bar assembly, diagnostics, and warnings.

Preserve exactly:

- event ID, track ID, timing and notated duration;
- note string, fret, pitch, confidence, and provenance;
- chord ordering and duplicate-string behaviour;
- explicit quarter-rest handling and empty notes;
- event confidence and full subgroup provenance;
- editable-draft first-event text, including tempo wording.

Preferred internal module: `src/score2gp/pdf_tab_event_factory.py`. Stop rather
than introduce a circular import or move public exception/schema types.

## Approved Surface

- `src/score2gp/build_ir.py`
- `src/score2gp/pdf_tab_event_factory.py` (new, if viable)
- one focused unit-test file
- existing PDF-only behavioural tests only when necessary

Do not change timing policy, candidate grouping, CLI production, schemas,
MusicXML, notation OMR, GP writers, diagnostics, or public APIs.

## Acceptance

1. Existing note, chord, rest, duplicate-string, CLI, and GP tests pass
   unchanged.
2. Focused tests prove note, chord, explicit rest, provenance/confidence, and
   editable first-event annotation cases.
3. Normalized event values before/after are identical for representative public
   scenarios.
4. `build_ir_from_tabraw_only()` has less event-construction responsibility.
5. No observable output, warning, diagnostic, refusal, or schema change.

## Validation

```bash
.venv/bin/python -m pytest tests/test_pdf_only_tab.py \
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
pre/post evidence, and stop for independent review. Do not merge or start D3.
