# Decision Record — Authorise Next Standard-Staff Recognition Capability Research

- **Status**: APPROVED
- **Role**: Supervisor
- **Date**: 2026-07-07

## 1. Context & Rationale
Following the merge of Governance PR #242 (merge commit: `373b6836b2121b82ad815753bcf78bc90e942137`), same-onset chord grouping for eighth/sixteenth note candidates is successfully implemented and recorded. 
However, standard-staff recognition remains limited to single-track sequential chords and relies on simple geometric heuristics. To determine the next logical milestone (e.g. OMR candidate extraction robustness, multi-staff/multi-voice timing), we require Architect research to evaluate the technical viability, gaps, and risks before any Developer implementation is authorised.

## 2. Baselines
- **Product Merge Baseline**: Product PR #337 squash-merged at `eae13541de67899ff9563a09f48ed747171dea6b`.
- **Governance Merge Baseline**: Governance PR #242 squash-merged at `373b6836b2121b82ad815753bcf78bc90e942137`.

## 3. Selected Next Path
Option A — Architect research:
- **Title**: Architect research — Next standard-staff recognition capability after same-onset chord grouping
- **Role**: Architect
- **Loop Tier**: Tier A (Full Loop)
- **Developer Work**: Not authorised.
- **Diagnostic Work**: Not authorised.

## 4. Required Architect Output
The Architect must produce a self-contained research report under `projects/score2gp/research/2026-07-07-next-recognition-capability-strategy.md` in the product repository, separating Facts, Inferences, Hypotheses, and Unknowns.
The report must investigate:
- OMR candidate extraction robustness (noteheads, stems, flags, beams, and their geometric association).
- Notation bridge mapping for multi-staff or multi-voice notation.
- GP export implications for multi-track output.
The report must recommend exactly one outcome (Outcome A, B, or C) with a detailed next task description and acceptance criteria.

## 5. Constraints & Stop Conditions
- No private/copyrighted PDFs may be processed.
- No new generated PDFs, GP files, screenshots, logs, or dumps may be committed to git.
- Stop if research requires private or copyrighted PDF fixtures.
- Stop if research requires committing generated files.

## 6. Required Next Review
Reviewer architecture verification.
