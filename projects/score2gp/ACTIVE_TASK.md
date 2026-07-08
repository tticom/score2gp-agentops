# Active Task

**Task**: Req-114 / Task 46: Quarter rest extraction based on stable geometry
**Authorised Role**: Architect
**Repository**: `tticom/score2gp`

## Status
APPROVED

## Executable Task
Yes

## Completion Evidence
Architect must research and propose how to cleanly identify quarter rests (crotchet rests) from existing stable geometry candidates without inferring pitch or full rhythmic context.

## 1. Baseline
- The semantic boundary for left-margin clefs has been established (Req-111, Req-112, Req-113).
- We now want to look into the staff body primitives to identify standalone symbols, starting with the quarter rest which has distinct vertical characteristics.

## 2. Context
Quarter rests are typically tall vertical-stroke-like or squiggly curve-like symbols sitting in the middle of the staff body. Because they do not rely on a notehead or stem, they are a good starting point for semantic extraction in the staff body. We need to identify if current diagnostics/primitives (e.g. `x_aligned_cluster_candidates` or `vertical_stroke` or `curve`) are sufficient to build a robust quarter rest heuristic.

## 3. Goal
Produce an Architect research proposal (`docs/testing/quarter-rest-recognition.md`) determining the safest, most deterministic method to classify quarter rest candidates from the body geometry.

## 4. Non-goals
- Do not implement the classification yet.
- Do not modify existing logic.
- Do not build inference for other rests or notes.

## 5. Required Output & Outcome
A product PR with the `quarter-rest-recognition.md` research proposal, recommending a specific implementation path for the Developer to take in Req-114.

## 6. Next Steps
- After Architect PR opens, run Reviewer architecture verification before any Developer implementation is authorised.
