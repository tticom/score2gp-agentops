# Mandatory Incremental Progress Rule

**Date:** 2026-06-18

## Context
A recent Product Task 175 follow-up branch produced a PR that only repackaged evidence already produced by a prior merged PR. That is not progress. It wasted a task slot, created review overhead, and did not reduce uncertainty or move Score2GP closer to reliable note recognition.

## Decision
All future agy prompts require an explicit Incremental Progress Check.

## Consequence
Duplicate/no-progress PRs should be closed, not merged. Product PRs that merely repackage existing evidence are explicitly not mergeable.

## Exception
Governance recording tasks may summarise prior merged work when explicitly authorised to record completion, authorise the next task, or update governance state.

## Relationship to Architect A/B/C Gate
Diagnostics must force a decision or stop, not create another loop. The Architect gate forces an outcome (A, B, or C). Unbounded diagnostics without a specific hypothesis, metric, and stop/pivot condition are strictly forbidden.
