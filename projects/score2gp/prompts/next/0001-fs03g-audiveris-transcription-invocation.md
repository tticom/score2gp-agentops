# 0001 - FS-03G Audiveris Transcription Invocation

## Objective

Determine whether the committed standalone OMR wrapper omits the Audiveris transcription step. This is evidence-only work. Do not alter product code.

## Start

1. Work only in canonical Ubuntu WSL paths under /home/tticom/work/score2gp-workspace.
2. Prove gh auth status identifies tticom-automation and local Git identity is tticom-automation / tticomautomation@gmail.com.
3. Read ACTIVE_TASK.md and AGENT_CONTROL.md.
4. Fetch origin/main. If either repository has unrelated changes, stop and report without resetting, cleaning, or deleting anything.
5. Create an AgentOps branch named agy/fs03g-audiveris-transcription-invocation from origin/main. Use an ignored product work directory; do not modify product tracked files.

## Execute

At product revision df6e5c8178794f0ea7f98d69e069a1be3593f176, use only:
- tests/fixtures/pdf/generated_standard_staff_whole_note.pdf
- tests/fixtures/pdf/generated_paired_notation_tab_system.pdf

Use the official rootless Audiveris 5.7.0 Ubuntu 24.04 x86_64 executable already evidenced by FS-03C. For each PDF, run in separate ignored output directories:

1. The committed score2gp omr wrapper.
2. Direct Audiveris with -batch -transcribe -export -output <isolated-output> -- <pdf>.

For every XML or MXL artifact, record exact command, executable path, product SHA, PDF SHA-256, exit status, output-tree summary, XML/MXL structural validity, root/part/measure/note/pitched-note/rest counts, and sanitized log warnings/errors.

Do not run convert. Do not use private inputs. Do not modify source, tests, fixtures, schemas, configuration, or generated assets.

## Decide

- If direct transcribe produces non-zero events while the wrapper produces zero, report wrapper-invocation evidence only. Do not implement a change.
- If both are empty, report the first observed upstream limitation without guessing.
- If either command fails, report its first failure.

## Publish

1. Write projects/score2gp/reports/2026-07-23-fs03g-audiveris-transcription-invocation-matrix.md.
2. Update ACTIVE_TASK.md status to PR_OPEN.
3. Commit only these AgentOps files, push the agy/ branch, and open one AgentOps PR.
4. The PR body must state the exact head SHA, commands, matrix verdict, validation, and residual risk.
5. Do not merge. Stop at READY_FOR_CODEX_REVIEW.
