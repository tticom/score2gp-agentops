# 0052 — Paired-Staff Evidence Fusion (CRP-09)

Status: MERGED

## Objective

Implement `tests/test_paired_staff_evidence_fusion.py` and refine `src/score2gp/notation_omr/evidence.py` and `pipeline.py` to associate notation, TAB, bars, and techniques by document topology (`SystemTopology` / `PairedStaffTopology`) rather than global measure-index coincidence.

## Start

1. Branch from `origin/main` in the `score2gp` product repository.
2. Confirm the branch name is `agy/crp-09-paired-staff-evidence-fusion`.
3. Read `docs/design/2026-08-09-conversion-recovery-architecture.md` and `docs/design/2026-08-09-conversion-module-migration-map.md`.
4. Verify standard tests pass.

## Implementation Scope & Seam Contract

Modify `src/score2gp/notation_omr/evidence.py`, `src/score2gp/notation_omr/pipeline.py`, and create `tests/test_paired_staff_evidence_fusion.py`:
1. **Paired-Staff Topology Fusion**: Fuse notation and TAB evidence using `SystemTopology` staff pairs, proving one-to-one ownership or explicit ambiguity across pages and systems.
2. **Prevent Cross-System Snapping**: Strictly scope candidate alignment within system boundaries.
3. **Reference Isolation**: Ensure paired-staff evidence fusion operates without receiving reference `.gp` files.

## Validation Commands

1. Run `agent_verify.py`:
   ```bash
   python3 scripts/agent_verify.py
   ```
2. Run paired-staff evidence fusion tests:
   ```bash
   python3 -m pytest tests/test_paired_staff_evidence_fusion.py
   ```

## Deliverables

- Branch `agy/crp-09-paired-staff-evidence-fusion` pushed to `origin`.
- Only `src/score2gp/notation_omr/evidence.py`, `src/score2gp/notation_omr/pipeline.py`, and `tests/test_paired_staff_evidence_fusion.py` created/modified.
- Pull Request opened on GitHub.
