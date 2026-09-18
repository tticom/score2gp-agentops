# AGY-002 — Durable Cycle Completion and Restart Recovery

Status: READY — not executable until separately promoted in ORCHESTRATION_STATE.json.
Role: Developer
Repository: `score2gp-agentops`

## Objective

Make completion of an AGY cycle durable and replay-safe. A process restart or
loss of ignored runtime records must not make completed work executable again,
and completion must preserve enough sanitized evidence to audit the result.

## Allowed paths

- `scripts/agy_cycle.py`
- `plan/backlog.yaml`
- `docs/cycle-history/**`
- `tests/test_agy_cycle.py`

Do not modify product code, Score2GP task authority, prompts outside this task,
identity policy, review rules, or merge behavior.

## Required behavior

1. Completing a cycle writes an append-only durable summary containing the task
   ID, cycle ID, attached PR, exact PR head, merge commit, validation receipt,
   and completion timestamp.
2. Repeating completion for the same cycle is idempotent and does not create a
   second completion or successor execution.
3. A task recorded as completed remains ineligible after ignored runtime cycle
   records are removed.
4. A successor may be recorded as prepared, but completion must never claim or
   execute it automatically.
5. Interrupted completion and replay have deterministic, tested outcomes.

## Validation

- `python3 -m pytest -q tests/test_agy_cycle.py`
- `git diff --check`

Tests must exercise the public cycle controller behavior, including a negative
control proving that a completed task cannot be claimed again after runtime
cleanup. Do not use private Score2GP fixtures or product conversion claims.

## Stop conditions

Stop and report a blocker if completion can be replayed as new work, completion
evidence is lost after runtime cleanup, a successor is automatically claimed,
or one cycle can attach more than one PR.
