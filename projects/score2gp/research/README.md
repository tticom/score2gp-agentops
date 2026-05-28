# ScoreToGP Research Records

This directory contains durable, evidence-backed research reports and analyses for the ScoreToGP agent executions.

## Mandatory Evidence Record Rule

Every agent task must create or update one durable markdown file in `score2gp-agentops` before reporting completion.

Accepted locations:
- `projects/score2gp/runs/<date>-<slug>.md`
- `projects/score2gp/reviews/<date>-<slug>.md`
- `projects/score2gp/research/<date>-<slug>.md`

The record must include:
- repo and branch
- command(s) run
- input availability, using private-safe basenames only
- output directory path, if any
- strict conversion status
- remediation/diagnostic status
- generated file existence
- semantic round-trip status
- exact blocker category
- private-safe metrics
- public tests run
- private-safety audit
- next required evidence

If no report file was written, the task is incomplete.

## Mandatory Prompt Chain Rule

Every agent run must record the exact explicit prompt chain used for that run.

If the run includes multiple prompts, each prompt must be stored as a numbered immutable file under a `prompts/` directory.

The final run/research/review record must state which prompt was operative for the final commit or conclusion.

A PR body is not sufficient.
A final chat response is not sufficient.
Console output is not sufficient.
A report without the prompt chain is incomplete.

Agents cannot reliably record hidden platform/system instructions. They must record the explicit prompt text they received, plus the governance docs and repository refs they were instructed to read.
