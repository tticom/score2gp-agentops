# Pull Request Standards Rule

## Invariants for Pull Request Creation

Whenever any agent creates or opens a Pull Request (via `gh pr create`, CLI scripts, or automated tools):

1. **Mandatory Explicit Title**:
   - Every Pull Request MUST have an explicit, descriptive, non-empty title provided at creation time.
   - The title MUST follow standard project conventions (e.g. `fix(scope): description`, `feat(scope): description`, `docs(scope): description`).
   - Never create a PR relying on Git commit default titles or auto-generated fallback titles.

2. **Complete Non-Default Standard Fields**:
   - Standard PR fields—including Title, Description/Body, Base Branch, and Head Branch—MUST NOT be left with default, blank, or placeholder values.
   - The PR body MUST contain comprehensive summary context, including work accomplished, verification commands executed, test results, and reviewer focus areas (e.g., generated via project helpers such as `python scripts/pr_body.py`).

3. **Pre-flight Field Verification**:
   - Before executing `gh pr create`, agents MUST verify that `--title` and `--body` (or `--body-file`) parameters are explicitly defined with populated, non-default content.

4. **Prohibition on Merging Pull Requests**:
   - Agents MUST NEVER merge a Pull Request under any circumstances.
   - Prohibited actions include running `gh pr merge`, merging PR branches directly into `main`, or triggering automated merges.
   - Merging Pull Requests is strictly reserved for human maintainers or designated governance processes.

5. **Test Writing and Isolation Standards (Banned Synthetic-Only Mocks)**:
   - Every code modification MUST be verified by **both** an in-situ integration test (running against a real private fixture PDF, e.g., `Lesson-5.pdf` or `Lesson-6.pdf`) and an isolated unit test (using small public/synthetic inputs *if and only if* doing so adds isolated coverage value).
   - In-situ integration tests that require private fixtures MUST use a graceful skip mechanism (e.g., `@pytest.mark.skipif`) when the private fixtures repository is not present. This ensures that the public unit tests still run successfully in public GitHub Actions without access to private files.
   - Purely synthetic/mocked tests are banned from being the *sole* validation instrument. All code must prove fitness for purpose on real inputs.

6. **Mandatory GitHub PR Publication for Reviews**:
   - Every agent acting in a reviewer capacity MUST publish their formal review verdict (`APPROVED`, `CHANGES_REQUESTED`, or `CANNOT_VERIFY`), line-level review comments, and marked summary decision directly to the GitHub PR thread using the exact-head guarded publisher (`scripts/score2gp_publish_review.py` or the pinned review skill publisher).
   - Outputting reviews solely into the assistant chat, saving them only to local scratch files, or using raw unbound CLI calls (`gh pr review` / `gh pr comment` directly) that bypass exact-head binding, summary markers, and post-publication verification is strictly prohibited.
   - The reviewer must verify that the formal review, inline comments, and marked summary comment are live on GitHub before completing the task.
