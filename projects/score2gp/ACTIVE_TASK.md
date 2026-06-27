# Active Task

**Task**: Reviewer architecture verification of the Architect's proposal to evaluate the horizontal projection morphology method on explicitly safe natural public fixtures.
**Authorised Role**: Reviewer
**Repository**: `tticom/score2gp-agentops`

## 1. Baseline
- Architect diagnostic evaluation of notehead-center morphology is complete.
- Fixture evidence proved that horizontal projection density successfully resolved 100% of half and whole note stem/padding offsets (snapping residuals to near-zero).
- However, synthetic quarter notes remained ambiguous because they were drawn as perfect off-grid blocks in the test suite, resulting in a 66.6% resolution rate (missing the 70% Outcome A threshold).
- Architect selected **Outcome B**: Useful but insufficient alone, because synthetic anomalies prevent full verification.
- Architect proposed a new fixture-safety-gated diagnostic phase to evaluate the method on natural (non-synthetic) fixtures.

## 2. Active Blocker
The previous blocker (absence of diagnostic evidence for notehead morphology viability) is closed.
The new blocker is that the Architect's proposal to test morphology on natural fixtures must pass Reviewer architecture verification before any further Architect diagnostics or Developer implementations can proceed.

## 3. Authorised Scope
The Reviewer is authorised to:
- evaluate the Architect's report in `projects/score2gp/decisions/2026-06-27-notehead-center-morphology-architect-evaluation.md`;
- verify whether testing morphology on a natural public fixture is bounded and safe (i.e. strictly using committed safe fixtures or a safe fixture-discovery gate);
- authorise the next Architect task if the proposal is sound;
- reject or amend the proposal if it risks unbound CV/ML approaches or unsafe fixture sourcing.

The Reviewer must not:
- implement product code;
- implement semantic pitch, clef, rhythm, or whole-note recognition;
- change ScoreIR semantics;
- change GP export;
- authorise ML/OCR/model training.

## 4. Required Outcomes
The next task must force one of these outcomes:
- **Outcome A**: The natural fixture evaluation proposal is verified and the next Architect task is authorised.
- **Outcome B**: The proposal needs revision to meet architectural constraints.
- **Outcome C**: The proposal is rejected, forcing a pivot to a different approach.
