# 0049 — Dual-Modality Visual TAB Digit OMR (CRP-06)

Status: MERGED

## Objective

Implement `tests/test_tab_digit_recognition.py` and refine TAB candidate text merging in `src/score2gp/pdf.py` to prevent adjacent single-digit frets (e.g. `7` and `10`) from merging into impossible guitar frets (> 24) and classify fret candidates accurately.

## Start

1. Branch from `origin/main` in the `score2gp` product repository.
2. Confirm the branch name is `agy/crp-06-dual-modality-tab-recognition`.
3. Read `docs/design/2026-08-09-conversion-recovery-architecture.md` and `docs/design/2026-08-09-conversion-module-migration-map.md`.
4. Verify standard tests pass.

## Implementation Scope & Seam Contract

Modify `src/score2gp/pdf.py` and create `tests/test_tab_digit_recognition.py`:
1. **Fret Limit Validation**: In the horizontal text-merging loop of `src/score2gp/pdf.py`, validate proposed merged numeric text strings. If a proposed merge yields an integer > 24, break the merge loop and retain them as separate fret candidate tokens.
2. **Candidate Classification**: Ensure single-digit and double-digit frets (0-24) are extracted as distinct fret candidates on notation and TAB staves.
3. **Reference Isolation**: Ensure candidate recognition runs without receiving reference `.gp` files.

## Validation Commands

1. Run `agent_verify.py`:
   ```bash
   python3 scripts/agent_verify.py
   ```
2. Run TAB digit recognition tests:
   ```bash
   python3 -m pytest tests/test_tab_digit_recognition.py
   ```
3. Run private smoke runner:
   ```bash
   python3 scripts/private_e2e_smoke.py --pdf fixtures/private/Lesson-5.pdf
   ```

## Deliverables

- Branch `agy/crp-06-dual-modality-tab-recognition` pushed to `origin`.
- Only `src/score2gp/pdf.py` and `tests/test_tab_digit_recognition.py` created/modified.
- Pull Request opened on GitHub.
