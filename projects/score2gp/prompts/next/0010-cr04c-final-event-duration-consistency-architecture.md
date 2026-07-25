# 0010 - CR-04C Final-Event Duration Consistency Architecture

## Objective

Resolve the smallest correct representation for PDF-only TabRaw final events
whose padded `duration_ticks` disagree with their `notated_duration`, and turn
that decision into a bounded, public-testable Developer authorization.

This is a Tier B Architect task. Product implementation is not authorised.

## Start

1. Work only in the canonical Ubuntu WSL repositories below
   `/home/tticom/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `AGENT_CONTROL.md`, `ACTIVE_TASK.md`, this prompt, the Architect skill,
   product `AGENTS.md`, and
   `tasks/2026-07-25-candidate-task-lesson5-duration-padding.md`.
4. Require clean governance and product worktrees.
5. Fetch both repositories. Use current product `origin/main`, record its full
   SHA, and require it to contain merge commit
   `f47194e57b551d4b571a04c0b7641fbe9c173f80`.
6. Run `python scripts/agent_verify.py` in the product repository before
   analysis. Stop if verification or artifact audit fails.
7. Create governance branch
   `agy/cr04c-final-event-duration-consistency-architecture`.

## Claim Under Test

For a PDF-only TabRaw bar with four sequential candidates, the current final
event can carry `duration_ticks == 2400` while its
`notated_duration.value == "eighth"`. Determine which supported representation
preserves measure capacity and produces semantically truthful ScoreIR and GP:

- retain the grid-sized note and represent remaining capacity as rest event(s);
- split the padded duration into valid tied/notated components;
- use another representation already supported by ScoreIR and the GP writer;
- or refuse the input if none is safe without broader semantics.

## Required Evidence

Use tracked public fixtures or a minimal synthetic public TabRaw input to:

1. reproduce the exact ticks/label mismatch on current product `main`;
2. trace `Timing.duration_ticks` and `NotatedDuration` through ScoreIR
   validation and GPIF serialization;
3. inspect existing rest, tie, dotted-duration, and measure-capacity behavior;
4. compare the candidate representations against current schemas, writer
   support, Guitar Pro package output, and existing tests;
5. identify compatibility effects on PDF-only and editable-draft modes.

Separate fact, inference, hypothesis, and unknown. Cite exact files, functions,
tests, and generated public evidence.

## Decision Requirements

Select exactly one smallest implementation path, or explicitly stop/pivot.
The recommendation must define:

- the invariant connecting ticks, notated duration, and measure capacity;
- exact product files expected to change;
- public failing tests that prove behavior before implementation;
- success, refusal, stop, and pivot criteria;
- whether existing output changes are intentional compatibility corrections;
- validation commands and artifact-safety checks.

Do not authorize a generic duration engine, rhythm recognition, OCR, MusicXML
changes, schema redesign, or fixture-specific Lesson-5 logic.

## Validation

Run read-only or temporary-output experiments only. At minimum:

```bash
python -m pytest tests/test_pdf_only_tab.py tests/test_build_ir.py
python scripts/agent_verify.py
python scripts/artifact_audit.py
git diff --check
git ls-files fixtures/private work
git status --short
git status --branch
```

The private-safety invariant output from `git ls-files fixtures/private work`
must be exactly `fixtures/private/.gitkeep`.

## Deliverables

1. Add a dated architecture/decision record under
   `projects/score2gp/research/` or the established equivalent.
2. Update the duration-padding candidate with the verdict and evidence.
3. If implementation is supported, create the next versioned Developer prompt,
   update `ACTIVE_TASK.md`, and advance `prompts/NEXT.md` to it in the same
   governance PR.
4. If implementation is not supported, record the stop/pivot decision and
   authorize the smallest evidence-producing alternative instead.
5. Commit and push governance changes, open one governance PR, and report its
   branch, PR, full head SHA, evidence, verdict, next authorization, validation,
   and artifact status.
6. Stop for independent Codex review. Do not merge, enable auto-merge, edit
   product code, or begin Developer implementation.
