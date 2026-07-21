# Active Task

**Task**: FS-03D: Compatible Public Sidecar-Handoff Matrix
**Authorised Role**: Developer, Tier B evidence-only
**Repository**: `tticom/score2gp` and `tticom/score2gp-agentops`

## Status

PR_OPEN

## Context

FS-03C was recorded through governance PR #345, merged as
`418a2bf2897aff05212e0935535957cc85cef450`. It established that rootless
Audiveris can generate a structurally valid MXL sidecar on the authorised
standard-staff fixture, but that fixture has no safe TAB grouping. Its
`missing_pdf_grouping` refusal therefore does not test the explicit sidecar
handoff on a compatible PDF.

FS-03D determines that missing fact using current public fixtures only. It does
not change product behaviour, call OMR from `convert`, or claim musical
correctness from a written sidecar or GP file.

## Execution Model

Follow the Agy local-preparation boundary in `AGENT_CONTROL.md`:

- prove that WSL `gh auth status` is unauthenticated, then do not run `gh`;
- create only fresh local `agy/` worktrees from `origin/main`;
- do not modify any existing worktree, publish, push, create a PR, or merge;
- leave local commits and worktrees intact for Codex review.

## Required Matrix

Probe these candidates in this order, using a new ignored work directory per
candidate:

1. `tests/fixtures/pdf/generated_paired_notation_tab_system.pdf`
2. `tests/fixtures/pdf/generated_paired_notation_tab_system_double_barline.pdf`

For each candidate:

1. Run the committed `.venv/bin/score2gp extract-tab` command and inspect the
   produced TabRaw JSON. Record playable candidate count; assigned
   system/string/bar counts; and unsafe grouping warning codes.
2. Run the pinned rootless Audiveris 5.7.0 Ubuntu 24.04 x86_64 asset through
   the committed `.venv/bin/score2gp omr` command. Verify the published SHA-256
   before extraction and record the manifest status and sidecar SHA-256.
3. Run one committed explicit `.venv/bin/score2gp convert --musicxml` handoff
   using the exact manifest artifact and record exit status, stage, refusal
   code, output-written flag, timing issue count, and first remaining warning.

If a candidate cannot supply safe PDF grouping, record that fact and continue
to the next candidate. Do not alter the fixture, manually edit MusicXML, use a
different OMR engine, or attempt a repair.

## Classification Rules

- `compatible_pdf`: the inspected PDF has at least one playable candidate and
  safe system/string/bar grouping according to the committed diagnostics.
- `artifact_available`: the standalone OMR manifest reports successful
  execution, discovery, and structural validation.
- `handoff_observed`: an explicit handoff reaches a result beyond PDF grouping;
  it is not a musical-correctness claim.
- `handoff_supported`: only if the committed command writes output with no
  unresolved timing refusal. Otherwise use the exact refusal and classify the
  untested capability as `unproven`.

## Scope And Handoff

Do not change product source, tests, configuration, schemas, generated assets,
or private fixtures. Write one sanitized report at
`projects/score2gp/reports/2026-07-21-fs03d-compatible-public-handoff-matrix.md`
and update this task status to `LOCAL_HANDOFF_READY` on the local AgentOps
branch. Commit locally only.

The report must contain an exact claim ledger, commands, product and AgentOps
base SHAs, CLI/import paths, asset and sidecar hashes, per-candidate matrix,
and a pre-submit challenge. Finish with the local branch and exact local head
for Codex review.
