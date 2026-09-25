# Task Recording Convention

There is one place for each kind of record. Planned work is recorded only in the task authority. `tests/test_single_backlog.py` enforces this. It also lists every live line that uses a planning-container word, verbatim, in its `REVIEWED_MENTIONS`: a new or reworded line fails until a reviewer accepts its entry in the PR diff.

## 1. What must be true: requirements

Requirements are recorded in `projects/score2gp/requirements/` (the register is its `README.md`). Every planned item cites the requirement it delivers, or a named control-plane need. A requirement below `ACCEPTED` has a research task (`RES-<REQ>`).

## 2. What to do: the task authority

All planned work lives in `projects/score2gp/ORCHESTRATION_STATE.json`:

| Field | Holds |
|---|---|
| `task` | The one active task |
| `next_task_proposal`, `queued_task_proposals` | Promotable tasks in the full proposal schema |
| the authority's `backlog` | Items not yet detailed enough to promote, in the light schema (`id`, `title`, `requirements`, `kind`, `repository`, `status`, `priority`, `depends_on`, `notes`) |
| `completed_tasks` | Finished tasks, with their PR, reviewed head and merge commit |

`scripts/score2gp_orca_control.py` validates the authority's backlog: schema, unique IDs, known dependencies and no cycles. It also computes the **ready frontier**: items with status `READY` whose dependencies are all terminal, in priority order. Governance promotes from the frontier by converting an item to the full proposal schema. `ACTIVE_TASK.md` is generated from the authority and never edited by hand.

Record planned work nowhere but the task authority: no `TASKS.md` files, sub-folder records or cycle files.

## 3. How to do it: task prompts

Each promoted task has exactly one prompt file, `projects/score2gp/prompts/next/<task>.md`. The prompt at the authority revision that promoted the task is the operative instruction. Its validation commands are in the task's `validation_commands`.

## 4. What happened: evidence

Outcomes are recorded where they stay tied to exact code:
- **Implementation handback:** the author's exact-head handback comment on the PR, published and read back by the handback publisher (`templates/PR_BODY_TEMPLATE.md`, `PR_EVIDENCE_CONTRACT.md`).
- **Review:** the independent reviewer's formal verdict, inline findings and marked summary at the exact head (`PR_REVIEW_TEMPLATE.md`).
- **Checks:** the PR's CI runs.
- **Completion:** governance moves the task to `completed_tasks` and writes one dated reconciliation record in `projects/score2gp/handoffs/`, citing the PR, the reviewed head, the merge commit and the outcome.
- **Research:** a research task records its findings in the requirement it serves, or in a dated record in `projects/score2gp/research/`.

Do not archive chat logs or raw terminal output. Dated record directories (`runs/`, `reviews/`, `reports/`, `decisions/`, `archive/`, `audits/`) hold history from earlier methods. They are not written to for new work.

## Summary

1. **What must be true:** `requirements/`
2. **What to do:** `ORCHESTRATION_STATE.json` (the task, proposals and the authority's backlog)
3. **How to do it:** `prompts/next/<task>.md`
4. **What happened:** the PR (handback, review, checks) and the governance reconciliation record
