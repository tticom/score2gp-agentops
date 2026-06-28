# Active Task

**Task**: Reviewer architecture verification of the Architect's fixture candidate discovery and approval recommendation.
**Authorised Role**: Reviewer
**Repository**: `tticom/score2gp-agentops`

## 1. Baseline
- Product PR #330 and Governance PRs #224, #225, #226, and #227 are merged.
- PR #227 determined that the morphology method requires testing on a safe natural fixture because synthetic quarter-notes remained ambiguous, and that no eligible safe natural public fixtures were present in the repository.
- Architect identified one safe candidate natural public score fixture (Bach Minuet BWV Anh. 120 from Mutopia) and verified its Public Domain provenance.
- The exact artifact format was pinned to A4 PDF with exact URL: `https://www.mutopiaproject.org/ftp/BachJS/BWVAnh120/BWV-120/BWV-120-a4.pdf`.
- The Letter PDF is explicitly not approved. Later fixture ingestion must use only the pinned A4 PDF URL.
- The candidate was evaluated as suitable for morphology diagnostics, and Recommendation A was proposed.
- NO binary files were downloaded or committed.

## 2. Active Blocker
The project requires a Supervisor decision to approve or reject the candidate natural fixture before a fixture-ingestion PR can be created. The Architect recommendation must first pass Reviewer architecture verification.

## 3. Authorised Scope
The Reviewer is authorised to:
- evaluate the Architect's report in `projects/score2gp/decisions/2026-06-27-safe-natural-fixture-candidate-approval.md`;
- verify whether the Architect correctly avoided downloading or committing binaries;
- verify whether the provenance and licence evidence provided supports the candidate;
- authorise the next task for a Supervisor approval decision on the candidate;
- reject or amend the proposal if the fixture constraints were violated.

The Reviewer must not:
- implement product code;
- implement semantic pitch, clef, rhythm, or whole-note recognition;
- change ScoreIR semantics;
- change GP export;
- authorise ML/OCR/model training;
- download or commit the candidate PDF file.

## 4. Required Outcomes
The next task must force one of these outcomes:
- **Outcome A**: The candidate discovery and provenance evaluation is verified, and the Supervisor decision task is authorised.
- **Outcome B**: The proposal needs revision to meet architectural or safety constraints.
- **Outcome C**: The proposal is rejected, forcing a pivot or stop condition.
