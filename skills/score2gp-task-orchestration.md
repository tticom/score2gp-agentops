# Skill: Score2GP Task Orchestration

## Purpose
Supervise agentic development across `tticom/score2gp` and `tticom/score2gp-agentops` using a safe, evidence-driven loop. 
This skill is for orchestration, governance updates, task promotion, and agent prompt generation. It must not directly merge code or bypass human review.

## Core Rule
Never trust self-reports. Verify live repository state, changed files, commits, and PR status before advancing work.

## Default Loop
1. Verify current state.
2. Identify active blocker.
3. Confirm active task from governance (`projects/score2gp/ACTIVE_TASK.md`).
4. Generate a bounded agent prompt.
5. Developer implements one task on one branch.
6. PR is opened.
7. Reviewer performs hard review (via `score2gp-pr-hard-review` skill).
8. Human merges only after review passes.
9. Governance records completion and defines the next smallest safe task.
10. Repeat.

## Mandatory Pre-flight Checks
Before any product or governance task:
```bash
git status --short
git branch --show-current
git fetch --all --prune
git log --oneline --decorate --graph --max-count=20
```

## Branch & Workflow Rules
- No direct commits to `main`.
- One task, one branch, one PR unless explicitly stacked.
- Agents must never merge to `main`. Human merge is required.
- Do not let agents start the next product implementation until the governance PR defining the task is merged.

## Agent Prompt Template
When prompting a developer agent, use this exact structure:

```text
Title: <short task name>

Context:
<What the agent needs to know>

Current verified state:
<Only facts verified live or provided by human>

Goal:
<Concrete expected outcome>

Non-goals:
<What must not be attempted>

Constraints:
<Branch, privacy, architecture, testing, and scope constraints>

Required pre-flight checks:
<Commands>

Implementation guidance:
<Likely files and safe approach>

Validation:
<Targeted tests, full tests, smoke checks>

Acceptance criteria:
<Completion conditions>

Stop conditions:
<When to stop and report>

Reporting format:
- Branch name
- PR link
- Exact files changed
- Commit hash
- Commands run
- Test results
- Smoke result
- Privacy/artifact check results
- Known limitations
- Whether PR is ready for review
```

## Governance Completion Rule
After a product PR is merged:
1. Verify the merge live.
2. Record the merge commit.
3. Open a governance PR on `tticom/score2gp-agentops`.
4. Mark the completed task in `ACTIVE_TASK.md`.
5. Define the next task. Keep it as small and reviewable as possible.

## Score2GP-Specific Safety Rules
- Preserve real visual and geometry evidence.
- Do not synthesize plausible-looking geometry.
- Do not infer musical semantics unless explicitly authorised.
- Do not jump from diagnostics to recognition without a boundary review.
- Candidate diagnostics are read-only unless a later task changes that.
- `None` means not run or evidence unavailable. `[]` means run but no candidates found.
- Public fixtures are allowed only when already tracked or explicitly created for the repo.
- Private PDFs, GP files, screenshots, logs, and local debug dumps must not be committed.

## Stop Conditions
Stop and report instead of continuing if:
- Active task is missing or says no task is approved.
- Repo is dirty before work starts.
- Product and governance branches are out of sync.
