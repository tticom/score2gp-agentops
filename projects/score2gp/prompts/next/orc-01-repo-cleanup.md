# ORC-01: Repository Hygiene & Cleanup

## Objective
Clean up the score2gp and agentops repositories by removing redundant files and establishing a consistent method of recording tasks, actions, tests, and outcomes.

## Contract
- **Input Class:** The score2gp and score2gp-agentops repositories.
- **Observable Outputs:** Deletion of obsolete `*TASKS*.md` files, old prompt recordings, unmaintained folders, and orphaned scripts. Introduction of a unified task-recording convention.
- **Allowed Paths:** (Globally across both repositories for markdown/doc/json files, no product source code changes).
- **Validation Commands:** `git diff --check`, `pytest` (to ensure no tests were accidentally broken by removal of fixtures).
- **Negative Controls:** Must not delete active control plane JSONs (`ORCHESTRATION_STATE.json`) or active orchestration code. Must not modify product source code (`score2gp/src/`).
- **Promotion Dependency:** BENCH-01
- **Provenance:** Added per user instruction to prioritize repository hygiene.
