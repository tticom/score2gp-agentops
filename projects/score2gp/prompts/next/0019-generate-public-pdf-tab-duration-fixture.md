# 0019 - Generate Public PDF-Tab Duration Synthetic Fixture

## Status

ACTIVE — synthetic fixture creation authorised after AgentOps PR #386 merged at
`700214c3224478adfe2c5c4a6105875da4fcb279`.

## Objective

Address the `PUBLIC_FIXTURE_GAP` established by the audit in PR #386 by
creating a deterministic public synthetic PDF fixture and generator script in
`score2gp`. The fixture must contain multi-bar tablature with explicit drawn
vertical stems, beams, and flags representing varied rhythmic durations
(quarter, eighth, sixteenth notes) and an embedded expected-duration oracle. Do
not modify product source code in `src/score2gp/`.

## Skills and identity

1. Read `projects/score2gp/SKILLS_LOCK.md` and
   `projects/score2gp/WORKFLOW_SKILLS_PROFILE.md`.
2. Verify installed `governed-development-loop`, `identity-safe-git`,
   `durable-handoff`, and `code-review` resolve to locked commit
   `0d6d84879eff0d352b444fdeceb3bb7a098e0c47`.
3. Run the `identity-safe-git` gate for `tticom-automation`.
4. Work only in the automation-owned WSL product and AgentOps clones.

A mismatch is a no-write stop.

## Pin live state

Synchronize both repositories to `origin/main`, verify clean tracked state,
and record:

- full product and AgentOps SHAs;
- locked skills SHA;
- product Python executable and resolved `score2gp` module path;
- SHA-256 for the new generator script and generated PDF fixture;
- exact test and inspection commands with exit codes.

The product revision must contain
`d70d559152c5aa357a7d2eb38e65b09f288bb08f`. Run
`python scripts/agent_verify.py` before work and after test execution, and stop
if it fails.

## Allowed Files

### In `score2gp`:
- `tests/fixtures/pdf/make_generated_pdf_tab_duration_pdf.py`
- `tests/fixtures/pdf/generated_pdf_tab_duration.pdf`
- `tests/test_pdf_tab_duration_fixture.py` (or additions to `tests/test_pdf_staff_geometry_diagnostics.py`)

### In `score2gp-agentops`:
- `projects/score2gp/runs/2026-07-28-generate-public-pdf-tab-duration-fixture.md`

All product source modules in `src/` remain strictly read-only.

## Non-goals

No product code changes, private inputs, reference GP leakage, automatic merge,
branch deletion, or unauthorized promotion of follow-up implementation.

## Requirements

1. **Synthetic Generator**: Create `tests/fixtures/pdf/make_generated_pdf_tab_duration_pdf.py` using ReportLab or ReportLab-equivalent canvas drawing, creating a multi-bar PDF-tab score with drawn vertical stems, beams, and flags for quarter, eighth, and sixteenth notes.
2. **Deterministic PDF Fixture**: Generate and commit `tests/fixtures/pdf/generated_pdf_tab_duration.pdf`.
3. **Expected Oracle & Diagnostics**: Define an explicit expected-duration mapping (e.g. measure/event duration sequence) in comments or test helpers.
4. **Fixture Test**: Add automated unit tests to verify that the PDF generates reproducibly and that diagnostic stem/beam/flag detection extracts candidate geometry from the fixture.

## Durable report

Create exactly one file:

`projects/score2gp/runs/2026-07-28-generate-public-pdf-tab-duration-fixture.md`

Use `durable-handoff`. Include:

- pinned provenance and SHA-256 hashes of generated files;
- description of rhythmic elements drawn in the synthetic PDF;
- test execution results;
- confirmation that product implementation remains untouched.

## Validation and publication

In product repository `score2gp`:

```bash
.venv/bin/python -m pytest -q
python scripts/agent_verify.py
```

In `score2gp-agentops`:

```bash
.venv/bin/python -m pytest -q tests/test_governance_audit.py
.venv/bin/python scripts/score2gp_governance_audit.py
git diff --check
git status --short
```

Commit and push branch `agy/generate-public-pdf-tab-duration-fixture`, then open
one product PR and one AgentOps PR (or combined governance handoff as permitted).
The PR body must state the exact remote head, fixture SHAs, disconfirmation results,
and that no product `src/` files were modified.

Do not approve or merge the PR. Stop for independent hard review.
