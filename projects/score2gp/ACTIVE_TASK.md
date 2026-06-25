# Active Task: Measure-Grid Diagnostic Implementation

## Repository
tticom/score2gp

## Current Governance State
Last completed governance PR: PR #211
Architect research: Complete (Outcome B selected: non-raster deterministic vector alternative viable)
Reviewer architecture verification: Complete
Verdict: approve architecture
Developer implementation authorised: Yes, strictly bounded.
Product feature implementation authorised: No

## Authorised Developer Task
Implement a read-only measure-grid diagnostic from confirmed internal barlines.
- Consume confirmed internal barlines from the structural-skeleton diagnostic.
- Produce spatial measure-region bounds per staff/system.
- Report exact region count and start/end X coordinate bounds.
- Explicitly fail if grid resolution requires notation semantics.

**Allowed Fixtures:**
- `generated_standard_staff_quarter_note.pdf`
- `generated_standard_staff_multi_staff.pdf`
- `generated_standard_staff_ledger_lines.pdf`

**Metric & Threshold:**
- Exact measure-region count per staff/system; start/end X bound correctness; zero false measure grids; explicit failure for semantic-dependent cases.
- Threshold: 100% boundary isolation on the approved fixture set; zero false grids.

**Stop/Pivot Triggers:**
- Stop if grid resolution requires notation semantics.
- Return to Architect if confirmed internal barlines are insufficient to define spatial regions.
- Stop if implementation would require ScoreIR, GP export, duration inference, voice mapping, or semantic notation interpretation.

## Active Blocker
Developer implementation of the bounded measure-grid diagnostic.

## Required Next Stages
1. Developer implementation
2. Reviewer implementation conformance review
3. PR readiness review

## Explicit Non-Authorisations
These remain explicitly **blocked**:
- standard-notation conversion;
- note/rest semantic recognition;
- rhythm/duration inference;
- polyphony;
- voice mapping;
- clef/key/time interpretation;
- ScoreIR generation;
- GP export;
- tab-only timing changes;
- private fixture usage;
- generated artifact commits.
