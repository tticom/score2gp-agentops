# 0007 - CR-04A False-Rest and Per-Voice Capacity Architecture

## Objective

Locate the first committed-evidence divergence that creates the Lesson-5
false-rest candidate, and define a deterministic per-voice measure-capacity
gate. Produce a Developer-ready rule and public regression plan. This is a
bounded architecture and diagnostic task, not product implementation.

## Start

1. Work only in canonical Ubuntu WSL repositories below
   `/home/tticom/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `AGENT_CONTROL.md`, `ACTIVE_TASK.md`, the Architect skill, this prompt,
   the CR-04A backlog entry, and product `AGENTS.md`.
4. Require clean governance and product worktrees.
5. Fetch both repositories and require product `origin/main` to contain merge
   commit `ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f`.
6. Create one governance branch named
   `agy/cr04a-false-rest-capacity-architecture`.

## Evidence Questions

Trace the relevant committed path from recognition outcomes through timeline
construction and MusicXML emission. Establish:

1. where the Lesson-5 extra rest first appears;
2. whether it is extracted falsely, inserted as padding, duplicated across
   voices, or created during serialization;
3. the available meter/divisions/voice/chord/backup evidence at that point;
4. the earliest safe injection point for a generic capacity check;
5. how chord members, rests, voice changes, and MusicXML backup/forward
   elements contribute to independent voice duration;
6. the exact observable condition that must refuse rather than silently trim,
   rescale, or report strict success.

Use public fixtures and tests where they expose the behavior. Private Lesson-5
input may be inspected only if already available under the approved fixture
policy; record only sanitized facts and hashes. If the mismatch cannot be
reproduced from permitted evidence, report the precise observability gap while
still defining any capacity rule supported by committed code.

## Required Rule Packet

The report must specify:

- event grain and voice ownership;
- duration calculation in divisions/ticks;
- treatment of chord members and zero-advance events;
- treatment of rests, backups, and forwards;
- expected duration per measure and per voice;
- underfull, exact, and overfull outcomes;
- refusal code and the stage that emits it;
- malformed or missing-evidence behavior;
- no-mutation and fail-closed constraints;
- exact allowed product files for implementation;
- public positive, negative, and adversarial tests;
- focused and full verification commands.

Do not authorize a filename rule, fixture coordinate, fixed measure number,
hard-coded duration, global event-count threshold, silent deletion, or
cross-voice balancing.

## Stop / Continue Decision

Continue to a Developer prompt only when the evidence identifies:

- one implementation injection point;
- a generic false-rest rejection or refusal rule;
- a deterministic per-voice capacity calculation;
- measurable public regressions;
- a narrow product file allowlist.

Otherwise stop with `OBSERVABILITY_GAP` and list the minimum additional
instrumentation or public fixture needed. Do not guess.

## Deliverables

Commit only governance artifacts:

- `projects/score2gp/reports/2026-07-24-cr04a-architecture.md`;
- a Developer prompt under `projects/score2gp/prompts/next/` only if all
  continue criteria pass;
- `ACTIVE_TASK.md` and `prompts/NEXT.md` updated to the resulting next state.

Run governance diff and cleanliness checks, push the `agy/` branch, and open
one governance PR with the evidence summary, limitations, and exact next
decision. Stop for Codex review. Do not modify product files, start the
Developer task, enable auto-merge, or merge.
