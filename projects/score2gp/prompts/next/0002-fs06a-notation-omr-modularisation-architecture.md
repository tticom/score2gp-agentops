# 0002 - FS-06A Notation OMR Modularisation Architecture

## Objective

Define the compatibility-first migration of the overloaded whole_note_recogniser.py module into a cohesive score2gp.notation_omr package. Produce one concrete first implementation task. Do not edit product code.

## Start

1. Work only in canonical Ubuntu WSL paths under /home/tticom/work/score2gp-workspace.
2. Prove gh auth status identifies tticom-automation and local Git identity is tticom-automation / tticomautomation@gmail.com.
3. Read ACTIVE_TASK.md, AGENT_CONTROL.md, and this prompt.
4. Fetch origin/main. If either repository has unrelated changes, stop and report without resetting, cleaning, or deleting anything.
5. Create AgentOps branch agy/fs06a-notation-omr-modularisation from origin/main.

## Execute

Use only committed product source and public tests.

1. Build an import and caller map for whole_note_recogniser.py, including CLI entry points and tests.
2. Partition actual responsibilities into proposed score2gp.notation_omr modules, such as models, staff_geometry, duration_evidence, rest_evidence, pitch, timeline, and diagnostics, but retain only boundaries supported by the code.
3. Define a compatibility shim in whole_note_recogniser.py and the public interfaces that must remain stable during the first migration.
4. Specify an ordered set of small implementation PRs. Each must have an ownership boundary, allowed files, test command, behaviour-preservation contract, rollback condition, and no private-fixture dependency.
5. Select one smallest first implementation task. It must move a cohesive low-risk unit behind the shim without changing observable behaviour.

Do not rename or move product files, add package modules, change tests, or modify any product behaviour.

## Evidence Quality

Use exact file and symbol references. Before publishing, scan the report for ASCII control characters other than newline and tab; fail and repair the report if any are found. Do not claim an interface is public unless a caller or test proves it.

## Publish

1. Write projects/score2gp/reports/2026-07-23-fs06a-notation-omr-modularisation-architecture.md.
2. Update ACTIVE_TASK.md status to PR_OPEN.
3. Commit only the report and active-task update, push the agy/ branch, and open one AgentOps PR.
4. The PR body must state the exact head SHA, selected first implementation task, validation, and residual risk.
5. Do not merge. Stop at READY_FOR_CODEX_REVIEW.
