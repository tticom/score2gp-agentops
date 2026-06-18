# Mandatory Incremental Progress Rule

**Date:** 2026-06-18

## Context
A recent Product Task 175 follow-up branch produced a PR that only repackaged evidence already produced by a prior merged PR. That is not progress. It wasted a task slot, created review overhead, and did not reduce uncertainty or move Score2GP closer to reliable note recognition.

## Decision
All future agy prompts require an explicit Progress Baseline and an Incremental Progress Check. The check must explicitly compare the proposed result against the baseline. Speed, volume, formatting quality, and rapid PR creation are not success criteria unless the task produces verified progress over the stated baseline.

## Consequence
Reviewers must mark tasks or PRs NOT READY if the baseline is missing/vague/false, if the output merely repeats the baseline, or if no incremental evidence/capability/state/verdict was produced. Duplicate/no-progress PRs should be closed, not merged. Product PRs that merely repackage existing evidence are explicitly not mergeable.

## Exception
Recording previous results should normally be included as the first section of the next development-cycle task. Standalone recording tasks are allowed only when they record completion, authorise next work, update policy, change active governance state, or change readiness/blocker status.

## Relationship to Architect A/B/C Gate
Diagnostics must force a decision or stop, not create another loop. The Architect gate forces an outcome (A, B, or C). Unbounded diagnostics without a specific hypothesis, metric, and stop/pivot condition are strictly forbidden.
