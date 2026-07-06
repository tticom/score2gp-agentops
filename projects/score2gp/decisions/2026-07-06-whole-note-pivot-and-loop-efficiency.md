# Supervisor Decision — Whole-Note Pivot and Loop Efficiency Rules

**Date**: 2026-07-06  
**Role**: Supervisor  
**Status**: Approved / Active Policy  

## 1. Context & Rationale
The whole-note recognition and export development effort has completed its E2E integration test loop using a synthetic single-note vector PDF fixture. This proof-of-concept verified the E2E pipeline, CLI argument parsing, and GP package structure but represents only a narrow capability. 

The loop took multiple iterations, was heavily manual, and highlighted process overheads in the governance-to-product cycle. In addition, product PR #336 was merged with two procedural deviations.

This decision record durably resolves both deviations as historical exceptions, parks further whole-note development, and introduces workflow efficiency updates to compress the loop for future low-risk recognition work.

## 2. Whole-Note Capability and Parking
- **Landed Capability**: Positive E2E validation for `notation-whole-note-export` with `--assume-treble-clef` on a synthetic vector PDF (`generated_standard_staff_single_whole_note.pdf`), producing a verified single-track, single-note `.gp` package.
- **Not Landed / Excluded**: Arbitrary score PDFs, standard music font glyph recognition (Emmentaler/LilyPond font glyph subset mapping), broad whole-note recognition, and multi-note/multi-bar export.
- **Project Pivot**: Whole-note work is parked. Due to the high complexity and low product priority of whole notes compared to 8th, 16th, and 32nd notes, no further whole-note implementation is authorised.

## 3. Historical Deviation Approvals
The Supervisor hereby resolves the two deviations from product PR #336:
1. **Lack of Pre-authorisation in `ACTIVE_TASK.md`**: Approved as a historical exception only. Future developer implementation work MUST be explicitly authorised in `projects/score2gp/ACTIVE_TASK.md` before coding begins.
2. **Committed Generated PDF Fixture**: Approved as a historical exception only. Committing the 2.0KB PDF to `tests/fixtures/pdf/` violated the strategy's stop condition but aligned with existing repository tracked-fixture convention. This exception does not create precedent. Future generated PDF commits require explicit task-level authorization.

## 4. Future Artifact Policy
- **Generated `.gp` packages**: Strictly forbidden from being tracked in git.
- **Generated PDF fixtures**: Allowed only if explicitly authorised in the task contract/prompt, public/reproducible, lightweight (<1MB), and required for unmocked regression or E2E tests.

## 5. Workflow Loop Compression
To reduce Supervisor manual touchpoints while preserving accuracy, we establish two workflow tiers:

### Tier A: Full Loop (High-Risk Work)
Required when the task involves:
- Uncertain architecture or new recognition strategies.
- Product behaviour changes or database schema modifications.
- Artifact policy exceptions or private/copyrighted data risk.
- Failed tests or unresolved Codex/review threads.
- Broad semantic claims.
- **Process**: Must follow separate sequential stages: Requirement -> Architect Research -> Reviewer Architecture Verification -> Developer Implementation -> Reviewer Conformance Review -> PR Readiness Review -> Merge.

### Tier B: Compressed Loop (Low-Risk Work)
Allowed when the task is limited to:
- Markdown-only governance recording or minor process improvements.
- Narrow bug fixes with pre-approved architecture.
- Fixture/test-only changes where expected behaviour is already authorised.
- PRs with no product behaviour broadening.
- No private/artifact risk, clean test suite, and no unresolved Codex threads.
- **Compression Rules**:
  - The requirement packet includes acceptance and readiness criteria up front.
  - One combined Reviewer performs implementation conformance review and PR readiness review in a single pass.
  - Governance completion records can be bundled with the next Supervisor decision in `ACTIVE_TASK.md` during state transitions, rather than requiring standalone PRs.
  - Merge operators still perform the final guarded merge check.

## 6. Stop and Pivot Rule
For low-value or low-priority recognition targets:
- Maximum one architecture/implementation iteration loop is authorised.
- If only synthetic capability is proven and real-world capability remains blocked, the agent must record the partial result, clean up all scratch files, and pivot back to Supervisor decision. No further iterations are authorised.

## 7. Current Project State
The project remains in the `NO_ACTIVE_TASK_APPROVED` state. No Developer implementation or Architect research task is currently approved. The next action belongs to the Supervisor to select the next capability (e.g., 8th/16th note rhythm recognition) using the compressed loop rules.
