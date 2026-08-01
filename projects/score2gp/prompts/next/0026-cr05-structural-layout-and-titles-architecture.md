# 0026 - CR-05 Structural Layout and Titles Architecture

## Objective

Determine a generic, testable architecture for independently classifying:

1. ordinary, double, and final barlines;
2. system and page layout breaks;
3. phrase or piece titles and their ownership by a system or measure.

A double or final barline must not imply a system break merely because of its barline type.

This is an Architect/research task in `tticom/score2gp`. Product source code implementation is not authorized.

## Start

1. Work only in the canonical Ubuntu WSL repositories below `/home/tticom-automation/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `projects/score2gp/AGENT_CONTROL.md`, `projects/score2gp/ACTIVE_TASK.md`, `projects/score2gp/prompts/next/0026-cr05-structural-layout-and-titles-architecture.md`, `projects/score2gp/skills/architect/SKILL.md`, `projects/score2gp/tasks/2026-07-17-visual-output-correctness-backlog.md`, and product repository `AGENTS.md`.
4. Require clean governance and product worktrees.
5. Fetch both repositories and record present maintainer authorization to accept current product `origin/main`, including commit `f3cf042c96defdaf09c3353f16f9dbcb38e542d3`, as the baseline for CR-05 research without historical reconstruction.
6. Run `python scripts/agent_verify.py` in the product repository before analysis.
7. Create product branch `agy/cr05-structural-layout-and-titles-architecture` in `tticom/score2gp`.

## Required Investigation

Trace the current behavior through relevant product paths, including:

- `src/score2gp/pdf.py`
- `src/score2gp/pdf_staff_geometry.py`
- `src/score2gp/whole_note_recogniser.py`
- `src/score2gp/cli.py`
- any directly invoked layout, text-classification, barline, grouping, or ownership helpers discovered during tracing

Do not assume the initially listed files contain the complete production path.

Establish with exact file/function references:

1. where barline type is classified;
2. where system/page breaks are inferred;
3. whether barline type currently influences layout-break classification;
4. where text above or near staves is extracted and classified;
5. how title ownership is currently represented or lost;
6. which public fixtures reproduce each observed defect;
7. which private samples provide supporting evidence without becoming test dependencies.

## Required State Separation

The architecture must define separate representations for:

- barline type;
- system-break evidence;
- page-break evidence;
- title/text classification;
- title-to-system ownership;
- title-to-measure ownership;
- absence of evidence;
- ambiguous or conflicting evidence.

Do not encode system layout as a consequence of double/final barline classification.

Do not treat arbitrary nearby text as a title without classification and ownership evidence.

## Required Falsification

For each proposed rule, provide:

- a positive example;
- a negative control differing in the controlling fact;
- an ambiguity or conflict case;
- the smallest broken implementation that the proposed test must reject;
- exact observable output;
- stop/continue/pivot criteria.

At minimum, disconfirm:

1. every double barline becoming a new system;
2. every system break requiring a double barline;
3. page-edge proximity alone causing a false break;
4. arbitrary text above a staff becoming a phrase title;
5. one title being assigned to multiple neighbouring systems;
6. fixture-specific coordinates masquerading as generic geometry.

## Required Outcome

Choose exactly one:

- `CONTINUE`: evidence supports one bounded Developer slice;
- `RESEARCH_NEXT`: one named uncertainty requires one bounded diagnostic task;
- `STOP`: no safe implementation task is currently justified.

If `CONTINUE`, propose exactly one smallest Developer slice with:

- authorized product files;
- public fixture or deterministic synthetic fixture;
- exact production seam;
- acceptance assertions;
- negative controls;
- compatibility requirements;
- validation commands;
- explicit non-goals.

Do not bundle barline classification, layout reconstruction, and title ownership into one implementation PR unless evidence proves they are inseparable.

## Durable Deliverables

Write in product repository `tticom/score2gp`:

- `docs/design/cr05-structural-layout-and-titles-architecture.md`

The report must include:

- accepted baseline revisions;
- present maintainer authorization to proceed without historical reconstruction;
- verified repository facts;
- hypotheses and unknowns;
- evidence ledger;
- disconfirmation record;
- selected outcome (`CONTINUE`, `RESEARCH_NEXT`, or `STOP`);
- recommended follow-up candidate, if applicable;
- what was not verified.

Stop after publishing one product architecture PR in `tticom/score2gp` for independent Codex review.

Do not modify product source code in `score2gp`. Do not create or modify AgentOps candidate prompts, `projects/score2gp/ACTIVE_TASK.md`, `projects/score2gp/prompts/NEXT.md`, or governance run records in `score2gp-agentops`.
