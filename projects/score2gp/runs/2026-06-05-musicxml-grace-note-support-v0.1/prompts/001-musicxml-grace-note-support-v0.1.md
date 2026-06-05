Title: MusicXML Grace Note Support v0.1

Context:
The project has reached the post-layout-gating milestone.

Current verified state:

* Product main includes PR #169.
* Product merge commit: `b9f54a40ffa963e83e91a2fd22070ec9eeff6d75`.
* Public tests: 466 passed.
* private_input_1 is a milestone success under default flow:

  * compiles to ScoreIR
  * writes a validated GP package
  * matches 137/137 non-grace MusicXML notes
  * has 153 playable PDF candidates
  * has 16 unmatched PDF candidates
* Grace-note architecture research found:

  * private_input_1 has 90 total grace notes across the full MusicXML.
  * 45 are in notation voice 1.
  * 45 are in TAB voice 5.
  * All 45 TAB voice grace notes contain explicit string/fret technical data.
  * On page 1 / first 7 measures, there are 16 unmatched PDF candidates.
  * 15 of those 16 correspond to grace notes currently skipped as `musicxml-grace-skipped`.
  * These grace-note candidates occur immediately before their host/following notes.
  * Because grace notes are skipped, host notes can be matched against the grace-note PDF candidates, causing a cascading pitch mismatch.
* Lessons 3–7 remain stable.
* Melodic Soloing remains stable at 82 matched notes.
* Unsupported/scanned/ASCII/missing-sidecar inputs are now cleanly refused by explicit gates.
* Private-safety invariant is clean:
  `git ls-files fixtures/private work` -> `fixtures/private/.gitkeep`

Governance prerequisite:
Ensure the grace-note architecture research branch/PR is merged or at least available in agentops before opening the product PR. Do not start from undocumented local evidence.

Role:
Developer.

Branch:
`feature/grace-note-support-v0.1`

Goal:
Implement narrow grace-note support for standard guitar-track MusicXML so simple pitched TAB grace notes can be parsed, deduplicated, aligned to preceding visual PDF candidates, and represented safely without corrupting measure timing.

Primary target:
Reduce private_input_1 unmatched candid
<truncated 6145 bytes>
.
* Private-safety invariant remains clean.
* private_input_1 still compiles under default flow.
* private_input_1 still writes a valid GP package.
* Existing 137 non-grace matches do not regress.
* Grace-note skip count for private_input_1 decreases materially.
* Target for v0.1: unmatched candidates reduce from 16 to approximately 1 on the existing audit, if the research hypothesis is correct.
* ScoreIR/GPIF output remains valid.
* Lessons 3–7 remain stable:

  * Lesson 3: 459
  * Lesson 4: 546
  * Lesson 5: 295
  * Lesson 6: 235
  * Lesson 7: 624
* Melodic Soloing remains stable at 82.
* Unsupported/scanned/ASCII/missing-sidecar inputs remain cleanly refused.
* No private/generated artifacts are tracked.

Stop conditions:
Stop and report instead of broadening if:

* public tests fail before changes;
* private-safety invariant fails;
* grace note skip source cannot be isolated;
* ScoreIR cannot safely represent grace notes;
* GPIF representation cannot be determined safely;
* adding grace notes creates timing overlaps;
* host note matching regresses;
* non-grace matched count drops;
* implementation requires hardcoded private coordinates;
* implementation requires a broad timing-engine rewrite;
* implementation requires committing private/generated artifacts.

Reporting format:
Verdict:

* ready for review
* blocked
* needs architecture decision
* false hypothesis

Include:

* branch name
* commit hash
* files changed
* implementation summary
* supported grace-note scope
* unsupported grace-note cases
* public test result
* private smoke result
* private audit result, counts only
* private_input_1 matched/unmatched before and after
* grace-note skip count before and after
* non-grace match stability result
* GPIF validity result
* Lessons 3–7 matched counts
* Melodic Soloing matched count
* private-safety output
* working tree status

