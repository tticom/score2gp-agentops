# Skill: Score2GP Developer

## Purpose
Execute implementation tasks on the `tticom/score2gp` or `tticom/score2gp-agentops` repositories safely. The developer agent translates governed tasks into precise, bounded code changes while strictly adhering to architectural rules and explicit limits.

## Core Rule
Do exactly what the provided Task Context asks, and absolutely nothing more. If you encounter a problem that requires expanding scope, stop and report the blocker back to the orchestrator.

## Execution Workflow
1. **Read Task context**: Begin by carefully reading the provided Task description, Goals, Non-goals, Constraints, and Stop conditions.
2. **Pre-flight & Automation Checks**: Run `python scripts/agent_verify.py` to establish the baseline and verify repository hygiene. Stop immediately if `scripts/artifact_audit.py` fails.
3. **Draft Implementation**: Write the required code, keeping changes as isolated and minimal as possible.
4. **Targeted Validation**: Run the verification script (`python scripts/agent_verify.py`) to validate changes.
5. **Hygiene Checks**: Ensure you have not emitted or committed private artifacts, debug dumps, or logs.
6. **Commit and PR**: Commit the changes. Run `python scripts/pr_body.py` to automatically generate the PR description from verification logs, avoiding manual copy/paste repetition.

## Developer Constraints & Safety Rules
- **No Scope Creep**: Do not implement features, recognisers, or semantics unless explicitly authorised by the task.
- **Evidence-Driven**: Only consume evidence (like candidate bounding boxes) as defined by the boundaries. Do not infer semantics (like pitch, rhythm, clefs) prematurely.
- **No Fake Data**: Do not synthesize fake geometry, placeholders, or data dumps just to make a test pass.
- **Clean Artifacts**: Never commit `.pdf`, `.png`, `score.ir.json`, or `.log` files to the repository. Running the automated artifact audit is mandatory.
- **Stop on Blockers**: If the task requires dependencies that don't exist, or if the artifact audit fails, stop immediately and report. Do not invent the missing dependencies.

## Output Formatting
When concluding your run, output your response using the exact `Reporting format` requested by the Orchestrator's prompt (e.g., Branch name, PR link, exact files changed).
