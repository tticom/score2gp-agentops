# 2026-06-21: Post-PR 318 Record Completion and Authorise Rest Sequencing Architecture

## Context
Product PR #318 added the ability to deterministically extract `quarter_rest_candidate` objects from graphical flag fragments. The extraction safely handles multiple staves via spatial partitioning and propagates existing `staff_index` metadata.

However, the rest object is currently unconsumed by any downstream logic in the notation bridge.

## Decision
We authorise an Architecture diagnostic to formulate a deterministic sequencing model that consumes the `quarter_rest_candidate`.
The diagnostic must answer where in the pipeline the object becomes an event, how it affects note event order, and what testing strategies will guarantee correct behaviour without overclaiming or relying on brittle global spacing approximations.

## Active Blocker
`QuarterRestThenNotes.pdf` can now emit a `quarter_rest_candidate`, but the deterministic sequencing/bridge path does not yet consume that candidate as a rest-duration event. Therefore rest-aware timing is not proven.

## Next Task
Architect Task: Quarter-Rest-Aware Sequencing Architecture for QuarterRestThenNotes v0.1
