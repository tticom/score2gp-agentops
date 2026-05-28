# Durable Handoff: Architect to Developer (v1.0)

## Current Workspace State
- **Product Repository**: `score2gp`
- **Architect Branch**: `agent/pdf-to-gp-smoke-v1/architect` (pushed to origin)
- **Governance Repository**: `score2gp-agentops`
- **Handoff Target Branch**: `agent/pdf-to-gp-smoke-v1/developer`

All architectural plans and TPO-approved acceptance criteria have been saved, staged, committed, and pushed to origin on `agent/pdf-to-gp-smoke-v1/architect` under `agent-workflow/tasks/pdf-to-gp-smoke-v1/`:
- [01-architecture-plan.md](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/agent-worktrees/pdf-to-gp-smoke-v1/score2gp-architect/agent-workflow/tasks/pdf-to-gp-smoke-v1/01-architecture-plan.md) (with narrow local geometric filters scope)
- [02-acceptance-criteria.md](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/agent-worktrees/pdf-to-gp-smoke-v1/score2gp-architect/agent-workflow/tasks/pdf-to-gp-smoke-v1/02-acceptance-criteria.md) (TPO approved)

---

## Action Items for the Implementation Developer

The Developer is instructed to execute the following phases precisely to fulfill the product acceptance criteria for the **Major Triads Lesson 3** smoke test:

### Phase 1: Branch Synchronization
1. Synchronize the `agent/pdf-to-gp-smoke-v1/developer` branch with the latest pushed commits from the `agent/pdf-to-gp-smoke-v1/architect` branch.

### Phase 2: Local Layout Filters Implementation (`src/score2gp/pdf.py`)
Implement the following three targeted local filters in `src/score2gp/pdf.py`:

1. **Horizontal Collinear Line Merging (`merge_collinear_horizontal_segments`)**:
   - Before clustering lines into staff system rows, merge horizontal vector segments sharing the same Y-coordinate (within a narrow margin like `1.0` pt) and overlapping or lying collinear within a horizontal gap distance of `10.0` points.
   - This consolidates fragmented left/right vector segments into full-width visual staves, completely resolving the **Collinear System Splitting** issue.

2. **TAB-vs-Notation Staff Pre-Classification (`classify_staff_line_group`)**:
   - Pre-classify line groupings. Ensure that 5-line standard notation staves are explicitly detected and ignored from forming guitar TAB systems.
   - Guitar TAB systems must be validated as having exactly six lines (or reconstructed/valid five lines) and correct spacing.

3. **TAB-Grid Intersect Filtering (`filter_tab_barline_candidates`)**:
   - Filter candidate barlines (vertical vectors) strictly by ensuring they cleanly intersect the Y-extent of the authoritative 6-string TAB staff region.
   - Ignore standard notation note stems/beams (lying entirely within the 5-line notation staff) and short TAB rhythm stems (too short to cross all six strings of the TAB staff).

### Phase 3: Synthetic Messy Public Fixture
- Add the synthetic public PDF fixture at `tests/fixtures/pdf/generated_paired_notation_tab_system.pdf` representing standard notation paired directly above a six-string TAB staff, complete with notation note stems, short TAB rhythm stems, and fragmented horizontal vectors.
- Add regression tests in `tests/test_pdf.py` verifying that:
  - Exactly one TAB system is detected.
  - Standard notation staves are ignored.
  - Note/rhythm stems are ignored as barlines.
  - Fret candidates assign cleanly to systems, strings, and bars with zero unassigned tokens.

### Phase 4: E2E Private Smoke Verification
- Run `python scripts/private_e2e_smoke.py` and verify:
  1. Grouping status becomes `grouped` (no warnings).
  2. All **546 / 546 playable fret candidates** map cleanly with zero unassigned tokens.
  3. Validated `ScoreIR` JSON and `smoke.gp` Guitar Pro file are successfully generated under strict mode.

---

## Safety Guardrails
- **No Loosening Gates**: Do not enable `allow_remediation = True` or `allow_skip_unboxed = True` in strict compiler mode.
- **Private Safety**: Ensure `git ls-files fixtures/private work` outputs exactly `fixtures/private/.gitkeep`. Never commit private music assets or details.
