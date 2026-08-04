# 0030 - CR-06 Key-Signature Semantics Architecture

## Objective

Determine a generic, testable architecture in `tticom/score2gp` for key-signature evidence detection on notation staves.

The architecture must distinguish explicit sharp/flat key-signature glyph evidence from the absence of key-signature evidence. It must never emit C-major / A-minor (0 accidentals) as a "recognized key signature" when evidence is absent or ambiguous, and must never manufacture accidentals or alter pitch assignments from unknown key signature evidence.

This is an Architect/research task in `tticom/score2gp`. Product source code implementation is not authorized.

## Start

1. Work only in the canonical Ubuntu WSL repositories below `/home/tticom-automation/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `projects/score2gp/AGENT_CONTROL.md`, `projects/score2gp/ACTIVE_TASK.md`, `projects/score2gp/prompts/next/0030-cr06-key-signature-semantics-architecture.md`, `projects/score2gp/skills/architect/SKILL.md`, `projects/score2gp/tasks/2026-07-17-visual-output-correctness-backlog.md`, and product repository `AGENTS.md`.
4. Require clean governance and product worktrees.
5. Fetch both repositories and accept current product `origin/main` as the baseline for CR-06 research.
6. Run `python scripts/agent_verify.py` in the product repository before analysis.
7. Create product branch `agy/cr06-key-signature-semantics-architecture` in `tticom/score2gp`.

## Required Investigation

Trace the current behavior through relevant product paths, including:

- `src/score2gp/pdf.py`
- `src/score2gp/pdf_staff_geometry.py`
- `src/score2gp/whole_note_recogniser.py`
- `src/score2gp/gpif.py`
- `src/score2gp/cli.py`

Establish with exact file/function references:

1. where key signature information is currently parsed, defaulted, or hardcoded;
2. how sharp (#) and flat (b) key-signature accidental glyphs near clefs are extracted or ignored;
3. how key-signature evidence is passed to GPIF or ScoreIR;
4. which public fixtures reproduce key-signature absence vs explicit key signatures.

## Required Outcome

Choose exactly one:

- `CONTINUE`: evidence supports one bounded Developer slice;
- `RESEARCH_NEXT`: one named uncertainty requires one bounded diagnostic task;
- `STOP`: no safe implementation task is currently justified.

If `CONTINUE`, propose exactly one smallest Developer slice with authorized product files, test fixtures, negative controls, and validation commands.

## Durable Deliverables

Write in product repository `tticom/score2gp`:

- `docs/design/cr06-key-signature-semantics-architecture.md`

Stop after publishing one product architecture PR in `tticom/score2gp` for independent Codex review. Do not modify product source code in `score2gp`.
