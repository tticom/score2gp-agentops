# Prompt Chain Documentation & Directory Guide

This guide describes how to structure and document the prompt chain for multi-prompt or multi-turn agent runs under the ScoreToGP project.

## Directory Structure

For multi-prompt sessions, the run, research report, or review record should be organized inside a unique slug-named directory rather than a single file:

```text
projects/score2gp/runs/YYYY-MM-DD-short-run-slug/
  RUN.md                 <-- The main result record (follows RUN_RECORD_TEMPLATE.md)
  prompt-manifest.json   <-- The manifest file mapping all prompts (follows PROMPT_MANIFEST_TEMPLATE.json)
  prompts/               <-- Subdirectory containing immutable prompt files
    001-initial.md       <-- The first received prompt (follows PROMPT_RECORD_TEMPLATE.md)
    002-followup.md      <-- The next followup prompt
```

This structure is also supported and required under:
- `projects/score2gp/research/YYYY-MM-DD-short-slug/`
- `projects/score2gp/reviews/YYYY-MM-DD-short-slug/`

---

## Instructions

1. **Create the Directory**: When starting a run that you anticipate will involve multiple prompts/turns, create a directory under `runs/`, `reviews/`, or `research/` following the pattern `YYYY-MM-DD-short-slug`.
2. **Record Every Prompt**:
   - Save every explicit prompt received from the human user or external pipeline as a new `.md` file inside the `prompts/` subdirectory.
   - Number them sequentially starting from `001` (e.g. `prompts/001-initial.md`, `prompts/002-followup.md`).
   - Use the `PROMPT_RECORD_TEMPLATE.md` to format each file, including any state assumptions or specific context.
3. **Maintain the Manifest**:
   - Create and update a `prompt-manifest.json` at the root of the run directory.
   - Populate the prompt fields, listing which prompts are superseded and identifying the final **operative prompt** that drove the final result/commit.
4. **Final Result File**:
   - Write the main result file (`RUN.md`, `REVIEW.md`, or `RESEARCH.md`) inside the directory.
   - Fill in all template requirements, and specify the prompt manifest location and operative prompt ID under the `Prompt Chain` section.
