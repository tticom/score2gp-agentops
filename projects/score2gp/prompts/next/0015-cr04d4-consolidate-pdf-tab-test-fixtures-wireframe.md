# 0015 - CR-04D4 Consolidate PDF-Only Tab Test Fixtures

## Objective

Reduce repeated PDF-only `TabCandidate`, `BoundingBox`, and TabRaw-file setup
without weakening the explicit behavioural meaning introduced by CR-04D3.
This is a Tier B Developer task authorising one bounded, test-only product PR.

## Preconditions

1. Product PR #388 is externally merged as
   `cea235d83e72e608b841e5d6d55b631077fa1833`.
2. Product `origin/main` contains `pdf_tab_bar_assembler.py` and
   `test_pdf_tab_bar_assembler.py`.
3. Product and governance worktrees are clean apart from ignored local
   environments.
4. Prompt 0016 is not active.

Stop if any precondition fails.

## Start

1. Work only in the canonical `tticom-automation` Ubuntu WSL repositories.
2. Prove Linux, HOME, GitHub, Git, and repository identity gates before writes.
3. Read the control files, Developer skill, product `AGENTS.md`, CR-04D plan,
   and this prompt.
4. Fetch both repositories and prove product `origin/main` is the merged #388
   state above.
5. Run `.venv/bin/python scripts/agent_verify.py` before editing.
6. Branch `agy/cr04d4-consolidate-pdf-tab-test-fixtures` from product
   `origin/main`.

## Verified Duplication Inventory

Merged `test_pdf_tab_bar_assembler.py` contains repeated direct construction
of `TabCandidate` and `BoundingBox` values across empty, note, chord,
sequential, duplicate-string, explicit-rest, tolerance, refusal, and complete
normalized-`Bar` cases. The focused chord-grouper tests repeat the same base
layout fields. Large literal normalized-`Bar` dictionaries are deliberate
independent oracles and are not ordinary setup duplication.

## Required Refactor

Create one small test-helper module with explicit builders for the repeated
input setup. Prefer narrow helpers such as:

- a `TabCandidate` builder whose defaults represent a valid PDF-only fret
  candidate and whose arguments expose scenario-significant fields;
- an explicit quarter-rest candidate builder only if it is clearer than
  overriding the fret builder;
- a helper that writes a `TabRaw` file only where multiple refusal tests repeat
  that exact serialization boundary.

Use the helpers in the focused CR-04D tests where they materially reduce
duplication and make scenario differences easier to see.

The helpers must:

- create fresh model/list/dict instances on every call;
- expose IDs, raw text/fret, x/y, string, bar/system/staff/page indexes,
  confidence, and bbox overrides needed by the existing scenarios;
- preserve exact default values, ordering, provenance inputs, and JSON
  serialization used by the current tests;
- remain test-only and must not be imported by product code.

Do not turn distinct behaviours into a broad parameter matrix. Do not replace
complete normalized-`Bar` literal expectations with production constructors,
shared expected-value builders, snapshots generated during the test, or
partial assertions. Those literals are intentionally verbose independent
oracles.

## Required Characterization

Before consolidating, record the focused test count and prove the merged tests
pass. After consolidation:

1. every pre-existing focused test remains present by name unless a rename is
   explicitly justified;
2. empty, single-note, chord, sequential, duplicate-string, explicit-rest,
   custom-tolerance, mixed-overcapacity, 65-event refusal, exact public refusal
   translation, and all four complete normalized-`Bar` cases still pass;
3. the complete literal normalized-`Bar` dictionaries remain semantically
   unchanged;
4. at least one focused helper test proves fresh objects are returned and
   caller mutation cannot leak into a later scenario;
5. existing multi-bar, cross-page, CLI refusal, chord grouping, quarter-rest,
   duration consistency, and GP validation tests pass unchanged.

## Approved Surface

- `tests/pdf_tab_test_helpers.py` (new)
- `tests/test_pdf_tab_bar_assembler.py`
- `tests/test_pdf_only_chord_event_grouper_event_grouping.py`
- `tests/test_pdf_only_tab_quarter_rest.py` only if the helper makes the
  scenario clearer
- `tests/test_pdf_only_tab.py` only for repeated setup directly shared with the
  named refusal/equivalence cases

No production file is approved. Do not change `src/`, schemas, CLI, fixtures,
recognition/timing/grouping policy, public APIs, warnings, diagnostics,
refusals, ScoreIR, GPIF, or writers.

## Acceptance

1. The duplication inventory and resulting helper boundary are documented in
   the PR evidence.
2. Repeated input setup is materially reduced without hiding scenario intent.
3. Every named regression remains independently asserted and test collection
   does not lose required cases.
4. Complete normalized-`Bar` literal oracles and exact refusal payload
   assertions remain complete and fixed.
5. Helper calls are isolated: no mutable default or cross-test state leakage.
6. Product code and all observable behaviour are unchanged.

## Validation

```bash
.venv/bin/python -m pytest --collect-only -q \
  tests/test_pdf_tab_bar_assembler.py \
  tests/test_pdf_only_chord_event_grouper_event_grouping.py \
  tests/test_pdf_only_tab_quarter_rest.py tests/test_pdf_only_tab.py
.venv/bin/python -m pytest \
  tests/test_pdf_tab_bar_assembler.py tests/test_pdf_only_tab.py \
  tests/test_pdf_only_chord_event_grouper_event_grouping.py \
  tests/test_pdf_only_tab_quarter_rest.py tests/test_cli_convert.py
.venv/bin/python scripts/agent_verify.py
.venv/bin/python -m pytest
.venv/bin/python -m score2gp.cli export-schema --out schemas
.venv/bin/python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json
.venv/bin/python scripts/artifact_audit.py
git diff --check origin/main...HEAD
git diff --exit-code -- schemas
git diff --name-only origin/main...HEAD
git ls-files fixtures/private work
git status --short
git status --branch
```

The changed-file list must contain only the approved test surface.

## Deliverables

Commit and push one product branch, open one PR with the before/after
duplication inventory, test collection count, exact remote head, and validation
evidence, then stop for independent review. Do not merge or begin CR-04D5.
