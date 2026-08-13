# Root-Cause Analysis: Review Skills Failure on CRP-10, 11, and 12

## 1. Overview
During the reviews of CRP-10, CRP-11, and CRP-12, severe architectural regressions and silent data corruption fallbacks were merged into `main`. The `devils-advocate-review` skill failed to identify these P1 issues despite its mandate to act as a sceptical reviewer. 

## 2. Identified Failures
1. **Silent Fallbacks Masked as Strictness (CRP-12 & CRP-10):**
   - **CRP-12:** `ScoreIRCompiler` claimed strict refusal of synthetic notes but silently injected `(string=1, fret=0)` notes for unowned notes.
   - **CRP-10:** `TopologicallyLockedBarTimeline` silently truncated overlapping notes and injected `padding_rest` data.
   - **Reviewer Gap:** The reviewer relied on author summaries claiming strict invariants and failed to execute adversarial inputs that would trigger the unowned note or overlapping note conditions. Fail-closed behavior was not verified.

2. **Semantic Blanks in Mock-Only Evidence (CRP-11):**
   - **CRP-11:** `BiomechanicalPositionOptimizer` evaluated chords sequentially rather than concurrently.
   - **Reviewer Gap:** The reviewer accepted tests built with mocks and sequential inputs, failing to demand integration tests with actual chord geometries. The reviewer did not construct a metamorphic relation test for simultaneous notes.

3. **Greenwashing via Skipped Tests and Weak Oracles:**
   - Private integration tests used `pytest.skip` when fixtures were absent. CI reported these as "green", providing a false sense of security.
   - Oracles merely checked for `.gp` file size > 0 instead of verifying semantic data.
   - **Reviewer Gap:** The reviewer treated a "green" CI result and file existence as verified evidence, violating the rule that file existence is insufficient and failing to demand exact semantic oracles.

## 3. Proposed Updates to Governance Rules (`REVIEW_RULES.md`)
To prevent recurrence, `projects/score2gp/REVIEW_RULES.md` is being amended with:
- **Ban on Skipped Tests:** Explicitly declaring that skipped tests (e.g., missing private fixtures) are `NOT_EVALUATED`, not `PASS`, and block approval.
- **Ban on Silent Fallbacks:** Mandating that strict capacity/refusal claims must fail-closed with exceptions, not silent data injection (e.g. `padding_rest` or `string=1, fret=0`) or silent truncation.
- **Ban on Mock-Only Evidence:** Requiring real-world private fixtures for integration correctness, explicitly rejecting mock-only test suites.
- **Semantic Oracle Requirements:** Explicitly requiring semantic validation of generated `.gp` files, banning `size > 0` checks as proof of correctness.

## 4. Reusable `devils-advocate-review` Follow-up Specification
This specification outlines required changes to the shared `devils-advocate-review` skill (to be executed in a separate authorized task in `agy-skills`):
1. **Test Log Parser Upgrade:** The skill must instruct the reviewer to parse test logs for `SKIPPED` statuses. If private fixture tests are skipped, the reviewer agent must automatically transition to `blocked` or `cannot verify`.
2. **Adversarial Input Generation:** The skill prompt must instruct the reviewer to actively inject edge cases (e.g., overlapping notes, simultaneous chords, missing note ownership) to verify fail-closed behaviour instead of silent mutation.
3. **Oracle Stringency Check:** The reviewer must inspect the test source code to verify that assertions check semantic file content, not just `os.path.getsize(file) > 0`.
