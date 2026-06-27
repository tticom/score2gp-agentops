# Safe Natural Public Score Fixture Candidate Approval

## 1. Baselines
- Product PR #330 (read-only StaffPositionDiagnostics) merged: `dc511e6f663c08c180e1beae473c5b0d31f31bc4`
- Governance PR #224 merged: `b78c9c306d41ee5b045ae7bb308807be5555a787`
- Governance PR #225 merged: `c46dba9a53d95b4b2ebc6cc950ed1932cc24e4eb`
- Governance PR #226 merged: `c963a67b44454554d6e621654a0fa876c6692733`
- Governance PR #227 merged: `ba972acb3b8e7b92719161b05135f59a86594ff3`

Governance PR #227 established that no eligible committed safe natural public fixture exists, existing unknown-provenance PDFs are rejected, and fixture discovery/download/commit requires explicit Supervisor approval.

## 2. Active Blocker
The Score2GP project cannot run natural notehead morphology diagnostics because there is no approved safe natural public score fixture. 

## 3. Candidate Selected
- **Title**: Minuet in A minor (BWV Anh. 120)
- **Composer**: J. S. Bach (1685–1750)
- **Source page**: https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=1612
- **Source host**: Mutopia Project
- **Mutopia ID**: Mutopia-2009/01/06-1612
- **Candidate artifact format**: A4 PDF
- **Candidate artifact URL**: https://www.mutopiaproject.org/ftp/BachJS/BWVAnh120/BWV-120/BWV-120-a4.pdf
- **Note**: The Letter format PDF is explicitly not approved by this PR.

## 4. Source/Provenance/Licence Evidence
- **Fact**: The Mutopia project page lists the Copyright status as "Public Domain". 
- **Fact**: The source text used for typesetting is recorded as "Bach-Gesellschaft Ausgabe 1851-1899 Band 43 (1894)".
- **Inference**: Being in the Public Domain, redistribution, modification, and committing to a public repository as a fixture are fully permitted. Attribution is not strictly required but is good practice.

## 5. Suitability for Morphology Diagnostic
- **Inference**: A standard typesetting of a Bach Minuet contains standard natural notation (staff lines, noteheads, stems).
- **Inference**: As a piano minuet, it heavily features quarter notes and eighth notes (filled noteheads), which are exactly what the morphology diagnostic needs to test for horizontal projection robustness.
- **Inference**: It is not a tablature-only or handwritten score.

## 6. Risks and Unknowns
- **Unknown**: The actual performance of the morphology diagnostic on this specific PDF cannot be known until it is downloaded and the diagnostic is run.
- **Risk**: The quality or spacing of the LilyPond rendering might introduce specific artifacts, but as a "natural" (i.e. standard notation, non-synthetic for our project's generation purposes) PDF, it accurately represents real-world inputs.

## 7. Rejected Alternatives
- Other pieces were found via Mutopia (e.g., Carcassi Etudes, other Bach pieces), but the selected Minuet is short, standard, and clearly public domain. No other pieces were deeply evaluated since this one clearly met all requirements.

## 8. Recommendation A/B/C
**Recommendation A** — Approve candidate for later fixture ingestion.
The provenance and licence are completely clear, the candidate is highly suitable, and no binary was downloaded or committed.

## 9. Exact Next Task Allowed
Supervisor-approved fixture ingestion PR to download/commit exactly the approved candidate fixture with provenance metadata, no diagnostics, no product code changes, and artifact hygiene review.

## 10. Explicitly Blocked Scopes
- Binary fixture download/commit
- Diagnostic execution
- Product code changes
- Product test changes
- Semantic pitch implementation
- G-clef inference implementation
- Rhythm implementation
- Whole-note recognition implementation
- ScoreIR semantic changes
- GP export changes
- ML/OCR/model training
- Private fixture use
- Arbitrary public PDF downloads
- Unapproved binary fixture commits

## 11. Commands Run
- `gh pr view` for 224, 225, 226, 227
- Web search for Mutopia project Bach minuets.
- `curl` Mutopia project piece info page `https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=1612` to extract exact copyright and source details.

## 12. Artifact Hygiene
Clean. No binaries, PDFs, GP files, private files, or generated artifacts were downloaded or committed.

## 13. Fact / Inference / Hypothesis / Unknown Separation
Included implicitly in Sections 4, 5, and 6 above.
