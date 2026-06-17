# ACTIVE TASK

## Product Task 173: Bridge logical clef candidate evidence into read-only clef-resolved pitch mapping

**Repository:** `tticom/score2gp`

### Goal
Use the diagnostic logical clef candidate evidence introduced by Product Task 172 to reduce the missing-clef blocker in clef-resolved pitch coverage, while preserving the read-only diagnostic boundary.

### Scope
* Work in `tticom/score2gp`.
* Verify Governance PR authorising Task 173 is merged before product work begins.
* Verify Product PR #291 is merged before product work begins.
* Inspect where `LeftMarginPrimitiveCandidate` evidence is available in the recognition pipeline.
* Inspect where `classify_logical_clef_candidate` can be safely invoked.
* Inspect where `clef_resolved_staff_pitch` currently obtains clef evidence.
* Bridge only deterministic, unambiguous logical clef candidate evidence into the existing clef evidence boundary used by read-only coverage/pitch diagnostics.
* Preserve the strict evidence policy.
* Preserve `unknown` for weak, malformed, missing, or ambiguous clef evidence.
* Preserve `assumed_treble_pitch` as a separate fallback/diagnostic concept; do not treat it as visual clef evidence.
* Preserve `clef_resolved_staff_pitch` semantics.
* Preserve existing raster clef diagnostics.
* Add focused tests proving logical clef evidence can reduce missing-clef skips without broad guessing.
* Re-run the Task 170-style coverage analysis or equivalent focused diagnostic to show whether missing-clef blocker count changes.

### Non-Goals
* Do not declare `clef_resolved_staff_pitch` canonical.
* Do not implement playable output.
* Do not implement ScoreIR.
* Do not implement MusicXML.
* Do not implement GP output.
* Do not implement rhythm.
* Do not implement accidentals.
* Do not implement key signatures.
* Do not implement rests.
* Do not implement OCR.
* Do not implement broad visual clef recognition.
* Do not guess treble clef globally.
* Do not use `assume_treble_clef` as visual clef evidence.
* Do not infer clef from pitch outcomes.
* Do not infer clef from note positions.
* Do not infer clef from staff position.
* Do not infer clef from ledger-line placement.
* Do not commit private fixtures, private diagnostics, screenshots, logs, scratch JSON, PDFs, images, GP files, credentials, generated dumps, or sensitive material.

### Required Pre-Flight Checks
Run and report:
```bash
git status --short
git branch --show-current
git fetch --all --prune
git log --oneline --decorate --graph --max-count=20
gh pr view 181 --repo tticom/score2gp-agentops --json state,mergedAt,mergeCommit,headRefOid,baseRefName,isDraft,title,url,changedFiles
gh pr view 291 --repo tticom/score2gp --json state,mergedAt,mergeCommit,headRefOid,baseRefName,isDraft,title,url,changedFiles
gh pr view 290 --repo tticom/score2gp --json state,mergedAt,mergeCommit,headRefOid,baseRefName,isDraft,title,url,changedFiles
```

### Required Validation
Run focused tests relevant to changed files and report exact commands/results. At minimum:
* focused tests for the bridge logic;
* existing tests for logical clef candidate classifier;
* relevant note-candidate recognition or coverage tests;
* Task 170 coverage analysis script or equivalent diagnostic run, if available;
* `git diff --check`
* `git diff --stat`
* `git status --short`
* `git status --ignored`
* `git ls-files | grep -Ei "(private|scratch|dump|log|\.pdf$|\.gp$|\.png$|\.jpg$|\.jpeg$|\.json$)" || true`

### Acceptance Criteria
* Governance PR authorising Task 173 is verified merged before implementation.
* Product PR #291 is verified merged before implementation.
* Product PR #290 is verified merged before implementation.
* The bridge uses only deterministic, unambiguous logical clef candidate evidence.
* Missing, weak, malformed, or ambiguous evidence remains unknown.
* No global treble guessing is introduced.
* `assume_treble_clef` is not used as visual clef evidence.
* `clef_resolved_staff_pitch` semantics are preserved.
* Existing raster clef diagnostics are preserved.
* Focused regression tests pass.
* Coverage evidence shows whether missing-clef blocker count improves.
* No private or unsafe artifacts are committed.
* A product PR is opened with complete evidence.

### Stop Conditions
Stop and report if:
* The governance PR authorising Task 173 is not merged.
* Product PR #291 is not merged.
* Product PR #290 is not merged.
* The working tree is dirty before changes and the dirt is unrelated.
* The logical clef candidate classifier cannot be located.
* `LeftMarginPrimitiveCandidate` evidence is not available at the bridge boundary.
* The only feasible implementation requires broad visual clef recognition.
* The only feasible implementation requires global treble guessing.
* The only feasible implementation requires using `assume_treble_clef` as visual clef evidence.
* The only feasible implementation requires inferring clef from pitch outcomes, note positions, staff position, or ledger-line placement.
* The implementation would require private fixtures or unsafe artifacts.
* The implementation would require playable output, ScoreIR, MusicXML, GP output, rhythm, accidentals, key signatures, rests, or OCR.
* Tests fail in a way the agent cannot explain or isolate.
* Requirements conflict with verified repository state.

### PR Requirements
* Work on a short-lived feature branch.
* Commit only intentional product changes.
* Open a product PR against `main`.
* Include in the PR body:
  * Task summary.
  * Governance prerequisite verification.
  * Product PR #291 prerequisite verification.
  * Product PR #290 prerequisite verification.
  * Implementation summary.
  * Exact files changed.
  * Bridge boundary summary.
  * Coverage evidence.
  * Tests run and results.
  * Safety and privacy/artifact hygiene result.
  * Behavioural confirmations.
  * Known limitations.
  * Suggested next action.
* Do not merge the product PR.

### Reporting Format
Return:
* Branch name.
* Product PR link.
* Full head SHA.
* Exact files changed.
* Governance prerequisite verification result.
* Product PR #291 verification result.
* Product PR #290 verification result.
* Logical clef bridge summary.
* Coverage improvement evidence.
* Validation commands and results.
* Privacy/artifact hygiene result.
* Behavioural confirmations.
* Known limitations.
* Suggested next action.
