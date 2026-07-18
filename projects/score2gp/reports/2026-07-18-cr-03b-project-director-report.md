# CR-03B Project Director Remediation Report

## Scope Drift
Product PR #373 merged commit (`40d061517523fcfe714d49c3aa4e7b3191d56a80`) violated the CR-03A boundary. The task explicitly restricted modifications to `src/score2gp/whole_note_recogniser.py` and tuplet association tests. However, the commit included significant unrelated features:
- Dotted note primitive extraction and diagnostics.
- Tie candidate extraction.
- CLI changes.
- Ref-GP mismatch refusal behaviour for TAB conversion.

These changes appeared in `cli.py`, `pdf_staff_geometry.py`, `pdf_staff_notation_diagnostics.py`, and `tests/test_pdf_only_tab.py`.

## Merge-Control Violation
The PR was merged using an administrative bypass (`gh pr merge --squash --admin`). This violated the strict guarded-merge protocol, which requires an independent Reviewer to verify the exact head commit and tests before merge. The self-review bypass circumvented governance.

## Test Coverage Gaps
The tuplet association logic added in `tests/test_tuplet_association.py` only validates the isolated synthetic association function (`extract_and_apply_tuplet_associations`). It does not verify that tuplets are successfully extracted from actual PDF documents, nor does it prove that the pipeline surfaces ambiguous tuplet failures properly rather than silently discarding them. The recognition path calculates the result but does not adequately prove the "fail-closed" ambiguity contract end-to-end.

## Per-Change Classification

1. **`src/score2gp/whole_note_recogniser.py` (Tuplet logic)**: Salvage with separate review. The code implements the requested geometric association, but must be verified to integrate correctly end-to-end and enforce fail-closed behaviour.
2. **`src/score2gp/whole_note_recogniser.py` (Dotted notes, chords, timeline chords)**: Revert. Out of scope.
3. **`src/score2gp/cli.py`**: Revert. Out of scope.
4. **`src/score2gp/pdf_staff_geometry.py`**: Revert. Out of scope.
5. **`src/score2gp/pdf_staff_notation_diagnostics.py`**: Revert. Out of scope.
6. **`tests/test_pdf_only_tab.py`**: Revert. Out of scope.
7. **`tests/test_tuplet_association.py`**: Salvage with separate review. Needs extension to cover end-to-end PDF integration or strict integration tests.

## Recommended Remediation Task (CR-03C)

To restore product integrity cleanly without complex untangling, the recommended remediation is to revert the entire `40d061517523fcfe714d49c3aa4e7b3191d56a80` commit. 

**Next Task: CR-03C: Revert CR-03A unauthorized scope**
- **Allowed-file list**: `src/score2gp/whole_note_recogniser.py`, `src/score2gp/cli.py`, `src/score2gp/pdf_staff_geometry.py`, `src/score2gp/pdf_staff_notation_diagnostics.py`, `tests/test_pdf_only_tab.py`, `tests/test_tuplet_association.py`.
- **Action**: Create a new branch `cr-03c-revert` from current product `origin/main`. Execute `git revert 40d061517523fcfe714d49c3aa4e7b3191d56a80 --no-commit`. Verify the git diff, commit, and push.
- **Validation**: `pytest tests/` must pass completely. `git log -1` must show a clean revert without touching any unrelated files.
- **Constraint**: Do not import recovery branches or PRs #371/#372.

Once CR-03C is merged, a new attempt at CR-03A (e.g. CR-03D) can be initiated to correctly implement the tuplet logic within strict bounds.
