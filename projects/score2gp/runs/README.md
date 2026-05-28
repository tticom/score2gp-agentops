# ScoreToGP Run Records

This directory contains durable, evidence-backed run records for the ScoreToGP agent pipeline executions.

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
