# Product Task 174: Add public logical-clef coverage proof for clef-resolved whole-note diagnostics

## Repository
tticom/score2gp

## Goal
Create safe public/generated or synthetic regression evidence proving that, when deterministic logical treble-clef evidence is present, the pipeline can map a whole-note candidate through `clef_resolved_staff_pitch` instead of skipping it for missing clef evidence.

## Scope
* Work in `tticom/score2gp`.
* Verify Governance PR #182 is merged before product work begins.
* Verify Product PR #292 is merged before product work begins.
* Inspect existing fixture generation and test patterns before changing anything.
* Add the smallest safe public/generated or synthetic coverage proof for the logical clef bridge.
* Prefer a synthetic/integration test if it proves the pipeline boundary without committing new PDFs.
* If adding a public generated fixture is necessary, it must be clearly generated, non-private, minimal, deterministic, and safe to commit.
* The proof must show at least one logical-clef-backed staff where:
  * deterministic logical clef evidence is present;
  * a note candidate has staff position evidence;
  * `clef_resolved_staff_pitch` is produced;
  * the candidate is not skipped for missing clef evidence.
* Update or add focused diagnostics/tests so the evidence is repeatable.
* Preserve the existing Task 170 aggregate report unless the task intentionally regenerates it and the change is justified.
* Keep the public fixture aggregate result honest if it remains unchanged.
* Preserve strict clef evidence policy.
* Preserve `unknown` for weak, malformed, missing, or ambiguous clef evidence.
* Preserve `assumed_treble_pitch` as a separate fallback/diagnostic concept.
* Preserve existing raster clef diagnostics.
* Preserve diagnostic/reporting boundaries.

## Non-Goals
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

## Required Pre-flight Checks
Run and report:
```bash
git status --short
git branch --show-current
git fetch --all --prune
git log --oneline --decorate --graph --max-count=20
gh pr view 182 --repo tticom/score2gp-agentops --json state,mergedAt,mergeCommit,headRefOid,baseRefName,isDraft,title,url,changedFiles
gh pr view 292 --repo tticom/score2gp --json state,mergedAt,mergeCommit,headRefOid,baseRefName,isDraft,title,url,changedFiles
gh pr view 291 --repo tticom/score2gp --json state,mergedAt,mergeCommit,headRefOid,baseRefName,isDraft,title,url,changedFiles
```

## Required Validation
Run focused tests relevant to changed files and report exact commands/results. At minimum:
* focused test proving logical-clef-backed `clef_resolved_staff_pitch` mapping;
* existing logical clef bridge tests;
* relevant coverage/reporting tests;
* Task 170 coverage analysis or equivalent diagnostic run, if available;
* `git diff --check`;
* `git diff --stat`;
* `git status --short`;
* `git status --ignored`;
* `git ls-files | grep -Ei "(private|scratch|dump|log|\.pdf$|\.gp$|\.png$|\.jpg$|\.jpeg$|\.json$)" || true`

## Acceptance Criteria
* Governance PR authorising Task 174 is verified merged before implementation.
* Product PR #292 is verified merged before implementation.
* A repeatable public/generated or synthetic proof demonstrates logical-clef-backed `clef_resolved_staff_pitch` mapping.
* The proof shows at least one candidate is not skipped for missing clef evidence when deterministic logical clef evidence is present.
* Weak, missing, malformed, or ambiguous evidence remains `unknown`.
* No global treble guessing is introduced.
* `assume_treble_clef` is not used as visual clef evidence.
* Existing raster clef diagnostics are preserved.
* Diagnostic/reporting boundary is preserved.
* Focused regression tests pass.
* Public fixture aggregate evidence is reported honestly, whether changed or unchanged.
* No private or unsafe artifacts are committed.
* A product PR is opened with complete evidence.

## Stop Conditions
Stop and report if:
* The governance PR authorising Task 174 is not merged.
* Product PR #292 is not merged.
* Product PR #291 is not merged.
* The working tree is dirty before changes and the dirt is unrelated.
* The logical clef bridge cannot be located.
* The only feasible proof requires private fixtures or unsafe artifacts.
* The only feasible implementation requires broad visual clef recognition.
* The only feasible implementation requires global treble guessing.
* The only feasible implementation requires using `assume_treble_clef` as visual evidence.
* The only feasible implementation requires inferring clef from pitch outcomes, note positions, staff position, or ledger-line placement.
* The implementation would require playable output, ScoreIR, MusicXML, GP output, rhythm, accidentals, key signatures, rests, or OCR.
* Tests fail in a way the agent cannot explain or isolate.
* Requirements conflict with verified repository state.

## PR Requirements
* Work on a short-lived feature branch.
* Commit only intentional product changes.
* Open a product PR against `main`.
* Include in the PR body:
  * Task summary.
  * Governance prerequisite verification.
  * Product PR #292 prerequisite verification.
  * Product PR #291 prerequisite verification.
  * Implementation summary.
  * Exact files changed.
  * Coverage proof summary.
  * Tests run and results.
  * Safety and privacy/artifact hygiene result.
  * Behavioural confirmations.
  * Known limitations.
  * Suggested next action.
* Do not merge the product PR.

## Reporting Format
Return:
* Branch name.
* Product PR link.
* Full head SHA.
* Exact files changed.
* Governance prerequisite verification result.
* Product PR #292 verification result.
* Product PR #291 verification result.
* Logical clef coverage proof summary.
* Coverage/diagnostic evidence.
* Validation commands and results.
* Privacy/artifact hygiene result.
* Behavioural confirmations.
* Known limitations.
* Suggested next action.
