# Epic C First Pass Appraisal

**Date**: 2026-07-08
**Reviewer**: Autonomous Agent
**Scope**: Epic C (Semantic Boundary Definition & Core Interpretation)

## 1. What Landed
The first iteration of Epic C established strict, fail-closed boundaries for semantic interpretation based purely on geometric diagnostics, successfully completing:
- **Req-111 / Req-112**: Established the `evaluate_logical_clef_gate` on the left margin, aggressively failing closed on ambiguous geometries.
- **Req-113**: Integrated `classify_logical_clef_candidate` using robust height and width proportions to safely identify Treble Clefs without OCR.
- **Req-114**: Expanded to the staff body by extracting `QuarterRestCandidate`s from isolated `XAlignedPrimitiveClusterCandidate`s using height, aspect ratio, and centering heuristics.

## 2. What Tests Prove
- **Isolation Safety**: Tests explicitly prove that clusters containing multiple primitives or failing strict bounding box ratios are ignored/failed-closed.
- **Backwards Compatibility**: The existing 895 test cases (including ScoreIR generation and public synthetic fixture snapshots) continue to pass perfectly. 
- **Privacy Invariants**: The `artifact_audit.py` script confirms no semantic dumps or private fixtures leaked into the workspace.

## 3. What Remains Unproven
- **Real-World Coverage**: The heuristics rely on synthetic configurations. They have not been audited against a large corpus of real-world score rendering engines.
- **Other Rest Durations**: Half rests, whole rests, and flag-based rests (eighth, sixteenth) are completely unhandled.
- **Overlapping/Polyphonic Clusters**: Quarter rests are only recognised if completely isolated (`primitive_count == 1`). Real scores frequently contain rests sharing vertical space with notes in other voices.
- **ScoreIR Translation**: These candidates are currently diagnostic/analytical objects. They are not injected into the final ScoreIR timeline.

## 4. Risks of Overclaiming
It is dangerous to claim we have "solved" rest extraction or clef extraction. We have merely built extraction sieves for the most pristine, isolated synthetic examples of treble clefs and quarter rests. Rushing to infer pitch or rhythmic duration from these isolated candidates would immediately violate the "no guessing" mandate, as we lack the necessary structural context (stems, noteheads, barlines, key signatures) to make rhythmic inferences.

## 5. Recommended Next Safe Task Series
Before attempting any rhythm or pitch work (Req-115/Req-116), we must harden the observability of these semantic candidates:
1. **Semantic Candidate Snapshotting (Req-119)**: Create deterministic JSON snapshot tests for `QuarterRestCandidate` and `LogicalClefCandidate` outputs, mirroring the safety nets we built for primitive geometry in Req-105.
2. **Semantic Extraction CLI / Reporting (Req-120)**: Expose semantic candidate extraction through the diagnostics CLI to allow maintainer audits.
3. **Fail-Closed Coverage Expansion (Req-121)**: Create synthetic tests that explicitly introduce whole rests, half rests, and polyphonic collisions to prove that the quarter rest heuristic safely ignores them.
4. **No-ScoreIR Leakage Gate (Req-122)**: Implement a strict test proving that the presence of these semantic candidates does *not* alter the legacy ScoreIR output, preserving the isolation boundary until mapping is formally authorised.
