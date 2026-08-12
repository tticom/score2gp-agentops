# 0053 — Musical Timeline Replacement (CRP-10)

Status: APPROVED

## Objective

Implement `tests/test_musical_timeline_replacement.py` and refine `src/score2gp/notation_omr/timeline.py` and `pipeline.py` to replace unbounded single-measure aggregation with topologically locked bar timelines, enforcing metre, tuplets, voices, rests, onsets, durations, and bar capacity invariants under a single owner of timing truth.

## Start

1. Branch from `origin/main` in the `score2gp` product repository.
2. Confirm the branch name is `agy/crp-10-musical-timeline-replacement`.
3. Read `docs/design/2026-08-09-conversion-recovery-architecture.md` and `docs/design/2026-08-09-conversion-module-migration-map.md`.
4. Verify standard tests pass.

## Implementation Scope & Seam Contract

Modify `src/score2gp/notation_omr/timeline.py`, `src/score2gp/notation_omr/pipeline.py`, and create `tests/test_musical_timeline_replacement.py`:
1. **Unified Owner of Timing Truth**: Replace unbounded single-measure aggregation with topologically locked bar timelines.
2. **Bar Capacity & Triplet Preservation**: Enforce metre, tuplets, voices, rests, onsets, durations, and bar capacity invariants (specifically 4/4 triplet timing on `Lesson-6.pdf`) without scaling, truncation, padding, deduplication, or auto-partition hacks.
3. **Reference Isolation**: Ensure musical timeline reconstruction operates without receiving reference `.gp` files.

## Validation Commands

1. Run `agent_verify.py`:
   ```bash
   python3 scripts/agent_verify.py
   ```
2. Run musical timeline replacement tests:
   ```bash
   python3 -m pytest tests/test_musical_timeline_replacement.py
   ```
3. Run private smoke test on `Lesson-6.pdf`:
   ```bash
   python3 scripts/private_e2e_smoke.py --pdf fixtures/private/Lesson-6.pdf
   ```

## Deliverables

- Branch `agy/crp-10-musical-timeline-replacement` pushed to `origin`.
- Only `src/score2gp/notation_omr/timeline.py`, `src/score2gp/notation_omr/pipeline.py`, and `tests/test_musical_timeline_replacement.py` created/modified.
- Pull Request opened on GitHub.
