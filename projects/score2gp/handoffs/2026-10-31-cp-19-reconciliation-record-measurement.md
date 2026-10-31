# CP-19 reconciliation record measurement (partial author run)

Measured 2026-10-31 before adding the two backfills below.

## Requirement and baseline

> **Completion:** governance moves the task to `completed_tasks` and writes one dated reconciliation record in `projects/score2gp/handoffs/`, citing the PR, the reviewed head, the merge commit and the outcome.

Source: `projects/score2gp/TASK_RECORDING_CONVENTION.md`, section 4. The file was introduced in ORC-01 on 2026-08-24, but that initial version did not require a dated record. The quoted requirement first appears in PLAN-01 revision
`f7ca93c67247b02e0dfd1676646582acdcfe5e34` (2026-09-25).

Measurement source: authority revision 258 at AgentOps `4b0b13aa5af114443c64f68d51f1bf55c513c60b`.
The population is every entry added to `completed_tasks` after the requirement first appeared, compared by task ID with that revision. This avoids treating the 23 already-completed entries as new completions.

There are 77 subsequent terminal entries: 71 merged/completed tasks and 6 resolved tasks without a merged task PR. Of the 71, 4 have a dated completion record with the task ID, PR, full reviewed head, full merge commit and completion outcome; 67 do not. A promotion-only mention does not count as reconciliation.

## Dated completion records present

| Task | Existing record under `projects/score2gp/handoffs/` |
|---|---|
| DUR-03-FU1 | `2026-10-25-dur-03-fu1-reconciliation-omit-01-fu2-promotion.md` |
| MEM-01-FU1 | `2026-10-27-mem-01-fu1-reconciliation-cp-12-promotion.md` |
| CP-15 | `2026-10-30-cp-15-reconciliation-cp-16-promotion.md` |
| CP-16 | `2026-10-31-cp-16-reconciliation-cp-18-promotion.md` |

## Dated completion records absent before this change

- `PLAN-01`
- `GOV-03`
- `DUR-01`
- `CP-13`
- `DUR-02`
- `RES-REQ-0005`
- `OMIT-01`
- `OMIT-02`
- `OMIT-05`
- `LAYOUT-01`
- `MEM-01`
- `OMIT-03`
- `DUR-03`
- `OMIT-04`
- `CFW-04`
- `PARTIAL-01`
- `SCALE-01`
- `TUPLET-TAB-01`
- `PDF-GROUP-02`
- `TS-READ-01`
- `FIXTURE-GUARD-01`
- `UNREAD-01`
- `UNREAD-02`
- `PERF-01`
- `CFW-05`
- `PDFG-01`
- `OUT-01`
- `DUR-02-FU5`
- `SLIDE-01`
- `OMIT-02-FU1`
- `LETRING-01`
- `CFW-03`
- `HOPO-01`
- `MEM-02`
- `OMIT-02-FU4`
- `OMIT-05-FU2`
- `OMIT-04-FU3`
- `LAYOUT-01-FU1`
- `MEM-03`
- `OMIT-05-FU1`
- `RES-REQ-0003`
- `CP-10`
- `OMIT-04-FU1`
- `OMIT-01-FU1`
- `CP-06`
- `DUR-02-FU2`
- `OMIT-04-FU5`
- `PERC-01`
- `OMIT-03-FU1`
- `OMIT-04-FU2`
- `OMIT-03-FU3`
- `LAYOUT-01-FU3`
- `MEM-01-FU2`
- `OMIT-02-FU2`
- `OMIT-04-FU4`
- `DUR-03-FU4`
- `OMIT-03-FU4`
- `CP-12`
- `FND-02`
- `FND-06`
- `NPG-06A-FU1`
- `FND-03A`
- `FND-03B`
- `TRIP-01`
- `REFUSE-01B`
- `NPG-04A`
- `CP-18`

## Resolved entries (separate population)

These have no merged task PR, so the four-field merged-task check does not classify them as missing merged-task records. They are listed to account for every subsequent terminal entry.

- `PDF-GROUP-01`
- `BARTOTAL-01`
- `PDF-GROUP-03`
- `OMIT-01-FU2`
- `NPG-06A`
- `REFUSE-01`

`OMIT-01-FU2` has a dated record of its promotion, but no separate dated record of its later resolution was found. None of these six has a dated resolution record in the inspected directory.

## Choice, partial work and blocking prerequisite

Preserve the convention and add record generation to the reconciliation writer. This is the smaller honest policy change: it implements the existing requirement and needs no maintainer quotation authorizing a convention amendment.

This run backfills OMIT-01 and OMIT-02 using the recorded authority metadata. These are retrospective records dated when written; their historical reconciliation timestamps remain explicit. The other historical omissions are measured above, not silently declared repaired.

The actual writer is outside this repository: `launchers/reconcile_promote.py` under the workspace root. It imports `reconcile_task` from `scripts/score2gp_orca_control.py`, then directly writes the authority and active-task view. Its final writes contain no reconciliation record. No tracked repository file defines `reconcile_promote`.

The bounded assignment permits `scripts/*.py`, the convention, handoff Markdown and CP-19 tests only. Editing the external launcher is outside that contract. A repository helper without a caller change would leave the normal path unchanged; adding filesystem side effects to the reducer would obscure that missing integration. No implementation or convention amendment has been made.

Required continuation: authorize a change to the external launcher (or move its writer into a tracked, authorized entrypoint with a sanctioned caller update), then implement record generation, prove the skip-the-record mutant fails through that entrypoint, and run the mandated validation. No merge, review, audit or identity gate change is required.

Evidence limits: this is local historical inspection, not a fresh GitHub verification of the historical approvals or merges. The launcher must commit and publish any retained changes and create the exact-head handback; this run cannot claim publication. Skills pin: `c51d4469bff70ee90b2a99c0690d7c41554ba9de`.
