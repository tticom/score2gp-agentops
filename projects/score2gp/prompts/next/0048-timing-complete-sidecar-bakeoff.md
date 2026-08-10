# 0048 — Sidecar Bake-Off & 4/4 Triplet Discriminator (CRP-05)

Status: MERGED

## Objective

Implement `tests/test_sidecar_bakeoff.py` and refine `src/score2gp/notation_omr/timeline.py` to evaluate sidecar OMR options (Audiveris sidecar vs Score2GP internal topology-first timing adapter) against `Lesson-6.pdf` 4/4 triplets with balanced measure capacities, selecting Outcome A or B under strict reference isolation.

## Start

1. Branch from `origin/main` in the `score2gp` product repository.
2. Confirm the branch name is `agy/crp-05-sidecar-bake-off`.
3. Read `docs/design/2026-08-09-conversion-recovery-architecture.md` and `docs/design/2026-08-09-conversion-module-migration-map.md`.
4. Verify standard tests pass.

## Implementation Scope & Seam Contract

Modify `src/score2gp/notation_omr/timeline.py` and create `tests/test_sidecar_bakeoff.py`:
1. **4/4 Triplet Discriminator**: Test `Lesson-6.pdf` multi-voice measures containing 4/4 triplets to verify duration assignment does not drop triplet notes or corrupt measure capacity.
2. **Outcome Selection**: Evaluate Audiveris MusicXML output vs internal Score2GP timeline assembly; select Outcome A (internal topology-first timing adapter) if Audiveris drops triplet timing.
3. **Reference Isolation**: Ensure sidecar evaluation executes without receiving reference `.gp` files.

## Validation Commands

1. Run `agent_verify.py`:
   ```bash
   python3 scripts/agent_verify.py
   ```
2. Run bake-off tests:
   ```bash
   python3 -m pytest tests/test_sidecar_bakeoff.py
   ```

## Deliverables

- Branch `agy/crp-05-sidecar-bake-off` pushed to `origin`.
- Only `src/score2gp/notation_omr/timeline.py` and `tests/test_sidecar_bakeoff.py` created/modified.
- Pull Request opened on GitHub.
