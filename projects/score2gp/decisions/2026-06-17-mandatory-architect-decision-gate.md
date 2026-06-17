# Decision Record: Mandatory Architect Decision Gate for Note Recognition

**Date:** 2026-06-17
**Context:** Governance Update — Add Mandatory Architect Decision Gate for Note Recognition Path Selection

## Status
Accepted

## Context
Score2GP has reached a point where open-ended raster diagnostics are no longer acceptable as an Architect outcome. The pattern of unbounded "more diagnostics" recommendations must be stopped to ensure visible progress toward the intended outcome.

Prior raster work was already bounded as diagnostic-only, and handling of weak/malformed evidence mattered. This new governance control acts as a decision gate to stop that pattern from becoming an endless loop of diagnostics.

## Decision
Future Architect prompts for note-recognition strategy decisions must include a mandatory Architect Decision Gate. The Architect must not end with an unbounded diagnostic recommendation.

The Architect must choose exactly one of:

1. **Outcome A — Raster path is viable:** Provide a concrete measurable raster approach, references, validation plan, and the smallest next Developer task.
2. **Outcome B — Raster path is not viable but another approach is:** Provide the alternative approach, references, why it is more viable than raster, validation plan, and the smallest next Developer task.
3. **Outcome C — No currently viable approach:** State that Score2GP cannot currently progress toward reliable note recognition under present constraints. Identify the missing prerequisite and the smallest unblocker, if one exists. Do not authorise Developer work.

## Consequences
- The requirement writer must enforce this gate in `REQUIREMENT_PROMPTING_CONTRACT.md`.
- Unbounded diagnostic tasks ("do more diagnostics") without a specific hypothesis, metric, and stop/pivot condition are strictly forbidden.
- This governance decision requires alignment across:
  - `REQUIREMENT_PROMPTING_CONTRACT.md`
  - `skills/architect/SKILL.md`
  - `AGENT_CONTROL.md`
- The canonical meaning for note-recognition Architect outcomes across all these files is:
  - **A:** raster viable;
  - **B:** raster not viable but alternative viable;
  - **C:** no viable implementation path and no Developer authorisation.
- If the Architect cannot choose A, B, or C with evidence, the result is failure, not another vague research task.
