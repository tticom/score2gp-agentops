# 0051 — Recognition Adapter Seam (CRP-08)

Status: MERGED

## Objective

Implement `tests/test_recognition_adapters.py` and refine `src/score2gp/notation_omr/evidence.py` to provide typed text, vector, and raster candidate adapters (`CandidateAdapter`, `EvidenceRecord`, `SourceModality`) that retain source coordinates, modality, confidence, absence, ambiguity, and conflict behind one interface.

## Start

1. Branch from `origin/main` in the `score2gp` product repository.
2. Confirm the branch name is `agy/crp-08-recognition-adapter-seam`.
3. Read `docs/design/2026-08-09-conversion-recovery-architecture.md` and `docs/design/2026-08-09-conversion-module-migration-map.md`.
4. Verify standard tests pass.

## Implementation Scope & Seam Contract

Modify `src/score2gp/notation_omr/evidence.py` and create `tests/test_recognition_adapters.py`:
1. **Typed Evidence Adapters**: Implement `SourceModality` enum (`TEXT`, `VECTOR`, `RASTER`, `HYBRID`), `EvidenceRecord`, and `CandidateAdapter`.
2. **Coordinate & Modality Preservation**: Ensure wrapped candidates preserve exact bounding boxes, modality, confidence, absence, ambiguity, and conflict metadata without assigning downstream musical semantics.
3. **Reference Isolation**: Ensure candidate evidence wrapping operates without receiving reference `.gp` files.

## Validation Commands

1. Run `agent_verify.py`:
   ```bash
   python3 scripts/agent_verify.py
   ```
2. Run recognition adapter tests:
   ```bash
   python3 -m pytest tests/test_recognition_adapters.py
   ```

## Deliverables

- Branch `agy/crp-08-recognition-adapter-seam` pushed to `origin`.
- Only `src/score2gp/notation_omr/evidence.py` and `tests/test_recognition_adapters.py` created/modified.
- Pull Request opened on GitHub.
