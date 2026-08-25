# ORC-02: Agent Isolation & Control-Plane Cutover

## Objective
Isolate all agent instructions to the agentops repository, leaving the score2gp repository completely free of agentic governance files. Execute the state cutover to convert legacy `go` and `got` commands into thin compatibility wrappers around the shared resolver.

## Contract
- **Input Class:** score2gp and score2gp-agentops repositories.
- **Observable Outputs:** 
  1. Migration of any remaining `.agents/`, `agy/`, or agentic config files from `score2gp` to `score2gp-agentops`.
  2. Convert legacy `go` and `got` into thin compatibility wrappers around the shared resolver per step 4 of `ORCA_WORKFLOW.md`.
- **Allowed Paths:** score2gp/.agents/*, score2gp-agentops/scripts/*, score2gp-agentops/projects/*
- **Validation Commands:** AgentOps tests, `python3 -m pytest tests/test_score2gp_orca_control.py`.
- **Negative Controls:** Must not break the Orca control plane resolver. Must leave `score2gp` fully operational as a pure product repository.
- **Promotion Dependency:** ORC-01
- **Provenance:** Added per user instruction to isolate agents and complete the orchestration migration.
