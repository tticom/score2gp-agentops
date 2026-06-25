# Active Task: Candidate-to-Measure Architecture Research

## Repository
tticom/score2gp

## Current Governance State
Current product baseline: PR #326 in tticom/score2gp, merged with commit 7565e751e0dea624a209aeb4233373338296262a.
Architect research: Authorised
Reviewer architecture verification: Required next
Developer implementation: Blocked
Product feature implementation: Blocked

## Authorised Architect Task
Perform bounded architecture research to determine whether detected notation candidates can be assigned into measure regions using the merged structural skeleton and measure-grid diagnostics.

**Required Architect outcome:**
The Architect must choose exactly one:
- **Outcome A:** Candidate-to-measure spatial assignment is viable using the merged measure-grid and existing candidate geometry. Developer implementation may be proposed only after Reviewer architecture verification approves the approach.
- **Outcome B:** Measure-grid is useful but existing candidate evidence is insufficient. The Architect must define the smallest additional diagnostic evidence needed before implementation.
- **Outcome C:** Candidate-to-measure assignment is not viable with the current raster/vector diagnostics. No Developer work is authorised and a pivot is required.

**Required evidence:**
The Architect report must identify:
- Where notation candidate X-position or bounding-box evidence currently exists, if anywhere.
- Whether candidate X/bbox evidence can map deterministically to `MeasureGridDiagnostics` start/end X bounds.
- Whether staff identity is preserved strongly enough to prevent cross-staff assignment.
- How candidates near internal barlines would be handled.
- How double/repeat adjacent confirmed barlines affect assignment.
- Which files/functions were inspected.
- Which commands were run.
- What is fact, inference, hypothesis, and unknown.

**Allowed Fixtures:**
- `generated_standard_staff_quarter_note.pdf`
- `generated_standard_staff_multi_staff.pdf`
- `generated_standard_staff_ledger_lines.pdf`
- `generated_paired_notation_tab_system_double_barline.pdf`

**Outcome A threshold:**
Outcome A is allowed only if the Architect can show a concrete deterministic assignment rule using existing diagnostics and candidate geometry, with fixture-level evidence that candidates can be assigned to the expected staff and measure region without semantic recognition.

**Failure threshold:**
If candidate X/bbox evidence is absent, inconsistent, not linked to staff identity, or not recoverable without broad product changes, Outcome A is forbidden.

**Stop/pivot condition:**
If existing diagnostics cannot support candidate-to-measure assignment, the Architect must not recommend implementation. They must choose Outcome B or Outcome C.

## Active Blocker
Score2GP now has structural measure-grid evidence, but it does not yet have verified evidence that detected notation candidates can be assigned into measure regions safely enough to support recognition work. Can structural skeleton + measure-grid diagnostics support candidate-to-measure spatial assignment on approved fixtures without relying on semantic recognition?

## Required Next Stages
1. Architect research
2. Reviewer architecture verification
3. Developer implementation (only if architecture verification approves one concrete approach)
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
