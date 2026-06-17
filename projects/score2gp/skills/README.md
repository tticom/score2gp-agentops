# Score2GP Agent Skills

This directory contains mandatory role skills for Score2GP governance.

Role skill files are not optional guidance. `AGENT_CONTROL.md` defines when they must be loaded.

The Architect, Developer, and Reviewer skills exist to prevent speculative work, diagnostic drift, and implementation drift. They enforce a strict execution loop:

- **Architect** researches and must select exactly one bounded outcome (A: raster viable, B: alternative viable, or C: not currently justified/no Developer work).
- **Reviewer** verifies architecture/research plausibility.
- **Developer** implements the approved requirement using requirement-driven TDD.
- **Reviewer** verifies implementation conformance to the requirement and architecture.
- **Reviewer** separately verifies PR readiness.
