# Supervisor Decision — Authorise 8th/16th-Note Architect Research

**Date**: 2026-07-06  
**Role**: Supervisor  
**Status**: Approved / Active Task  

## 1. Context & Rationale
With the whole-note E2E pipeline proof-of-concept completed and parked, the next logical milestone is the recognition and rhythm semantics of 8th and 16th notes. These note values are common in real scores and represent a significant jump in complexity, introducing stems, flags, beams, notehead/stem relationships, duration classification, onset mapping, and Guitar Pro rhythmic grouping semantics.

Because this represents a completely new recognition strategy and product-behaviour area, it is classified as **Tier A (Full Loop)**. We do not authorise Developer implementation or diagnostic changes at this stage. Instead, the Architect must perform research to establish a viable technical approach before any coding begins.

## 2. Baselines
- **Product Merge Baseline**: Product PR #336 squash-merged at `cae6a416076e66f6b84940ad0cbf3061beb241d9`.
- **Governance Merge Baseline**: Governance PR #238 squash-merged at `96397d845b924fb27b12753940ccfec7251ebb09`.
- **Active State**: Parked whole-note capability; active workflow loop tiers (Tier A/B) and preserved `ACTIVE_TASK.md` authorisation.

## 3. Authorised Next Task
Exactly one next task is authorised:
- **Title**: Architect research — 8th/16th-note recognition and rhythm-semantics strategy
- **Role**: Architect
- **Loop Tier**: Tier A (Full Loop)
- **Developer Implementation**: Not authorised
- **Diagnostic Implementation**: Not authorised except read-only repository inspection and non-committed local analysis of existing tracked public fixtures/files. No generated artifacts may be committed to git.

## 4. Required Architect Output
The Architect must produce a self-contained research report under `projects/score2gp/research/2026-07-06-8th-16th-note-recognition-strategy.md` that strictly separates:
- Facts (direct evidence in existing code, tests, fixtures, or third-party tools);
- Inferences (conclusions drawn from facts);
- Hypotheses (testable propositions for later steps);
- Unknowns (identified gaps in knowledge).

The Architect must investigate current product capabilities and gaps for:
- notehead detection (specifically 8th/16th noteheads);
- staff association (how pitches are resolved);
- stem detection (orientation, length, and coordinate extraction);
- flag detection (for isolated 8th/16th notes);
- beam detection (for grouped 8th/16th notes);
- stem-to-notehead association;
- beamed-group segmentation (identifying measure sub-beats);
- duration classification (whole, half, quarter, 8th, 16th);
- onset/duration tick mapping (assigning start ticks and durations in ScoreIR);
- rhythm grouping (GP track beam grouping constraints);
- Guitar Pro export implications;
- current test/fixture coverage and gaps;
- artifact constraints.

The Architect must conclude the report by selecting exactly one of:
- **Outcome A (Raster path viable)**: A raster/product implementation path for 8th/16th-note recognition and rhythm semantics is viable with current repository architecture. Provide the smallest implementable next Developer task, exact files likely affected, fixture requirements, validation strategy, acceptance criteria, and stop conditions.
- **Outcome B (Alternative path viable)**: A direct raster/product path is not viable, but another bounded approach is viable. Provide the alternate approach, exact evidence, smallest implementable next Developer task, fixture requirements, validation strategy, acceptance criteria, and stop conditions.
- **Outcome C (No viable path)**: No viable implementation path is currently justified. No Developer work is authorised. Provide the specific blocker, missing evidence, and the smallest next diagnostic/research question that would change the decision.

## 5. Research Constraints
- **Private Scores**: Forbidden.
- **Copyrighted Scores**: Forbidden.
- **New Generated Files**: No new generated PDFs, GP files, screenshots, logs, or dumps may be committed to the git repository.
- **Speculative Claims**: Forbidden. Capabilties must be proven by existing repo evidence.
- **Fixture Strategy**: Propose fixture strategy (e.g. PDF, JSON coordinate, MusicXML), but do not create or commit any files.

## 6. Stop and Pivot Conditions
- The Architect must stop and return to Supervisor if the task requires private PDFs or new generated artifacts.
- The Architect must stop if a single viable outcome (A, B, or C) cannot be justified from the evidence.
