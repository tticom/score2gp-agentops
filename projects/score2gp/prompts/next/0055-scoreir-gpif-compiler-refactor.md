# 0055 — Unified ScoreIR / GPIF Compiler Refactor & Binary Assembly Seam (CRP-12)

Status: MERGED

## Objective

Implement `tests/test_scoreir_gpif_compiler_refactor.py` and refine `src/score2gp/scoreir_compiler.py` and `src/score2gp/gpif_builder.py` to compile validated OMR evidence, timeline events, and fretboard positions into valid ScoreIR and GPIF representations, producing valid `.gp` binaries without unevidenced timing snapping or synthetic note generation.

## Start

1. Branch from `origin/main` in the `score2gp` product repository.
2. Confirm the branch name is `agy/crp-12-scoreir-gpif-compiler-refactor`.
3. Read `docs/design/2026-08-09-conversion-recovery-architecture.md` and `docs/design/2026-08-09-conversion-module-migration-map.md`.
4. Verify standard tests pass.

## Implementation Scope & Seam Contract

Modify `src/score2gp/scoreir_compiler.py`, `src/score2gp/gpif_builder.py`, and create `tests/test_scoreir_gpif_compiler_refactor.py`:
1. **ScoreIR & GPIF Compilation**: Compile `TopologicallyLockedBarTimeline` events and `FretTokenOwnership` positions into structured `ScoreIR` and `GPIF` models.
2. **Binary Assembly Seam**: Ensure compiled ScoreIR / GPIF models assemble cleanly into valid `.gp` binary structures.
3. **Reference Isolation**: Ensure compilation operates without receiving reference `.gp` files.

## Validation Commands

1. Run `agent_verify.py`:
   ```bash
   python3 scripts/agent_verify.py
   ```
2. Run ScoreIR and GPIF compiler tests:
   ```bash
   python3 -m pytest tests/test_scoreir_gpif_compiler_refactor.py
   ```
3. Run private smoke test on `Lesson-6.pdf`:
   ```bash
   python3 scripts/private_e2e_smoke.py --pdf fixtures/private/Lesson-6.pdf
   ```

## Deliverables

- Branch `agy/crp-12-scoreir-gpif-compiler-refactor` pushed to `origin`.
- Only `src/score2gp/scoreir_compiler.py`, `src/score2gp/gpif_builder.py`, and `tests/test_scoreir_gpif_compiler_refactor.py` created/modified.
- Pull Request opened on GitHub.
