# Active Task: Candidate-to-Measure Architecture Research

## Repository
tticom/score2gp

## Current Governance State
Last completed governance PR: PR #326 (measure-grid diagnostic merged)
Architect research: Authorised
Reviewer architecture verification: Required next
Developer implementation: Blocked
Product feature implementation: Blocked

## Authorised Architect Task
Perform bounded architecture research to determine whether detected notation candidates can be assigned into measure regions using the merged structural skeleton and measure-grid diagnostics.

**Hypothesis:**
Structural skeleton and measure-grid diagnostics provide sufficient geometric boundaries to support candidate-to-measure spatial assignment without relying on semantic notation recognition.

**Allowed Fixtures:**
- `generated_standard_staff_quarter_note.pdf`
- `generated_standard_staff_multi_staff.pdf`
- `generated_standard_staff_ledger_lines.pdf`
- `generated_paired_notation_tab_system_double_barline.pdf`

**Metric & Threshold:**
- Determine if candidates fall reliably into bounded measure regions geometrically.
- Success threshold: Pass/fail verdict on the viability of candidate-to-measure assignment for the given fixtures.

**Stop/Pivot Triggers:**
- Stop if candidate-to-measure assignment requires semantic notation recognition, rhythm inference, or score interpretation.
- Pivot if the current diagnostic bounds cannot safely isolate candidates.

## Active Blocker
Score2GP now has structural measure-grid evidence, but it does not yet have verified evidence that detected notation candidates can be assigned into measure regions safely enough to support recognition work. Can structural skeleton + measure-grid diagnostics support candidate-to-measure spatial assignment on approved fixtures without relying on semantic recognition?

## Required Next Stages
1. Architect research
2. Reviewer architecture verification
3. Developer implementation (only if architecture verification approves)
4. Reviewer implementation conformance review (only if implemented)
5. PR readiness review

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
- Developer implementation.
