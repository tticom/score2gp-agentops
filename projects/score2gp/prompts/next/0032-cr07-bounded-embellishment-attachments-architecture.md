# 0032 - CR-07 Bounded Embellishment Attachments Architecture

## Objective

Determine a generic, testable architecture in `tticom/score2gp` for bounded embellishment attachments (such as vibrato, slides, bends, hammer-ons, pull-offs, and palm muting).

The architecture must evaluate one technique class at a time with source glyph/geometry, source and target event ownership, ordering, and true-negative controls (e.g. ensuring chordal vibrato is handled separately from single-note vibrato).

This is an Architect/research task in `tticom/score2gp`. Product source code implementation is not authorized.

## Start

1. Work only in the canonical Ubuntu WSL repositories below `/home/tticom-automation/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `projects/score2gp/AGENT_CONTROL.md`, `projects/score2gp/ACTIVE_TASK.md`, `projects/score2gp/prompts/next/0032-cr07-bounded-embellishment-attachments-architecture.md`, `projects/score2gp/skills/architect/SKILL.md`, `projects/score2gp/tasks/2026-07-17-visual-output-correctness-backlog.md`, and product repository `AGENTS.md`.
4. Require clean governance and product worktrees.
5. Fetch both repositories and accept current product `origin/main` as the baseline for CR-07 research.
6. Run `python scripts/agent_verify.py` in the product repository before analysis.
7. Create product branch `agy/cr07-bounded-embellishment-attachments-architecture` in `tticom/score2gp`.

## Required Investigation

Trace the current behavior through relevant product paths, including:

- `src/score2gp/gpif.py`
- `src/score2gp/ir.py`
- `src/score2gp/pdf.py`
- `src/score2gp/tabraw.py`

Establish with exact file/function references:

1. how embellishments and techniques are currently represented in ScoreIR and GPIF;
2. how embellishment glyphs or curve/text primitives near TAB lines are detected or attached;
3. how single-note vs chordal embellishments are distinguished;
4. which public fixtures reproduce embellishment extraction and attachment.

## Required Outcome

Choose exactly one:

- `CONTINUE`: evidence supports one bounded Developer slice;
- `RESEARCH_NEXT`: one named uncertainty requires one bounded diagnostic task;
- `STOP`: no safe implementation task is currently justified.

If `CONTINUE`, propose exactly one smallest Developer slice with authorized product files, test fixtures, negative controls, and validation commands.

## Durable Deliverables

Write in product repository `tticom/score2gp`:

- `docs/design/cr07-bounded-embellishment-attachments-architecture.md`

Stop after publishing one product architecture PR in `tticom/score2gp` for independent Codex review. Do not modify product source code in `score2gp`.
