# Active Task

**Task**: OMR/CV Architecture Research Spike for Whole-Note Recognition
**Authorised Role**: Architect
**Repository**: `tticom/score2gp-agentops`

## 1. Baseline
- Product PR #332 merged, ingesting the Supervisor-approved Mutopia A4 safe natural public fixture (`mutopia-bwv-anh-120-minuet-a-minor-a4.pdf`).
- Product PR #333 merged (commit `b38c0acc9c284379dcd0f82316db08c3fc6211ec`).
- Geometric `x_aligned_cluster_candidate` path is explicitly disproven for whole-note detection.
- Basic connected-component raster heuristics are explicitly disproven for whole-note detection due to overlapping metrics with text and expression markings (Outcome C).
- Whole-note rule-based Developer implementation is formally blocked.

## 2. Active Blocker
Rule-based pixel heuristics and PDF primitives cannot distinguish musical whole notes from identically shaped text elements (e.g. '0', 'o', 'p', 'e', '4'). Whole-note implementation is blocked until an Optical Music Recognition (OMR) or semantic symbol classification pathway is proven viable.

## 3. Authorised Scope
The Architect is authorised to evaluate OMR/CV options and produce measurable feasibility evidence.

The Architect must compare at least these options (if feasible without external downloads):
- Existing OMR libraries or models already suitable for local evaluation.
- Symbol-classification model integration feasibility.
- Template matching (only as a rejected or limited baseline, unless strongly evidenced).
- Dataset/training requirements (if no off-the-shelf model can be evaluated safely).
- Integration constraints for Score2GP.
- Privacy, licensing, dependency, latency, maintainability, and testability risks.

**Developer implementation is strictly BLOCKED.**

## 4. Non-Goals
- Do not authorise Developer implementation.
- Do not implement product whole-note recognition.
- Do not implement semantic pitch, clef, or rhythm parsing.
- Do not change ScoreIR semantics or GP export.
- Do not mandate training a model in this task unless research proves it is the correct route and defines data requirements.

## 5. Required Evidence
- Measurable feasibility criteria for the proposed OMR/CV solution.
- Assessment of dependency constraints and execution latency.
- Clearly separated facts, inferences, and unknown risks.
- A defined narrow path forward, or a formal recommendation to abandon the feature.

## 6. Stop Conditions
- Stop if any product file in `tticom/score2gp` requires modification.
- Stop if external downloads (models/binaries) are required but violate repository governance.
- Stop if the research attempts to implement a complete production model pipeline.

## 7. Next Required Review
Reviewer architecture verification of the Architect's OMR/CV feasibility report.
