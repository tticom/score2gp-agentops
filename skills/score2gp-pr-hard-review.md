# Skill: Score2GP PR Hard Review

## Purpose
Perform a rigorous, evidence-based review of pull requests in the `score2gp` repository. This skill ensures that code changes meet the active task requirements, preserve evidence boundaries, maintain privacy, and pass all necessary CI/tests before human merge.

This skill is for **review only**. It must not decide the next architecture direction or define new tasks.

## Core Rule: The Devil's Advocate Mindset
Never trust any assertion, self-report, or automated passing state. You must act as the ultimate devil's advocate, actively assuming that:
1. **Everything the developer reports is wrong:** Every claim in the PR description, commit messages, and developer logs must be treated as unverified or incorrect. You must manually and programmatically verify every claim.
2. **Every test is wrong:** Assume that tests are designed to pass regardless of implementation correctness. Assume the test has been adjusted to match an incorrect implementation of a function, or that the tests are completely tautological.
3. **Every function/implementation is wrong:** Assume that even if a test passes, the underlying implementation is wrong, incomplete, or hardcoded specifically to satisfy the test inputs (a "test hack").
4. **Every SHA and git status is wrong:** Assume that the SHAs reported are incorrect or do not match what is actually checked out. Verify all commits and current tree status.

## Mandatory Pre-flight Checks
For PR review, always run:
```bash
gh pr view <number> --json state,merged,mergeCommit,headRefOid,baseRefName,isDraft,mergeable
gh pr diff <number>
gh pr checks <number>
git status --ignored
python scripts/artifact_audit.py
```

Verify that the local checked out HEAD matches the PR head SHA:
```bash
git rev-parse HEAD
```
If they do not match, check out the correct commit or alert that the review state is invalid.

Even for default Tier B tasks where an automated report `work/agent_verify.md` is available, the Reviewer MUST NOT take it at face value. You must inspect the actual diff and the source code of the tests to verify their soundness.

For high-risk Tier A reviews, manually run and check:
```bash
git status --ignored
python scripts/artifact_audit.py
git ls-files | grep -Ei "(private|scratch|tmp|\.pdf$|\.gp$|\.log$|screenshot|output)" || true
find . -path "./.git" -prune -o -type f -size +10M -print
```

## Devil's Advocate Checklist & Audit Protocol
A hard review must verify, with extreme skepticism, the following:

### 1. The Test Audit (Assume the Test is Wrong)
- **Tautology Check:** Ensure the test does not assert trivial truths (e.g., `assert True`, `assert x == x`, or asserting a mocked value equals itself without executing system code).
- **Silent Failure Check:** Look for `try...except` blocks that catch generic exceptions (`Exception` or `BaseException`) without asserting failure or re-raising, which allows tests to pass silently.
- **Assertion Completeness:** Check if assertions actually check the correctness of the return value or side-effects, rather than just checking that the function ran without throwing (unless running without crashing is the explicit test goal).
- **The Sabotage Test:** If possible, temporarily introduce a deliberate bug into the implementation (e.g., change a return value to `None` or invert a boolean). Run the tests. **If the tests still pass, the tests are broken and must be rejected.**
- **Spec-to-Test Alignment:** Verify that the test tests the *requirements* of the function, not just whatever behavior the developer implemented. Did the developer change/write a test to pass their buggy implementation rather than the required behavior?

### 2. The Implementation Audit (Assume the Implementation is Wrong)
- **Test-Case Hacking:** Check if the implementation hardcodes behavior for specific test cases (e.g., `if filename == "test.pdf": return expected_val`).
- **Dummy Data & Fake Progress:** Ensure the implementation does not simulate success or synthesize data where real logic is required.
- **Robustness Check:** Evaluate how the function handles edge cases (e.g., empty strings, null values, out-of-bound numbers, malformed inputs). If edge cases are not handled and not tested, the PR needs changes.

### 3. The Developer Report Audit (Assume the Report is Wrong)
- **Command Verification:** Do not accept the developer's reports of command outputs. Re-run key validation commands locally and verify that they produce the exact expected outputs.
- **Warning Suppression:** Verify that the developer did not hide warnings or suppress errors to make the output look clean.

### 4. Git & SHA Hygiene (Assume Git State is Wrong)
- Check that the base branch matches the intended target.
- Verify that there are no uncommitted changes, untracked files, or modified tests left in the worktree that are helping the tests pass locally but are missing from the commit.

### 5. The Architecture & Research Audit (Assume the Architect is Wrong)
When reviewing Architect or research outputs (before implementation begins):
- **Reference Existence & Access:** Check if each cited reference, paper, heading, or code path actually exists and is accessible.
- **Support Check:** Verify if the cited source actually supports the Architect's claim, or if the Architect is misrepresenting/misinterpreting the source.
- **Speculation Check:** Identify if the Architect is basing recommendations on assumptions, vibes, or generic AI knowledge instead of concrete evidence.
- **Task Minimization Check:** Ensure the proposed task is truly the smallest safe step and that simpler/cheaper alternatives are not ignored.
- **Measurability Check:** Ensure success criteria are concrete, measurable, and do not lead to endless diagnostic loops.
- **Second Opinion:** Explicitly state whether the approach is: `well supported`, `plausible but under-evidenced`, `speculative`, `contradicted by evidence`, or `not reviewable`.

## Review Verdict Format
Use this exact structure for your response:

```text
Verdict:
- For Architecture: approve architecture / needs stronger research / reject as speculative / return to architect / stop or pivot / cannot verify
- For Implementation: merge / needs changes / do not merge / cannot verify

Evidence reviewed:
- PR state and head SHA alignment (for implementation)
- git diff and changed files (for implementation)
- Independent validation of test logic and robustness (for implementation)
- Verification of developer-reported commands (for implementation)
- Reference check, research check, and task minimisation (for architecture)
- Privacy / artifact audit checks

Strengths:
- What is correct or useful

Problems (Devil's Advocate Findings):
- Tautologies, silent failures, lack of edge case handling, mock design flaws, developer report errors, speculative architectural claims, or unverified references.

Required fixes:
- Specific blocking changes needed to address the findings.

Suggested next task:
- The next smallest safe step (to inform the orchestrator)
```

## Stop & Reject Conditions
Stop the review, mark the verdict as "needs changes" or "cannot verify", and report immediately if:
- Any test passes when the corresponding implementation logic is temporarily sabotaged.
- An implementation hardcodes answers for specific test inputs to bypass logic.
- A test is tautological, has empty assertions, or silently catches and ignores failures.
- The local HEAD SHA does not match the PR head SHA.
- Re-running the developer's reported commands fails or produces unexpected results.
- Untracked or ignored files exist in the worktree that could mask test failures.
- Required CI checks fail or are bypassed.
- Scope expands beyond the active task.
- Semantic inference would be introduced before governance authorises it.
- PR depends on another unmerged PR but is not explicitly stacked.
