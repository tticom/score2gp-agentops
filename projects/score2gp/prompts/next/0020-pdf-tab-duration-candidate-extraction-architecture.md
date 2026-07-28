# 0020 - PDF-Tab Duration Candidate Extraction Architecture

## Status

ACTIVE — PDF-tab duration candidate extraction architecture authorised after
synthetic fixture `generated_pdf_tab_duration.pdf` merged into product main at `1a013cef0f242f1a75428c1ddfa77c251a2b22f0` and AgentOps PR #388 merged at `af37834cfca753017a557b6926e8ffd28bff997c`.

## Objective

Design the architectural dataflow and integration boundaries for associating
detected vertical stems, beams, and flags with PDF-only tablature events.
Currently, `select_pdf_tab_grid_spacing_and_duration_name` assigns uniform beat
durations based solely on event count, ignoring geometric stem/beam/flag
primitives. The Architect must produce a bounded architecture specification
and implementation roadmap that connects morphology duration candidates to PDF
tab bar assembly (`pdf_tab_bar_assembler.py` / `pdf_tab_measure_timing.py`)
without breaking existing PDF-tab conversion or standard notation diagnostics.

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
- synthetic fixture SHA-256 for `generated_pdf_tab_duration.pdf`;
- exact test and inspection commands with exit codes.

The product revision must contain `1a013cef0f242f1a75428c1ddfa77c251a2b22f0`. Run
`python scripts/agent_verify.py` before work and after research, and stop if it
fails.

## Allowed Files

### In `score2gp-agentops`:
- `projects/score2gp/architectures/2026-07-28-pdf-tab-duration-candidate-extraction-architecture.md`
- `projects/score2gp/runs/2026-07-28-pdf-tab-duration-candidate-extraction-architecture.md`

All product source modules in `src/` remain strictly read-only during this
architectural phase.

## Non-goals

No product source code modifications, no reference GP leakage, no private inputs,
no automatic merge, branch deletion, or premature implementation work.

## Requirements

1. **Dataflow & Seam Definition**: Trace the exact path from
   `NotationStaffDiagnostics` (or direct morphology Primitive primitive
   collections) through `TabRaw` into `assemble_pdf_tab_bar` /
   `PdfOnlyChordEventGrouper`.
2. **Stem & Beam Association Criteria**: Define spatial tolerance rules for
   associating vertical stems and horizontal/diagonal beams to specific fret text
   x-positions within a tab staff.
3. **Fallback & Legacy Heuristic Boundary**: Specify how the system handles
   un-stemmed tab staves (falling back to equal-spacing heuristics) vs
   stemmed/beamed tab staves.
4. **Implementation Slicing Plan**: Break the implementation into small, Tier B
   testable developer slices with concrete acceptance criteria driving
   `generated_pdf_tab_duration.pdf` oracle verification.

## Durable report

Create:

1. `projects/score2gp/architectures/2026-07-28-pdf-tab-duration-candidate-extraction-architecture.md`
2. `projects/score2gp/runs/2026-07-28-pdf-tab-duration-candidate-extraction-architecture.md`

Use `durable-handoff`. Include:

- pinned provenance;
- architectural dataflow diagrams and interface specifications;
- disconfirmation of potential failure modes (e.g. false stem attachment to barlines or fret text);
- proposed developer implementation prompt structure.

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

Commit and push branch `agy/pdftab-duration-extraction-architecture`, then open
one AgentOps PR.

Do not approve or merge the PR. Stop for independent hard review.
