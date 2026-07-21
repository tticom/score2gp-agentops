# Credential-Boundary Reactivation

## Decision

The human maintainer selected the local-preparation operating model after the
FS-03C prohibited merge-attempt incident. Agy may prepare only local commits in
new task worktrees. Codex, authenticated as `tticom-codex`, is the independent
publisher and merge operator for protected pull requests.

## Verified State

Verification on 2026-07-21 established:

| Control | AgentOps | Product |
| --- | --- | --- |
| `tticom-codex` collaboration | `write` | `write` |
| `tticom-automation` collaboration | `read` | `read` |
| `Main_Protect` enforcement | active | active |
| protected rules | pull request, deletion, non-fast-forward | pull request, deletion, non-fast-forward |
| required approvals | one, independent of last pusher | one, independent of last pusher |
| required resolved threads | yes | yes |
| WSL GitHub CLI available to Agy | no authenticated hosts | same shared WSL state |

Neither ruleset has a bypass actor for `tticom-automation`. The protected PR
rule remains the sole route to `main`; direct pushes, branch deletion, and
non-fast-forward updates remain blocked.

## FS-03C Reactivation Boundary

The previously discarded FS-03C probe is not evidence. A fresh run must start
from current product `origin/main`, use the pinned Audiveris asset, and follow
the exact evidence-only task limits in `ACTIVE_TASK.md`.

Agy must leave the result as a local `agy/` branch and report its exact commit
SHA. Codex will reproduce the review in an independent clean worktree, create
the remote pull request only when its claim ledger is accurate, and merge only
after the required independent approval.

## Non-Goals

This reactivation does not assert that Audiveris output is a supported
Score2GP route. It does not permit automatic OMR integration, timing repair,
recognition changes, visual-output changes, or the planned module refactor.
