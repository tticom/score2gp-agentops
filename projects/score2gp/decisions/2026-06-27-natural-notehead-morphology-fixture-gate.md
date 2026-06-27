# 2026-06-27 Architect Evaluation: Natural Notehead Morphology Fixture Gate

## Baseline Context

- **Product PR**: #330 (Merge Commit `dc511e6f663c08c180e1beae473c5b0d31f31bc4`)
- **Governance PR**: #224 (Merge Commit `b78c9c306d41ee5b045ae7bb308807be5555a787`)
- **Governance PR**: #225 (Merge Commit `c46dba9a53d95b4b2ebc6cc950ed1932cc24e4eb`)
- **Governance PR**: #226 (Merge Commit `c963a67b44454554d6e621654a0fa876c6692733`)
- **Previous Outcome**: Horizontal projection morphology method improved notehead centers for synthetic half/whole notes, but was blocked from product implementation because synthetic quarter-note fixtures remained ambiguous (66.6% resolution rate).
- **Active Task**: Perform a fixture-safety-gated evaluation to determine if the method is viable on safe natural public score material, or if the project must stop/pivot.

## Process-gate recovery

The fixture-safety gate evidence in this PR is content-valid but was produced before the prior Reviewer architecture verification/authorisation state was fully recorded. No product code, product tests, fixture binaries, private artifacts, diagnostic execution, semantic inference, or implementation changes were made. This PR does not authorise downstream work. The governance recovery is to require Reviewer architecture verification re-review of this PR before any PR readiness review, merge decision, fixture discovery/approval task, diagnostic execution, or implementation task may proceed.

## Fixture-Safety Gate Assessment

An inventory check of the product repository (`tticom/score2gp`) was performed to identify any eligible committed safe natural public fixtures.

- `fixtures/public/Derek Trucks BB King.pdf`: Rejected (Unsafe). No provenance or license available in the repository. Appears to be copyrighted transcription material.
- `fixtures/public/Just-Practice-Like-THIS-Every-Day.pdf`: Rejected (Unsafe). No provenance or license available in the repository.
- `fixtures/public/Melodic Soloing Masterclass.pdf`: Rejected (Unsafe). No provenance or license available in the repository.
- All PDF files in `tests/fixtures/pdf/`: Rejected (Synthetic/Generated). These are generated synthetic test files created by scripts like `make_standard_staff_diagnostics_pdfs.py` and lack natural musical typography anomalies (which was the exact issue identified in PR #226).

**Result**: NO eligible committed safe natural public fixtures exist in the repository.

## Diagnostic Method & Metrics

**Not run because no eligible committed safe fixture existed.**

Consequently, no product diagnostics were executed and no product test files or scripts were modified. The morphology method remains unverified on natural material.

## Safe Fixture Discovery Candidate

Since no eligible fixtures exist, the project must identify a candidate fixture for Supervisor approval before proceeding.

**Candidate Source**: Mutopia Project (e.g., a simple classical piece like a Bach Minuet or Sor study) or an explicit Creative Commons / Public Domain score from IMSLP.
**Why Suitable**: These sources explicitly mark scores as Public Domain or CC-BY. They represent natural musical engraving with stems, distinct notehead ovals, and natural layout spacing.
**Risks**: Even public domain scores might use obscure fonts that deviate from the standard geometric models.
**Approval Requirement**: The Reviewer and Supervisor must explicitly approve the candidate URL, license, and provenance before the binary PDF is downloaded into the `tticom/score2gp` repository.

## Analysis

### Facts
- The product repository contains three recently added natural PDF fixtures (`Derek Trucks BB King.pdf`, etc.) but none have accompanying provenance or license metadata.
- Using these unauthorized PDFs would violate the strict project safety rules against using arbitrary or copyrighted material.
- The `tests/fixtures/pdf/` folder contains only synthetic or generated fixtures, which are insufficient to resolve the quarter-note morphology ambiguity identified in PR #226.
- Because the fixture-safety gate failed, diagnostic execution was safely aborted.

### Inferences
- The project's strict artifact hygiene rules functioned correctly to block the execution of diagnostic code on unauthorized copyrighted material.
- The notehead center morphology method cannot be proven or disproven without first sourcing a demonstrably safe natural fixture.

### Hypotheses
- A public domain score from Mutopia or IMSLP will possess the natural notehead typography (ovals with attached stems) required to test the horizontal projection density method without violating licensing constraints.

### Unknowns
- Whether the morphology method will actually achieve the >70% resolution threshold on natural fixtures, once a safe fixture is approved and tested.

## Architect Outcome

**Outcome B — Useful but insufficient / fixture gate still needed**

## Outcome Justification

The safety gate correctly identified that the required diagnostic cannot currently be run because no committed safe natural public fixture exists in the repository. Although the morphology approach is promising, it remains entirely blocked. Outcome B is appropriate because the missing evidence is known, the reason for the blockage is documented, and a safe fixture approval path (seeking a Public Domain candidate) is clearly identified.

## Next Recommended Task

**Task**: Reviewer architecture verification of the Architect's fixture-safety gate assessment, confirming the rejection of unauthorized fixtures and authorizing a Supervisor-gated fixture discovery task to safely obtain a public domain natural score.

## Stop / Pivot Conditions

- Stop if no safe, explicitly licensed natural public score can be sourced and approved by the Supervisor.
- Pivot to Outcome C if the Supervisor explicitly rejects the addition of any new binary fixtures to the repository.

## Explicitly Still Blocked

- semantic pitch implementation: yes
- G-clef inference implementation: yes
- rhythm implementation: yes
- whole-note recognition implementation: yes
- ScoreIR semantic changes: yes
- GP export changes: yes
- ML/OCR/model training: yes
- private fixture use: yes
- arbitrary public PDF downloads: yes
- unapproved binary fixture commits: yes
