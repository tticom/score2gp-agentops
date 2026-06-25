# Decision: Record PR #214 Architecture Approval and Authorise Candidate Staff-Identity Diagnostic Evidence

## Context
Architecture PR #214 has merged and approved Outcome B regarding candidate-to-measure spatial assignment feasibility.

**Outcome B summary:**
- Measure-grid diagnostics provide excellent bounded horizontal regions.
- Notation candidate geometry exists (`bbox`, `width`, `height`, `aspect_ratio`, `stem_bbox`).
- Candidate-to-measure assignment remains **blocked** because notation candidate diagnostics currently lack explicit `page_index`, `system_index`, or `staff_index`.
- Naive Y-overlap against tight 5-line `staff_bounds` is unsafe due to ledger-line notes and the potential for cross-staff ambiguity in multi-staff systems.
- The next valid increment is to preserve or expose staff/system identity on notation candidate diagnostics.

## Baselines
- **Product PR #326**: `https://github.com/tticom/score2gp/pull/326` (Merge Commit: `7565e751e0dea624a209aeb4233373338296262a`)
- **Governance PR #213**: `https://github.com/tticom/score2gp-agentops/pull/213` (Merge Commit: `efc3a7ace72ea7456b7b45c25a6735ee3119c61c`)
- **Architecture PR #214**: `https://github.com/tticom/score2gp-agentops/pull/214` (Merge Commit: `c3b5d3bfad5d1a5c01f4819dd7730b3127726cfc`)

## Decision
We authorise a narrow Developer diagnostic-evidence task to preserve or expose staff/system identity on notation candidates. Full candidate-to-measure assignment remains explicitly blocked until this diagnostic evidence is secured and verified.

## Authorised Developer Task
**Task:** Preserve or expose `page_index`, `system_index`, and `staff_index` (or equivalent staff/system identity) on notation candidate diagnostics.

**Constraints:**
- The output must remain read-only diagnostic evidence.
- Candidate geometry must remain available, including existing `bbox` and stem geometry where present.
- Existing diagnostic consumers must not lose existing fields unless explicitly justified and covered by tests.
- The task must prove that candidates can be associated with the staff/system where they were extracted, without relying on naive post-hoc Y-overlap against tight staff bounds.
- The task must be fixture-tested against multi-staff and ledger-line cases.

**Explicitly Forbidden:**
- Assigning candidates to measure regions.
- Changing ScoreIR or GP export.
- Changing rhythm/note recognition behaviour.
- Adding semantic interpretation (duration inference, voice mapping, etc.).
- OCR, ML or training, MusicXML, or tab-only conversion changes.
- Using private fixtures or committing generated artifacts.

## Acceptance Criteria
- Candidate diagnostics expose or preserve staff/system identity.
- Candidate diagnostics still expose candidate geometry.
- Approved public fixtures show staff/system identity is present for candidate outputs.
- Multi-staff fixture proves candidates are not ambiguous between staves.
- Ledger-line fixture proves staff identity does not rely on naive overlap with tight 5-line `staff_bounds`.
- Existing measure-grid diagnostics remain unchanged unless a change is explicitly required and tested.
- Existing tests continue to pass.
- No product behaviour changes outside read-only diagnostics.

## Required Next Stages
1. Developer diagnostic-evidence implementation.
2. Reviewer implementation conformance review.
3. PR readiness review.
