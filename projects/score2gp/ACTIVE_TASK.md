# Active Task

**Task**: FS-03E: Sidecar-to-ScoreIR Event-Loss Trace
**Authorised Role**: Architect, Tier B evidence-only
**Repository**: `tticom/score2gp` and `tticom/score2gp-agentops`

## Status

LOCAL_HANDOFF_READY

## Context

FS-03D was recorded through governance PR #347, merged as
`cbc9e983d85750fd69d43bfadadd1642bd2fad8f`. It proved that rootless Audiveris
can generate structurally valid MXL artifacts and that explicit conversion can
reach `gp-write` for two compatible public PDFs. It also found the decisive
limitation: both outputs had `event_count: 0`, `matched_candidate_count: 0`,
and unused TAB candidates. The route is observed, not functionally supported.

FS-03E identifies the first exact data-loss, filtering, or unsupported
transformation between the Audiveris sidecar and the empty ScoreIR result. It
is a research task only: it must not repair, relax, suppress, or reinterpret
the mismatch.

## Execution Model

Follow the Agy local-preparation boundary in `AGENT_CONTROL.md`:

- prove that WSL `gh auth status` is unauthenticated, then do not run `gh`;
- create only fresh local `agy/` worktrees from `origin/main`;
- do not modify any existing worktree, publish, push, create a PR, or merge;
- leave local commits and worktrees intact for Codex review.

## Required Trace

Use the exact public fixtures and exact product revision
`df6e5c8178794f0ea7f98d69e069a1be3593f176`, in this order:

1. `tests/fixtures/pdf/generated_paired_notation_tab_system.pdf`
2. `tests/fixtures/pdf/generated_paired_notation_tab_system_double_barline.pdf`

For each candidate, use new ignored work directories and:

1. Reproduce the committed explicit sidecar handoff and record the source
   artifact identity, MusicXML root/part/measure/note/rest counts, TabRaw
   candidate counts, conversion report summary counts, and warning codes.
2. Inspect the committed source path from MXL parsing through ScoreIR creation.
   Name exact modules, functions, data types, and count-bearing fields at each
   boundary; distinguish direct observation from source-derived inference.
3. Identify the earliest boundary where a non-zero set becomes zero, or state
   precisely why the committed diagnostics cannot determine that boundary.
4. Record whether the loss is caused by a documented unsupported input shape,
   an explicit filter, an association mismatch, or remains unproven. Never
   attribute it to Audiveris merely because the sidecar is upstream.

Do not alter fixtures, manually edit MusicXML, use another OMR engine, add
instrumentation, change source/tests/configuration, or attempt a repair.

## Scope And Handoff

Do not change product source, tests, configuration, schemas, generated assets,
or private fixtures. Write one sanitized report at
`projects/score2gp/reports/2026-07-21-fs03e-sidecar-scoreir-event-loss-trace.md`
and update this task status to `LOCAL_HANDOFF_READY` on the local AgentOps
branch. Commit locally only.

The report must contain an exact claim ledger, commands, product and AgentOps
base SHAs, CLI/import paths, asset and sidecar hashes, boundary-count table,
source-path map, first-loss finding or explicit observability limit, and a
pre-submit challenge. Finish with the local branch and exact local head for
Codex review.
