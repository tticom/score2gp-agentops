# 0018 - PDF-Tab Duration-Evidence Adequacy Audit

## Status

ACTIVE — evidence audit authorised after AgentOps PR #383 merged at
`b3918e19d9130b52bcfacfe53133f5794efbad82`.

## Objective

Determine whether current public PDF fixtures, committed diagnostics, and the
PDF-only tab dataflow provide enough observable evidence to authorize a
bounded duration/beam implementation. Do not change product code or create a
fixture. The task ends with evidence and one explicit decision.

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
- SHA-256 for every inspected fixture;
- exact test and inspection commands with exit codes.

The product revision must contain
`d70d559152c5aa357a7d2eb38e65b09f288bb08f`. Run
`python scripts/agent_verify.py` before evidence collection and stop if it
fails.

## Required public evidence

Inspect only committed public material. At minimum:

- `tests/fixtures/pdf/generated_scorelike_tab.pdf`;
- `tests/fixtures/pdf/generated_uneven_spacing_tab.pdf`;
- `tests/fixtures/pdf/generated_paired_notation_tab_system.pdf`;
- the corresponding fixture generators;
- `tests/test_pdf_staff_geometry_diagnostics.py`;
- `tests/test_quarter_rest_e2e_acceptance.py`;
- `tests/test_deterministic_multinote_sequencing.py`;
- the production modules connecting PDF geometry, flag/beam candidates,
  TabRaw, PDF-only grouping, bar assembly, and ScoreIR timing.

If a listed file has moved, record the exact replacement. Do not substitute a
private PDF, MusicXML sidecar, reference GP, or remembered behavior.

## Required inspection

### 1. Visual/source fixture audit

Render or directly inspect each PDF and its generator. For every fixture,
record:

- whether it contains tablature;
- whether it contains explicit varied rhythmic notation;
- whether beams, flags, stems, or other duration marks are visibly present;
- whether expected durations are independently encoded anywhere;
- whether it is multi-bar and suitable for a deterministic public oracle.

A filename or generator comment is not visual evidence.

### 2. Dataflow audit

Trace the committed production path and record:

- where flag/beam candidates are created;
- whether they are associated with the tab staff, standard staff, or neither;
- whether their coordinates survive into TabRaw;
- whether event grouping can associate them with a note/chord candidate;
- where PDF-only timing currently becomes the fixed spatial eighth-note
  heuristic;
- the smallest ownership boundary that could consume duration evidence
  without mixing recognition, grouping, or measure-capacity policy.

Cite exact files, symbols, and line numbers at the pinned product SHA.

### 3. Executable disconfirmation

Run the smallest relevant existing public tests. Add no tests and change no
fixtures. Test the strongest plausible false-success mode:

> Standard-staff beam diagnostics exist, but no committed public PDF-tab
> fixture or production seam can connect those candidates to PDF-only tab
> events; therefore green tests could falsely imply implementation readiness.

Record which parts are proved, contradicted, or still unverified. Passing
tests alone cannot establish readiness.

## Decision gate

Return exactly one primary result:

- `IMPLEMENTATION_READY`: a public multi-bar PDF-tab oracle exists, duration
  evidence reaches a defined seam, expected behavior is measurable, and a
  bounded implementation allowlist can be named;
- `PUBLIC_FIXTURE_GAP`: the production seam is plausible, but no adequate
  committed public oracle exists;
- `ARCHITECTURE_GAP`: public evidence exists, but duration candidates do not
  reach a safe ownership boundary or recognition/grouping responsibilities
  remain unresolved;
- `BLOCKED`: required public evidence or runtime provenance cannot be
  inspected reliably.

Do not select `IMPLEMENTATION_READY` from count equality, green tests, file
existence, or standard-staff diagnostics alone.

## Durable report

Create exactly one file:

`projects/score2gp/runs/2026-07-27-pdf-tab-duration-evidence-adequacy-audit.md`

Use `durable-handoff`. Include:

- pinned provenance and author-reported versus independently checked evidence;
- fixture-by-fixture visual/source results;
- dataflow map with citations;
- test commands and results;
- strongest false-success mode and disconfirmation result;
- the primary decision;
- the smallest follow-up candidate with an explicit allowlist and measurable
  acceptance criteria only when supported by the decision.

Any follow-up remains unauthorised.

## Validation and publication

In AgentOps run:

```bash
python -m pytest -q tests/test_governance_audit.py
python scripts/score2gp_governance_audit.py
git diff --check
git status --short
```

Only the single durable report may change. Commit and push branch
`agy/pdftab-duration-evidence-audit`, then open one AgentOps PR. The PR body
must state the exact remote head, the primary decision, the strongest
false-success mode tested, residual unknowns, and that no product/private
files changed.

Do not approve or merge the PR. Stop for independent hard review.
