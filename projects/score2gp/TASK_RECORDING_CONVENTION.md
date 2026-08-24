# Task Recording Convention

To prevent the proliferation of scattered task lists, prompt recordings, and unmaintained queues, all tasks, actions, tests, and outcomes must strictly follow this lifecycle convention.

## 1. Task Definition & Planning
All pending tasks and backlog items must be recorded in the machine-readable Orca control plane state.

- **Authority:** `projects/score2gp/ORCHESTRATION_STATE.json`
- **View:** `projects/score2gp/ACTIVE_TASK.md` (Auto-generated from JSON; never edited manually).
- **Backlog:** Tasks awaiting execution are formally defined in `projects/score2gp/APPROVED_TASK_QUEUE.md` or as `next_task_proposal` in the JSON.

Do **not** create ad-hoc `TASKS.md` files or sub-folder backlogs.

## 2. Action & Test Recording
Agent implementation actions and test plans are tracked at the Pull Request level, not via local file recordings.

- **Prompt Definition:** The instructions for a given task must exist as a single `.md` file in `projects/score2gp/prompts/next/`.
- **Validation Commands:** The test commands required for a task are defined in the task's JSON payload in `ORCHESTRATION_STATE.json` under `validation_commands`.

Do **not** archive chat logs or raw terminal outputs into `runs/` or `archive/` folders.

## 3. Outcomes & Evidence
The outcome of a task is recorded permanently on the GitHub Pull Request itself using standard templates, ensuring outcomes remain tied to their exact code SHAs.

- **Implementation Handback:** The developer agent must submit their completion state as a PR comment following the format in `templates/PR_BODY_TEMPLATE.md` and `PR_EVIDENCE_CONTRACT.md`.
- **Reviewer Ledger:** The independent reviewer agent must record the test outcomes (including negative controls) and final verdict using `PR_REVIEW_TEMPLATE.md`.
- **Merged State:** Once a task is merged, it is automatically shifted into the `completed_tasks` array within `ORCHESTRATION_STATE.json`.

## Summary of the "Single Source of Truth"
1. **What to do:** `ORCHESTRATION_STATE.json`
2. **How to do it:** `prompts/next/<task>.md`
3. **What happened:** The Pull Request handback, review comments, and check runs.
