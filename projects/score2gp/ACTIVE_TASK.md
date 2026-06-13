## Current Active Task

## Task 105 — Add first read-only whole-note recognition outcome mapping from validated candidates

Status: ACTIVE

Owning repo: score2gp

Context:
Product PR #258 has merged. It strengthened the diagnostics gate by making expected whole-note candidate counts explicit and fail-fast. That gives us safer evidence for the next product improvement. We need to move from diagnostics-only candidate counting toward visible product behaviour, starting with a small, reviewable read-only recognition/conversion outcome for the safe public generated whole-note fixture.

Goal:
Add first read-only whole-note recognition outcome mapping from validated candidates. The product task should consume existing whole-note candidate evidence and produce a read-only recognition/conversion outcome for the safe public generated whole-note fixture, without weakening gates or touching unrelated symbol recognition.

Next Step:
Execute Product Task 105 in the `score2gp` repository.
