# 0026 - CR-05 Structural Layout and Titles Architecture

## Objective

Investigate and define the rule packet for separating double/final barline classification, system/page layout, and phrase-title anchoring in score2gp PDF conversion. Produce a Developer-ready rule and public regression plan.

This is a Tier B Architect task. Product implementation is not authorised.

## Start

1. Work only in the canonical Ubuntu WSL repositories below `/home/tticom-automation/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `projects/score2gp/AGENT_CONTROL.md`, `ACTIVE_TASK.md`, this prompt, `projects/score2gp/skills/architect/SKILL.md`, product `AGENTS.md`, and `tasks/2026-07-17-visual-output-correctness-backlog.md`.
4. Require clean governance and product worktrees.
5. Fetch both repositories and require product `origin/main` to contain commit `f3cf042c96defdaf09c3353f16f9dbcb38e542d3`.
6. Run `python scripts/agent_verify.py` in the product repository before analysis.
7. Create governance branch `agy/cr05-structural-layout-and-titles-architecture`.

## Evidence Questions

Trace current PDF layout and text extraction pipelines in product code (`pdf.py`, `pdf_staff_geometry.py`, `whole_note_recogniser.py`, `cli.py`). Establish:

1. How double/final barlines are detected vs ordinary barlines and system breaks;
2. Why a double barline currently forces/implies a line break, and how to decouple line break classification from barline type;
3. How phrase/piece titles are recognized and anchored to measure/system geometry;
4. Observable failure modes on tracked public fixtures and private corpus samples;
5. The exact generic geometric/classification rules required to resolve layout and title ownership without fixture-specific shortcuts.

## Deliverables

Commit governance artifacts in `score2gp-agentops`:
- `projects/score2gp/reports/2026-08-01-cr05-architecture.md`
- Next versioned prompt under `projects/score2gp/prompts/next/` if continue criteria pass
- `ACTIVE_TASK.md` and `prompts/NEXT.md` updated to resulting next state.

Stop for independent Codex review. Do not modify product files.
