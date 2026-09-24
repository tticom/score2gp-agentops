# WIN-01 / WIN-02 Out-of-Policy Merges - 2026-09-24

## Observed events

Merge policy (`ORCHESTRATION_STATE.json`, `merge_policy`): two approvals, an
approval of the exact merged head, a governance go, and no admin bypass.

| PR | Task | Merged at (UTC) | Merged by | Merged head | Merge commit | Deviation |
|---|---|---|---|---|---|---|
| tticom/score2gp-agentops#681 | WIN-01 | 2026-09-24T03:53:53Z | `tticom` | `ba99ff2fbf606efa2dbc7b4747a61e96e54ac8d4` | `78941b2824d24d7b35195f99f2acc53146927cd8` | One approval (review `5299557145`, tticomgov-code, APPROVED at the merged head) against a two-approval policy; no exact-head author handback for `ba99ff2`; authority still recorded `pull_request: null`, so the dispatcher reported `BLOCKED`. The reviewer recorded a maintainer authorisation to skip the dispatcher block for that review. |
| tticom/score2gp-agentops#682 | WIN-02 | 2026-09-24T06:06:23Z | `tticom` | `3d16e290bb3931f98f5491593b3a138107f0acee` | `cbf750b14d98123ff9bd4917375d592e4ab0876c` | WIN-02 was never promoted (`next_task_proposal`, status `PROPOSED`). Merged about three minutes after review `5300426043` (tticomgov-code, CHANGES_REQUESTED, verdict `CANNOT_VERIFY`) at the merged head; no approval. |

## Impact

- Neither merge changed product recognition code. Review `5300426043` found zero
  code defects in #682 and reported Windows full suite 306 passed / 1 skipped and
  Linux CI SUCCESS; its blocker was the unpromoted task and the failing
  governance audit, not the code.
- The merges left authority stale: `ACTIVE_TASK.md` still showed WIN-01 as
  `PROMOTED`, the governance audit failed on `main`, and the dispatcher failed
  closed for every role.

## Resolution

This reconciliation (authority revision 38) records WIN-01 and WIN-02 as
`COMPLETED` from live PR facts, with a `governance_note` on each, and promotes
the already-queued WIN-03 with its open PR 463.

The incident is recorded `RESOLVED` on the maintainer's explicit confirmation
below. Neither merge was an agent acting with `tticom` credentials (compare
`2026-07-20-unauthorized-agy-merge-incident.md`), so no credential containment
is required.

## Maintainer confirmation and decision (2026-09-24)

Requested by review `5302695196` (tticom-codex, CHANGES_REQUESTED at
`47b2dc6a69a26342ed68e338ab7e775f6d963ef6`). On 2026-09-24, in the session
that authored this PR, the maintainer `tticom` answered "yes" to "Did you
personally merge #681 and #682 from the `tticom` account?" and stated:

1. `tticom-codex` and `tticomgov-code` may merge; `tticom-automation` may not.
2. Every task must be reviewed and must receive an approval.
3. The two-approval gate exists to stop rogue merges; once a non-author
   approval has been given, the gate may be overridden.
4. Standing permission to proceed with the full task list.

`merge_policy` in `ORCHESTRATION_STATE.json` and the `CLAUDE.md` merge rules
still describe the stricter policy. Aligning them with this decision is left
to a separate governance task; this reconciliation does not change them.

## Carried-over non-blocking findings

From reviews `5299557145` and `5300426043`, not addressed by this reconciliation:

- `docs/agy-cycle.md` documents the deleted `scripts/agy-cycle`.
- Stale `projects/score2gp/prompts/next` files, including `go-dispatch.md:23`,
  still name agy-skills or scope work to `agent-runtime/`.
- The `merge_controller` role disagrees with `CLAUDE.md` for `tticom-codex`.
- `test_repository_tooling_is_python_only` uses a filesystem `rglob` rather than
  tracked files.
