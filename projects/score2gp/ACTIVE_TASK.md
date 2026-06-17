# Product Task 175: Diagnose generated public PDF logical-clef extraction gap

## Repository
tticom/score2gp

## Goal
Empirically diagnose why the current generated public PDF fixtures do not produce deterministic logical treble-clef evidence that reaches the logical clef bridge, while preserving all diagnostic/read-only boundaries.

## Scope
* Work in `tticom/score2gp`.
* Verify Governance PR #183 is merged before product work begins.
* Verify Product PR #293 is merged before product work begins.
* Verify Product PR #292 is merged before product work begins.
* Inspect existing generated public fixture generation and diagnostic/reporting patterns before changing anything.
* Inspect how left-margin primitive candidates are extracted from generated public PDFs.
* Inspect what primitive types, bounding boxes, groupings, and staff associations are produced around clef regions in the authorised public generated fixture set.
* Add a safe diagnostic script, focused test, or report that characterises the extraction gap using aggregate/non-sensitive evidence only.
* The diagnostic must distinguish at least:
  * no left-margin primitives found;
  * primitives found but wrong type;
  * primitives found but malformed;
  * primitives found but too fragmented;
  * primitives found but outside staff/clef region;
  * primitives found but ambiguous;
  * primitives found but failing classifier thresholds;
  * staff association missing or malformed.
* Prefer public/generated fixtures already tracked in the repository.
* Do not add private PDFs or screenshots.
* Do not modify the classifier heuristics unless the task discovers an obvious safe diagnostic-only bug in reporting; if any behavioural classifier change is needed, stop and report.
* Preserve the existing Task 170 aggregate report unless the task intentionally generates a new clearly named diagnostic report and justifies it.
* Keep all results honest if public fixture aggregate remains unchanged.
* Preserve strict clef evidence policy.
* Preserve `unknown` for weak, malformed, missing, or ambiguous clef evidence.
* Preserve `assumed_treble_pitch` as a separate fallback/diagnostic concept.
* Preserve existing raster clef diagnostics.
* Preserve diagnostic/reporting boundaries.

## Non-Goals
* Do not implement broad visual clef recognition.
* Do not tune classifier thresholds to force current fixtures to pass.
* Do not guess treble clef globally.
* Do not use `assume_treble_clef` as visual clef evidence.
* Do not infer clef from pitch outcomes.
* Do not infer clef from note positions.
* Do not infer clef from staff position.
* Do not infer clef from ledger-line placement.
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
* Do not commit private fixtures, private diagnostics, screenshots, logs, scratch JSON, PDFs, images, GP files, credentials, generated dumps, or sensitive material.

## Required Pre-flight Checks
Run and report:
```bash
git status --short
git branch --show-current
git fetch --all --prune
git log --oneline --decorate --graph --max-count=20
gh pr view 183 --repo tticom/score2gp-agentops --json state,mergedAt,mergeCommit,headRefOid,baseRefName,isDraft,title,url,changedFiles
gh pr view 293 --repo tticom/score2gp --json state,mergedAt,mergeCommit,headRefOid,baseRefName,isDraft,title,url,changedFiles
gh pr view 292 --repo tticom/score2gp --json state,mergedAt,mergeCommit,headRefOid,baseRefName,isDraft,title,url,changedFiles
```

## Required Validation
Run focused tests relevant to changed files and report exact commands/results. At minimum:
* focused test for any new diagnostic/reporting helper;
* existing logical clef coverage proof test;
* existing logical clef bridge tests;
* Task 170 coverage analysis or equivalent diagnostic run, if available;
* any new extraction-gap diagnostic script/report command;
* `git diff --check`;
* `git diff --stat`;
* `git status --short`;
* `git status --ignored`;
* `git ls-files | grep -Ei "(private|scratch|dump|log|\.pdf$|\.gp$|\.png$|\.jpg$|\.jpeg$|\.json$)" || true`

## Acceptance Criteria
* Governance PR authorising Task 175 is verified merged before implementation.
* Product PR #293 is verified merged before implementation.
* Product PR #292 is verified merged before implementation.
* A repeatable diagnostic identifies where generated public PDF logical-clef evidence is lost or rejected.
* The diagnostic distinguishes extraction absence, primitive type/shape problems, fragmentation, malformed evidence, ambiguity, classifier-threshold failure, and staff-association failure where applicable.
* Results are aggregate/safe and do not expose private data.
* Existing synthetic logical-clef coverage proof remains passing.
* Existing logical clef bridge tests remain passing.
* Task 170-style aggregate is reported honestly, whether changed or unchanged.
* No classifier threshold tuning or broad visual recognition is introduced.
* No global treble guessing is introduced.
* `assume_treble_clef` is not used as visual clef evidence.
* Existing raster clef diagnostics are preserved.
* Diagnostic/reporting boundary is preserved.
* No private or unsafe artifacts are committed.
* A product PR is opened with complete evidence.

## Stop Conditions
Stop and report if:
* The governance PR authorising Task 175 is not merged.
* Product PR #293 is not merged.
* Product PR #292 is not merged.
* The working tree is dirty before changes and the dirt is unrelated.
* The logical clef bridge cannot be located.
* The generated public fixture set cannot be located.
* The only feasible diagnosis requires private fixtures or unsafe artifacts.
* The only feasible implementation requires broad visual clef recognition.
* The only feasible implementation requires global treble guessing.
* The only feasible implementation requires classifier threshold tuning to force a pass.
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
  * Product PR #293 prerequisite verification.
  * Product PR #292 prerequisite verification.
  * Implementation summary.
  * Exact files changed.
  * Extraction-gap diagnostic summary.
  * Coverage/diagnostic evidence.
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
* Product PR #293 verification result.
* Product PR #292 verification result.
* Extraction-gap diagnostic summary.
* Coverage/diagnostic evidence.
* Validation commands and results.
* Privacy/artifact hygiene result.
* Behavioural confirmations.
* Known limitations.
* Suggested next action.
