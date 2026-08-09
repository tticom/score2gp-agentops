# 0045 — M6: Topologically Locked System Barlines (CRP-02)

Status: APPROVED

## Objective
Topologically lock 5-line notation barlines to 6-line TAB barlines system-by-system in `src/score2gp/pdf.py` before event extraction, closing the remaining 2-bar gap (41 -> 43 bars on `Lesson-5.pdf`) and ensuring system barlines do not bleed across system or page boundaries.

## Start
1. Branch from `origin/main` in the `score2gp` product repository.
2. Confirm the branch name is `agy/crp-02-topologically-locked-system-barlines`.
3. Read `docs/design/2026-08-09-conversion-module-migration-map.md`.
4. Verify standard tests pass.

## Implementation Scope & Seam Contract
Modify only `src/score2gp/pdf.py` and test files `tests/test_pdf_geometry_candidate_extractor.py`, `tests/test_pdf.py`:
1. **System-by-System Topological Locking**: Lock notation staff and TAB staff barlines system-by-system before event extraction, preventing barline bleed across system boundaries.
2. **43-Bar Alignment**: Ensure extracted notation bar boxes on `Lesson-5.pdf` reach full 43-bar alignment across 12 systems.

## Validation Commands
1. Run `agent_verify.py`:
   ```bash
   python3 scripts/agent_verify.py
   ```
2. Verify `Lesson-5.pdf` barline extraction:
   ```bash
   python3 scripts/private_e2e_smoke.py --pdf fixtures/private/Lesson-5.pdf
   ```

## Deliverables
- Branch `agy/crp-02-topologically-locked-system-barlines` pushed to `origin`.
- Pull Request opened on GitHub.

