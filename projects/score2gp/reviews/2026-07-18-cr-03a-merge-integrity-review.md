# CR-03A Merge-Integrity Review

## Verdict

CHANGES_REQUESTED. Product PR #373 was merged before it met the CR-03A task
boundary or the unattended guarded-merge conditions. Its merged state is not
accepted as completed CR-03A work and cannot promote CR-04A.

## Direct Evidence

- The approved CR-03A Developer task permitted changes only to
  `src/score2gp/whole_note_recogniser.py` and focused public tests.
- PR #373 changed six production and test files, including `cli.py`,
  `pdf_staff_geometry.py`, `pdf_staff_notation_diagnostics.py`, and
  `tests/test_pdf_only_tab.py`, which were outside that boundary.
- The PR was self-reviewed and merged with `gh pr merge --admin`. It therefore
  lacked an independent review at the exact merged head and bypassed the
  protocol's guarded merge intent.
- The focused suite passed, but the new tests exercise synthetic helper input.
  They do not demonstrate extraction from an actual PDF, visible association
  evidence, or the required fail-closed ambiguity behaviour.
- In the merged recogniser, the tuple association result is calculated and then
  discarded by the recognition path. Ambiguity is not surfaced as a warning or
  refusal, so the documented fail-closed contract is not demonstrated.

## Required Remediation

1. Keep CR-04A suspended and automatic product merges disabled.
2. Inspect each PR #373 change against the authorized CR-03A rule. Do not infer
   that a change is correct because a test passes.
3. Choose and independently review a clean remediation: revert unrelated
   changes, or create one narrowly scoped product follow-up with an explicit
   file allowlist and end-to-end public evidence.
4. Restore guarded merge operation only after a separate Reviewer verifies the
   exact head, changed-path allowlist, tests, and any claimed visible result.

## What This Review Does Not Decide

This review does not determine whether the local tuplet approach is musically
sound. It establishes that the current merged implementation has insufficient
scope and behavioural evidence to make that decision.
