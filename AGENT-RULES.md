# Agent Rules

## Global rules

1. Keep private copyrighted or licence-unclear fixtures local and untracked.
2. Do not place private PDFs, GP files, MXL/MusicXML files, screenshots, overlays, logs, or generated conversion artifacts in Git.
3. Use sanitized evidence only: counts, statuses, warning categories, command names, and artifact paths.
4. Do not claim full PDF-to-GP conversion works unless proven by reproducible tests.
5. Prefer public fixtures for automated tests.
6. Do not let multiple agents edit the same source worktree.
7. Do not allow documentation-only churn to masquerade as implementation progress.
8. Every proposed implementation slice must have a test or a clear explanation of why no test is possible.

## Role ownership

Architect:
- Researches, diagnoses failures, designs next changes.
- Writes architecture plans into score2gp-control.
- Does not edit implementation code.

TPO / Sceptic:
- Challenges the plan.
- Defines acceptance criteria and fake-progress blockers.
- Writes acceptance criteria into score2gp-control.
- Does not edit implementation code.

Developer:
- Reads controller docs.
- Implements only in the developer worktree.
- Updates implementation log in score2gp-control.
- Runs tests.

Reviewer:
- Reviews developer diff and test evidence.
- Writes review report into score2gp-control.
- Does not implement unless explicitly asked.

Human / Conductor:
- Decides whether to merge, revise, split, or stop.
