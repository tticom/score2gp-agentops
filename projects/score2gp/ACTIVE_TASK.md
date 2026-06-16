# Active Product Task

## Product Task 170 — Run clef-resolved pitch coverage report across authorised fixture corpus and record quality findings

### Scope
- Work in `tticom/score2gp`.
- Product Task 170 should be a read-only diagnostic analysis task. It should run or extend the new `clef_resolved_pitch_coverage` report over authorised fixtures and/or existing diagnostic outputs to identify where clef-resolved pitch mapping is succeeding, failing, or being skipped. The goal is to produce evidence for the next smallest recognition-improvement task, not to change recognition heuristics yet.
- Use the existing `clef_resolved_pitch_coverage` report added by Product Task 169.
- Run the report against authorised public fixtures and existing safe diagnostic outputs.
- Private fixtures may be used only if they are already authorised for local testing and are not newly committed.
- Summarise coverage and skip reasons.
- Identify the dominant blockers:
  - missing clef evidence;
  - ambiguous clef evidence;
  - malformed staff association;
  - malformed staff position;
  - missing ledger support;
  - pitch out of supported range;
  - zero or low `clef_resolved_staff_pitch` coverage.
- Produce a concise diagnostic findings report that recommends the next smallest safe product task.
- If a committed report file is useful, it must contain only safe aggregate data and no private filenames, copyrighted source names, raw OCR dumps, private fixture paths, or sensitive data.
- If committing any diagnostic report is unsafe, the product agent must report the findings in the PR body only and not commit the report artifact.
- Prefer using existing report paths or small wrapper scripts/options.

### Non-Goals
- Do not change recognition behaviour.
- Do not change pitch mapping semantics.
- Do not add or commit private PDFs, private diagnostic dumps, screenshots, logs, scratch JSON, GP files, images, or unrelated artifacts.
- Do not implement new clef detection.
- Do not implement canonical pitch adoption.
- Do not implement ScoreIR, MusicXML, Guitar Pro output, rhythm, accidentals, key signatures, rests, or OCR.

### Required Pre-flight Checks
Run these before making changes:
    git status --short
    git branch --show-current
    git fetch --all --prune
    git checkout main
    git pull --ff-only
    git log --oneline --decorate --graph --max-count=20

Also verify that the governance PR authorising Product Task 170 is merged before making product changes.

### Required Tests
Add or update tests proving:
- Any script/reporting extension added remains testable and functionally correct on safe data.
- Existing features, reporting paths, and whole-note compatibility remain unchanged.

### Validation
Run focused tests covering raster bridge, note-candidate reporting, CLI output, and whole-note compatibility. At minimum:
    pytest tests/test_raster_treble_clef_bridge.py tests/test_note_candidate_recognition_report.py tests/test_note_candidate_recognition_cli.py tests/test_whole_note_recognition_cli.py
    git diff --check
    git diff --stat
    git status --short
    git status --ignored
    git ls-files | grep -Ei "(private|scratch|dump|log|\.pdf$|\.gp$|\.png$|\.jpg$|\.jpeg$|\.json$)" || true

If tracked public fixture JSON files appear in `git ls-files`, explain whether they are pre-existing and whether this task changed them. Do not add new private or unrelated artifacts.

### Acceptance Criteria
- A diagnostic run or report is executed across the authorised corpus.
- The dominant blockers for `clef_resolved_staff_pitch` mapping are identified and quantified.
- A concise summary recommends the next smallest safe product task based on empirical findings.
- No product logic or mapping semantics are modified.
- The task does not emit playable output.
- Existing recognition behaviour is preserved.
- Focused tests pass.
- Hygiene checks pass.
- PR body records exact commands, results, files changed, branch name, full head SHA, the findings summary, and the recommendation for the next task.

### Stop conditions
Stop and report instead of continuing if:
- Governance authorisation for Product Task 170 is not merged.
- Running the report across the corpus produces unexpected exceptions or exposes malformed states that block aggregate counts.
- Existing tests fail before your changes in a way that prevents clean attribution.
- Safe reporting requires committing private fixtures or unapproved artifacts.
- The diagnostic results are ambiguous or uniformly zero and no clear next step can be recommended.
- You would need to commit private fixtures, diagnostic dumps, scratch JSON, logs, credentials, screenshots, GP files, PDFs, images, or unrelated artifacts.

### Commit and PR requirements
- Commit only intentional product files (e.g. a small summary script or test update).
- Push the feature branch.
- Open a product PR against `main`.
- The PR body must include:
  - Product Task 170 summary.
  - Governance PR verification result.
  - Exact files changed (if any).
  - Diagnostic findings and dominant blockers.
  - Recommendation for the next product task.
  - Validation commands and results.
  - Privacy/artifact hygiene result.
  - Confirmation that no canonical pitch adoption, mapping changes, or playable output were introduced.

### Reporting format
Return:
- Branch name.
- Product PR link.
- Full head SHA.
- Exact files changed.
- Summary of diagnostic execution.
- Key findings and identified blockers.
- Recommended next smallest product task.
- Validation commands and results.
- Privacy/artifact hygiene result.
- Confirmation that no canonical pitch adoption or mapping changes were introduced.
- Known limitations.
