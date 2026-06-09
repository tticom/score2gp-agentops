# Agentic Skills

This directory contains codified procedures and workflow constraints for autonomous agents working on the `score2gp` project.

## Convention

We use a flat directory structure for these skill definitions (e.g., `score2gp-pr-hard-review.md`). 
In the `agy` (Antigravity) environment, these markdown files do not require a strict `SKILL.md` sub-directory layout to function. The agent reads the raw markdown files directly when invoked or instructed to apply a specific skill.

By keeping them as flat markdown files, they are easy to read, modify, and reference in PR comments and system prompts.
