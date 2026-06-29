# Active Task

**Task**: Controlled Mutopia A4 Diagnostic Rerun / Validation
**Authorised Role**: Governance Implementer / Developer (Diagnostic)
**Repository**: `tticom/score2gp-agentops`

## 1. Baseline
- Supervisor Outcome A fixture-ingestion approval decision record (`projects/score2gp/decisions/2026-06-29-supervisor-mutopia-a4-fixture-ingestion-approval.md`).

## 2. Approved Fixture
`https://www.mutopiaproject.org/ftp/BachJS/BWVAnh120/BWV-120/BWV-120-a4.pdf`
(Exact pinned A4 URL only)

## 3. Authorised Scope
- Diagnostic purpose: Assess whole-note heuristics and false positives against the approved fixture.
- Execute a controlled diagnostic rerun/validation using the precise fixture URL.

## 4. Required Diagnostic Contract
- Precise fixture: `https://www.mutopiaproject.org/ftp/BachJS/BWVAnh120/BWV-120/BWV-120-a4.pdf`
- Command: To be defined by the next diagnostic implementer.
- Metric/Output Evidence: Must be captured textually (no generated binaries, PDFs, or GP files attached).
- Pass/Fail Threshold: To be validated.
- Stop/Pivot Condition: To be evaluated upon completion.

## 5. Forbidden Scope
- **Product implementation:** Not authorised.
- **OMR/CV Architecture Research:** Not authorised.
- **Letter variants:** Not authorised.
- **Private/local artifacts:** Not authorised.
- **Unpinned URLs:** Not authorised.

## 6. Stop Conditions
- Stop if the task attempts to download, commit, or attach the PDF or any other binary/artifact file.
- Stop if scope expands beyond the approved A4 fixture.
- Stop if product changes are proposed.

## 7. Next Required Review
Diagnostic evidence review or PR readiness review, depending on whether a PR is opened for the diagnostic.
