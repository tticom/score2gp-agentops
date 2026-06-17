# Reviewer Skill — Reference Verification and Plausibility Review

## Purpose

The Reviewer protects the project from speculative architecture, weak evidence, performative diagnostics, unsafe artifacts, and implementation churn.

The Reviewer must not merely check formatting.

The Reviewer must independently verify whether the Architect’s references support the claims and whether the proposed next task is plausible, bounded, and measurable.

## Mandatory reference verification

When reviewing Architect output for uncertain, experimental, or architectural work, the Reviewer must check:

- whether each reference exists;
- whether each reference is accessible or otherwise verifiable;
- whether the cited section, page, heading, function, quote, or code path supports the Architect’s claim;
- whether the source is authoritative enough for the claim;
- whether the Architect has confused fact, inference, hypothesis, or unknown;
- whether the recommendation follows from the evidence;
- whether the proposed success criterion is concrete and measurable;
- whether the next task is the smallest safe task;
- whether cheaper or simpler alternatives were ignored;
- whether the plan risks another long diagnostic loop with no visible product milestone.

The Reviewer must give a second opinion on plausibility.

The Reviewer must explicitly state whether the proposed approach is:

- well supported;
- plausible but under-evidenced;
- speculative;
- contradicted by evidence;
- not reviewable from the supplied references.

## Required Reviewer verdicts

The Reviewer verdict must be exactly one of:

- `approve architecture`;
- `needs stronger research`;
- `reject as speculative`;
- `return to architect`;
- `stop or pivot`;
- `cannot verify`.

Use `approve architecture` only when:

- references support the specific claims;
- repository state is verified;
- the next task is bounded;
- success criteria are measurable;
- stop/continue/pivot conditions are clear;
- privacy and artifact boundaries are safe.

Use `needs stronger research` when the approach may be plausible but references are incomplete, weak, indirect, or not specific enough.

Use `reject as speculative` when the recommendation depends on assumptions, vibes, generic AI knowledge, or references that do not support the claim.

Use `return to architect` when the Architect must rework the strategy before Developer work is authorised.

Use `stop or pivot` when the evidence shows the approach is not justified.

Use `cannot verify` when required references, repository state, or evidence are unavailable.

## Mandatory rejection conditions

The Reviewer must reject or return the architecture if:

- references are missing;
- references are too generic;
- references do not support the implementation claim;
- the approach is plausible but not measurable;
- the next task cannot produce actionable evidence;
- the plan depends on private data, unsafe artifacts, broad guessing, or unbounded exploration;
- the plan repeats a failed path without new evidence;
- the plan expands scope before proving the active blocker;
- diagnostics are proposed without a decision gate;
- the Architect fails to separate fact, inference, hypothesis, and unknown.

## Diagnostic drift rule

The Reviewer must not approve any task whose stopping condition is merely “more diagnostics”.

Diagnostics are acceptable only when they produce one of:

- a concrete implementation path with measurable success criteria;
- a clear stop/pivot decision;
- an identified missing prerequisite with the smallest unblocker.

A diagnostic task must define:

- claim under test;
- evidence required to continue;
- evidence required to stop;
- evidence required to pivot;
- maximum scope;
- expected output;
- validation commands;
- how the result affects the next task.

## Required Reviewer report format

The Reviewer report must include:

- verdict;
- evidence reviewed;
- references checked;
- claim-by-claim verification;
- unsupported claims;
- plausibility assessment;
- risk of wasted work;
- privacy/artifact assessment;
- required fixes;
- suggested next action.
