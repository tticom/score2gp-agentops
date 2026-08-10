# 0050 — Document Topology Module (CRP-07)

Status: MERGED

## Objective

Implement `tests/test_document_topology.py` and refine `src/score2gp/notation_omr/staff_geometry.py` to establish page, system, paired-staff, physical bar, and stable global measure identity behind a unified document topology interface.

## Start

1. Branch from `origin/main` in the `score2gp` product repository.
2. Confirm the branch name is `agy/crp-07-document-topology-module`.
3. Read `docs/design/2026-08-09-conversion-recovery-architecture.md` and `docs/design/2026-08-09-conversion-module-migration-map.md`.
4. Verify standard tests pass.

## Implementation Scope & Seam Contract

Modify `src/score2gp/notation_omr/staff_geometry.py` and create `tests/test_document_topology.py`:
1. **Document Topology Data Structures**: Add structured representations for page, system, paired-staff, physical bar, and global measure identity.
2. **Topology Extraction Invariants**: Ensure stems and connectors are not misclassified as barlines, and barlines do not cross-snap across disconnected systems.
3. **Reference Isolation**: Ensure document topology extraction operates without receiving reference `.gp` files.

## Validation Commands

1. Run `agent_verify.py`:
   ```bash
   python3 scripts/agent_verify.py
   ```
2. Run document topology tests:
   ```bash
   python3 -m pytest tests/test_document_topology.py
   ```

## Deliverables

- Branch `agy/crp-07-document-topology-module` pushed to `origin`.
- Only `src/score2gp/notation_omr/staff_geometry.py` and `tests/test_document_topology.py` created/modified.
- Pull Request opened on GitHub.
