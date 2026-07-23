# Active Task

**Task**: FS-03F: Valid Public MusicXML Sidecar Handoff Verification
**Authorised Role**: Architect, Tier B evidence-only
**Repository**: tticom/score2gp and tticom/score2gp-agentops

## Status

AGY_LOCAL_PREPARATION_AUTHORISED

## Context

FS-03E was recorded through governance PR #349, merged as 9004ea5. The canonical rootless Audiveris artifact for the paired public fixtures is structurally valid but contains zero MusicXML notes. The empty ScoreIR is downstream propagation of an empty sidecar, not an observed Score2GP event-loss transformation.

FS-03F verifies the supported explicit sidecar route with the repository's existing valid public MusicXML fixture. It establishes only whether the committed conversion path creates non-zero events and consumes TAB candidates when supplied a non-empty, public, fixture-matched timing source. It does not repair Audiveris, call OMR, or claim real-score recognition.

## Execution Model

Follow the Agy local-preparation boundary in AGENT_CONTROL.md:
- prove WSL gh auth status is unauthenticated, then do not run gh;
- create only fresh local agy/ worktrees from origin/main;
- do not modify existing worktrees, publish, push, create a PR, or merge;
- leave local commits and worktrees intact for Codex review.

## Required Verification

Use product revision df6e5c8178794f0ea7f98d69e069a1be3593f176 and only:
- PDF: tests/fixtures/pdf/generated_tiny_tab.pdf
- MusicXML: tests/fixtures/musicxml/generated_tiny_tab.musicxml

In a new ignored work directory:
1. Verify both input hashes and inspect MusicXML root, part, measure, note, pitched-note, and rest counts.
2. Run worktree-local .venv/bin/score2gp convert with explicit --musicxml, --out, --work-dir, and --json-report. Do not invoke omr.
3. Record conversion status, stage, refusal code, output-written, bar/event/matched/unmatched counts, warnings, and score.ir.json event count.
4. Do not edit fixtures, MusicXML, outputs, source, tests, or configuration; add no instrumentation or repair.

Acceptance:
- success, gp-write, null refusal, output written;
- event_count > 0 in report and ScoreIR;
- matched_candidate_count > 0;
- unmatched_tabraw_candidate_count recorded;
- exact evidence without musical-equivalence claims.

## Scope And Handoff

Do not change product source, tests, configuration, schemas, generated assets, or private fixtures. Write one sanitized report at projects/score2gp/reports/2026-07-23-fs03f-valid-public-sidecar-handoff.md and update this task to LOCAL_HANDOFF_READY on the local AgentOps branch. Commit locally only.

The report must contain exact claim ledger, commands, product and AgentOps base SHAs, CLI/import paths, input/output hashes, MusicXML and ScoreIR counts, conversion report fields, warnings, acceptance table, pre-submit challenge, local branch and exact local head.
