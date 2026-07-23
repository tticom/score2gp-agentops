# Active Task

**Task**: FS-03G: Audiveris Transcription Invocation Evidence Matrix
**Authorised Role**: Architect, Tier B evidence-only
**Repository**: tticom/score2gp and tticom/score2gp-agentops

## Status

AGY_EXECUTION_AUTHORISED

## Context

FS-03F, merged through governance PR #351, proves that the explicit sidecar route can create non-zero ScoreIR events and match playable TAB candidates when supplied a valid public MusicXML fixture. It does not make standalone Audiveris usable.

The committed standalone wrapper invokes Audiveris with -batch -export -output. Official Audiveris CLI documentation distinguishes transcription from export and documents -transcribe as a separate option (https://audiveris.github.io/audiveris/_pages/guides/advanced/cli/). FS-03G tests this invocation difference only. It does not alter the wrapper or claim that either route produces musically correct output.

## Execution Model

Execute only the versioned prompt selected by `projects/score2gp/prompts/NEXT.md`.
That prompt is the authoritative execution and publication contract for this task.
This file supplies scope and evidence constraints only; it must not introduce a
different branch, handoff, or publication path.

## Required Verification

Use product revision df6e5c8178794f0ea7f98d69e069a1be3593f176. Use only these public PDFs:
- tests/fixtures/pdf/generated_standard_staff_whole_note.pdf
- tests/fixtures/pdf/generated_paired_notation_tab_system.pdf

Use the already evidenced rootless Audiveris 5.7.0 Ubuntu 24.04 x86_64 executable only in new ignored directories. For each PDF, run two isolated commands:
1. The committed score2gp omr wrapper, which invokes Audiveris with -batch -export -output.
2. A direct Audiveris probe with -batch -transcribe -export -output <isolated-output> -- <pdf>.

For each produced XML or MXL artifact, record:
- command, executable path, exact product SHA, PDF hash, exit status, and output tree;
- artifact discovery result, container/root validity, and root/part/measure/note/pitched-note/rest counts;
- sanitized Audiveris log warning/error summaries;
- any direct difference between wrapper and transcribe runs.

Do not run convert, do not use private inputs, and do not modify product source, tests, fixtures, configuration, schemas, or generated assets.

## Interpretation And Handoff

- If the transcribe probe produces non-zero MusicXML events where the wrapper produces zero, classify this only as wrapper-invocation evidence. Do not implement a fix.
- If both routes remain empty, record that the cause is inside or upstream of Audiveris and remains unproven.
- If either route fails, record the first failure without guessing.

Write one sanitized report at projects/score2gp/reports/2026-07-23-fs03g-audiveris-transcription-invocation-matrix.md. It must include an exact claim ledger, acceptance matrix, pre-submit challenge, branch and exact remote head. Update this task to PR_OPEN and publish exactly one Agy PR as required by the versioned prompt.
