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

5. **Prohibition on Synthetic-Data Unit Tests**:
   - Every Pull Request introducing or modifying tests for layout, barlines, digit extraction, or note alignment MUST NOT use synthetic JSON mocks or hardcoded mock-coordinate vectors.
   - All tests MUST load and assert against real-world private fixtures (e.g. `Lesson-5.pdf` or `Lesson-6.pdf`).
