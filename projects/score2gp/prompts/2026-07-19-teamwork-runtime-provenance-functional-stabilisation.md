# Teamwork Prompt: Runtime Provenance And Functional Stabilisation

Run the Runtime-Provenance and Functional-Stabilisation Programme unattended.
The objective is a committed, reproducible conversion path that can reach a
liveable baseline for Lessons 3-7 before any `whole_note_recogniser.py`
refactor. Do not ask for routine approval. Continue through role changes,
review, and rework. Agy must never merge a product or governance PR; after
acceptance it must prepare an external-merge handoff and must not promote
dependent work until an external maintainer has merged it.

## Start State

- Governance repository:
  `/home/tticom/work/score2gp-workspace/score2gp-agentops`
- Product repository:
  `/home/tticom/work/score2gp-workspace/score2gp`
- Private fixture directory:
  `/home/tticom/work/score2gp-workspace/score2gp-private-fixtures/fixtures/private`
- Read, in order: `AGENT_CONTROL.md`, `AGENT_PR_READINESS.md`,
  `ACTIVE_TASK.md`, `APPROVED_TASK_QUEUE.md`, and
  `programmes/2026-07-19-runtime-provenance-functional-stabilisation.md`.

Before any write, prove the automation identity:

```bash
test "$(gh api user --jq .login)" = "tticom-automation"
test "$(git config --local --get user.name)" = "tticom-automation"
test "$(git config --local --get user.email)" = "tticomautomation@gmail.com"
```

If an identity check fails, make no write and report the failure. Do not use
the maintainer identity as a fallback.

## Non-Negotiable Controls

1. Begin every task from `origin/main`; never use historical local branches as
   a base.
2. Never amend a published commit, force-push, push directly to `main`, use a
   bypass, delete an open PR branch, run `gh pr merge`, use `--admin`, use a
   merge API, or merge through a web UI. No programme exception applies.
3. Use one task branch and one PR per task. Fix review findings with new
   commits on that same branch.
4. Never describe an executable path, external OMR engine, timing source, or
   rest origin without exact SHA, function path, command, and artefact evidence.
5. Private PDFs, reference GPs, sidecars, and detailed reports stay in ignored
   work directories. Commit only code, public synthetic tests, and sanitized
   facts.
6. `--ref-gp` is diagnostic-only. It must never guide generation, thresholds,
   or branch logic.
7. No production condition may use a filename, bar number, title, fixed
   coordinate, or reference-GP value.
8. Reviewer contexts are adversarial: seek disproof before approval. A green
   suite or generated GP is not sufficient evidence.

## Execute FS-01R Now

As Developer, implement only FS-01R.

1. On a product branch based on `origin/main`, create a normal narrow revert
   for the merge commit that merged product PR #376.
2. Do not salvage, extend, or reimplement #376. The only intended product
   change is restoring the pre-#376 state.
3. Run focused tests for the reverted files and `git diff --check`. Open one
   product PR and state the exact reverted merge SHA in its body.
4. A fresh Reviewer context must inspect the exact head and verify the diff is
   solely the narrow revert. If it finds a defect, return to Developer, commit
   a normal follow-up, and review again without stopping.
5. If accepted, record `READY_FOR_EXTERNAL_MERGE`, the exact head SHA,
   validation, risks, and that FS-01 remains blocked. Do not merge the PR or
   create a governance promotion that assumes it has landed.

## Continue The Programme

After an external maintainer merges FS-01R, reread `ACTIVE_TASK.md` and
continue without asking:

- **FS-02:** reconcile the committed conversion entry point. If the user-facing
  auto-OMR behaviour is not on `main`, prove the divergence and either submit a
  clean, reviewed implementation of that route or explicitly discard it. Do
  not repair tuplets or rests until this is settled.
- **FS-03:** run the corpus through the committed route and capture the first
  divergence for each input.
- **FS-04:** select the highest-impact shared defect class and fix it in a
  small vertical PR. Trace evidence through the actual pipeline. Keep
  independent defects separate.
- **FS-05:** write the liveable-baseline decision before authorising a
  refactor. Do not call a baseline liveable while it still relies on timing
  refusal, untraced rests, or uncommitted runtime code.
- **FS-06/FS-07:** only after FS-05, plan and execute the compatibility-first
  `notation_omr` modularisation while preserving the corpus record.

## Genuine Stop Conditions

Stop only if credentials remain unavailable, no committed runtime can be
identified after the FS-01/FS-02 evidence work, a necessary operation would
violate the controls above, or no credible in-programme task or research pivot
remains. Before stopping, commit an AgentOps end-of-run report with completed
tasks, exact PRs, validated facts, unresolved divergences, and the next
smallest credible action.
