# Active Task

**Task**: Req-113 / Task 42: Logical clef recognition candidate integration
**Authorised Role**: Architect
**Repository**: `tticom/score2gp`

## Status
APPROVED

## Executable Task
Yes

## Completion Evidence
Architect must research and propose how the `SemanticGateResult` (specifically a discovered logical clef candidate) should be classified into a concrete clef (Treble, Bass, etc.) using available heuristics or dependencies. 

## 1. Baseline
- Req-112 semantic boundary validation gate was implemented in product PR #348.
- Governance Reviewer approved the implementation in PR #264.
- `evaluate_logical_clef_gate` now correctly identifies a `logical_clef_candidate` but leaves its kind as `unknown` due to insufficient evidence.

## 2. Context
With the semantic boundary gate safely failing closed, the next step in Epic C is to actually recognize the specific clef glyph (Treble vs. Bass). The left margin candidate currently lacks text character context, meaning we must rely on font heuristics, bounding box aspect ratios, or introduce a new diagnostic capability to read the exact string.

## 3. Goal
Produce an Architect research proposal (`docs/testing/logical-clef-recognition.md`) determining the safest, most deterministic method to classify the clef kind.

## 4. Non-goals
- Do not modify existing logic.
- Do not implement the classification yet.
- Do not infer pitch or duration.

## 5. Required Output & Outcome
A product PR with the `logical-clef-recognition.md` research proposal, recommending a specific implementation path for the Developer to take in Req-113.

## 6. Next Steps
- After Architect PR opens, run Reviewer architecture verification before any Developer implementation is authorised.
