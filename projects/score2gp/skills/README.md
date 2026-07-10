# Score2GP Agent Skills

This directory contains mandatory role skills for Score2GP governance.

Role skill files are not optional guidance. `AGENT_CONTROL.md` defines when they must be loaded.

The Architect, Developer, Reviewer, and Project Director skills exist to prevent speculative work, diagnostic drift, implementation drift, and unnecessary human handoffs. They enforce a strict execution loop:

- **Architect** researches and must select exactly one bounded outcome (A: raster viable, B: alternative viable, or C: not currently justified/no Developer work).
- **Reviewer** verifies architecture/research plausibility.
- **Developer** implements the approved requirement using requirement-driven TDD.
- **Reviewer** verifies implementation conformance to the requirement and architecture.
- **Reviewer** separately verifies PR readiness.
- **Project Director** verifies live state, coordinates role transitions, performs continuation/pivot audits, promotes the next safe task, and keeps unattended Antigravity runs moving.

## Antigravity discovery

The governed skill source is:

- `projects/score2gp/skills/project-director/SKILL.md`

Antigravity does not automatically treat every repo markdown file as an installed skill. Runtime copies must be mirrored into the surface-specific discovery paths.

For Antigravity desktop app use:

- `C:\Users\niall\.gemini\antigravity\skills\score2gp-project-director\SKILL.md`

For shared user-level discovery use:

- `C:\Users\niall\.gemini\config\skills\score2gp-project-director\SKILL.md`

For Antigravity IDE user-level discovery use:

- `C:\Users\niall\.gemini\antigravity-ide\skills\score2gp-project-director\SKILL.md`

For Antigravity CLI discovery use:

- `C:\Users\niall\.gemini\antigravity-cli\skills\score2gp-project-director\SKILL.md`

When opening `/home/tticom/work/score2gp-workspace` as the Antigravity IDE folder, workspace custom agents must be available under:

- `/home/tticom/work/score2gp-workspace/.agents/agents/<agent-name>/agent.json`

Workspace-scoped skills should be available under:

- `/home/tticom/work/score2gp-workspace/.agents/skills/<skill-name>/SKILL.md`

The Project Director custom agent is also governed in:

- `.agents/agents/project-director/agent.json`

The Project Director workspace skill is also governed in:

- `.agents/skills/score2gp-project-director/SKILL.md`
