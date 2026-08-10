# 0046 — M6: Page-Continuous Measure Indexing & Offsets (CRP-03)

Status: MERGED

## Objective
Enable sequential measure tracking across page boundaries and compute cumulative page height coordinate offsets in `src/score2gp/pdf.py` (`_extract_pdf_text_candidates`) to prevent page-boundary index conflicts and coordinate collisions.

## Start
1. Branch from `origin/main` in the `score2gp` product repository.
2. Confirm the branch name is `agy/crp-03-page-continuous-measure-indexing`.
3. Read `docs/design/2026-08-09-conversion-module-migration-map.md`.
4. Verify standard tests pass.

## Implementation Scope & Seam Contract
Modify only `src/score2gp/pdf.py` and test file `tests/test_pdf.py`:
1. **Sequential Page Indexing**: Update `_extract_pdf_text_candidates` to track `running_bar_index` dynamically across page iterations, passing it to `_detect_tab_systems` instead of re-initializing to 1 on page change.
2. **Cumulative Page Offsets**: Calculate global y-coordinate offsets by summing preceding page heights to prevent candidate overlap and coordinate collisions across page boundaries.

## Validation Commands
1. Run `agent_verify.py`:
   ```bash
   python3 scripts/agent_verify.py
   ```
2. Verify multi-page smoke tests:
   ```bash
   python3 scripts/private_e2e_smoke.py --pdf fixtures/private/Lesson-5.pdf
   ```

## Deliverables
- Branch `agy/crp-03-page-continuous-measure-indexing` pushed to `origin`.
- Pull Request opened on GitHub.

