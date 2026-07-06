# Active Task

**Task**: Architect research — 8th/16th-note recognition and rhythm-semantics strategy
**Authorised Role**: Architect
**Repository**: `tticom/score2gp-agentops`

## 1. Baseline
- Product PR #336 merged at `cae6a416076e66f6b84940ad0cbf3061beb241d9`.
- Governance PR #238 merged at `96397d845b924fb27b12753940ccfec7251ebb09`.
- Whole-note work is parked, and workflow loop tiers (Tier A/B) are active.
- Project is at a clean `NO_ACTIVE_TASK_APPROVED` baseline prior to this authorisation.

## 2. Context
8th and 16th notes are critical recognition targets for rhythm notation. However, they introduce significant technical complexity (stems, beams, flags, rhythmic onset mapping, duration classification). This is a new recognition strategy and product-behaviour area, and is therefore classified as Tier A (Full Loop). Developer implementation is not authorised. The Architect must research and propose a viable technical strategy.

## 3. Scope
- **Approved**: Bounded research into 8th/16th noteheads, stems, flags, beams, coordinate association, beamed sub-beat segmentation, ScoreIR tick mapping, track rhythmic grouping, and GP export implications. Read-only inspection of existing product repository files, tests, and public fixtures.
- **Excluded**: Product code changes, adding new generated fixtures or PDFs, speculative or unproven claims, 32nd-note work, and Developer implementation.

## 4. Required Output & Outcome
The Architect must write a self-contained research report under `projects/score2gp/research/2026-07-06-8th-16th-note-recognition-strategy.md` separating facts, inferences, hypotheses, and unknowns. The report must conclude with selecting exactly one of:
- **Outcome A**: A raster/product path is viable. Provide the smallest implementable next Developer task, exact files affected, fixture/test requirements, validation strategy, acceptance criteria, and stop conditions.
- **Outcome B**: A direct raster/product path is not viable, but another bounded approach is. Provide the alternate approach, evidence, smallest implementable next Developer task, fixture requirements, validation strategy, acceptance criteria, and stop conditions.
- **Outcome C**: No viable implementation path is currently justified. No Developer work is authorised. Identify the missing prerequisite and next research question.

## 5. Artifact & Privacy Constraints
- No private score PDFs or copyrighted music may be processed.
- No generated PDFs, GP files, screenshots, logs, or dumps may be committed.
- Propose fixture requirements but do not create any files.

## 6. Required Next Review
Reviewer architecture verification.
