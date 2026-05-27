# ScoreToGP Architecture Decisions (ADR)

This document records the architectural decisions governing agent workflows and review posture for the ScoreToGP project.

---

## ADR-001: Separate Product Repo from Agent-Governance Repo
- **Status**: **Approved**
- **Decision**: Product logic, CLI commands, tests, and public schemas live in `score2gp`. Agent governance, sceptical review rules, prompt templates, and benchmark ladders live in `score2gp-agentops`.
- **Reason**: Decoupling the control plane (agent instruction) from the data plane (product logic) prevents product codebases from being polluted with LLM coordinating prose or brittle prompts.

## ADR-002: Reviewer/Architect Agent Must Review Before Prompting
- **Status**: **Approved**
- **Decision**: The reviewer agent must verify all local evidence and checks before generating the next implementation prompt.
- **Reason**: Ensures next implementation prompts are grounded in strict observed failures and verified evidence, preventing "blind steering" or recurring loop regressions.

## ADR-003: Visual/Source Evidence Outranks Generated Diagnostic Summaries
- **Status**: **Approved**
- **Decision**: Direct visual/source page inspection always outranks intermediate diagnostic tables, summaries, or logs. If they disagree, the tool output is assumed to be wrong.
- **Reason**: Diagnostic tables are compiled by the compiler itself and can easily mis-index or omit failures (e.g. failing to capture Measures 15 & 16 in the PDF).

## ADR-004: Strict, Remediation, Semantic, and File Existence Are Separate States
- **Status**: **Approved**
- **Decision**: Every review and prompt must report strict mode, remediation mode, semantic comparison, and generated-file existence separately.
- **Reason**: Combining these metrics creates false confidence. An output file existing does not imply semantic correctness, and remediation success does not prove strict gate compliance.

## ADR-005: Private Benchmarks Are Local Diagnostics, Not Public Fixtures
- **Status**: **Approved**
- **Decision**: Private lesson PDFs and GP oracle files must remain strictly private and outside version control. They guide local human-verified diagnosis but must never be committed to either repository.
- **Reason**: Respects intellectual property boundaries, prevents data leakage, and preserves repository hygiene.
