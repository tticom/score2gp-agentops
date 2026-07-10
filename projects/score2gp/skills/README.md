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
