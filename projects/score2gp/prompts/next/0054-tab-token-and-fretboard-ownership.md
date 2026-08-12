# 0054 — Biomechanical Fretboard Position Optimizer & TAB Token Ownership (CRP-11)

Status: APPROVED

## Objective

Implement `tests/test_tab_token_and_fretboard_ownership.py` and refine `src/score2gp/notation_omr/position_optimizer.py` and `pipeline.py` to recognize context-aware fret tokens and string ownership, separating observed visual TAB digits from inferred fretboard positions using biomechanical hand-position heuristics.

## Start

1. Branch from `origin/main` in the `score2gp` product repository.
2. Confirm the branch name is `agy/crp-11-tab-token-and-fretboard-ownership`.
3. Read `docs/design/2026-08-09-conversion-recovery-architecture.md` and `docs/design/2026-08-09-conversion-module-migration-map.md`.
4. Verify standard tests pass.

## Implementation Scope & Seam Contract

Modify `src/score2gp/notation_omr/position_optimizer.py`, `src/score2gp/notation_omr/pipeline.py`, and create `tests/test_tab_token_and_fretboard_ownership.py`:
1. **Fretboard Position Optimization**: Implement context-aware fret token and string ownership solver for TAB candidates.
2. **Observed vs. Inferred Distinction**: Distinguish explicitly observed visual TAB fret numbers from inferred fretboard assignments without synthetic string/fret guessing.
3. **Reference Isolation**: Ensure fretboard position optimization operates without receiving reference `.gp` files.

## Validation Commands

1. Run `agent_verify.py`:
   ```bash
   python3 scripts/agent_verify.py
   ```
2. Run TAB token and fretboard ownership tests:
   ```bash
   python3 -m pytest tests/test_tab_token_and_fretboard_ownership.py
   ```
3. Run private smoke test on `Lesson-5.pdf`:
   ```bash
   python3 scripts/private_e2e_smoke.py --pdf fixtures/private/Lesson-5.pdf
   ```

## Deliverables

- Branch `agy/crp-11-tab-token-and-fretboard-ownership` pushed to `origin`.
- Only `src/score2gp/notation_omr/position_optimizer.py`, `src/score2gp/notation_omr/pipeline.py`, and `tests/test_tab_token_and_fretboard_ownership.py` created/modified.
- Pull Request opened on GitHub.
