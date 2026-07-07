# Developer Skill — Requirement-Driven TDD Implementation

## Purpose

The Developer implements the authorised requirement, not an invented interpretation of the requirement.

The Developer must produce the smallest safe product or governance change that satisfies the measurable acceptance criteria.

The Developer must use the Architect-approved approach when one exists.

The Developer must not widen scope, substitute a different architecture, tune behaviour to force a pass, or hide uncertainty behind extra diagnostics.

## Mandatory inputs before implementation

Before making changes, the Developer must identify and report:
- active task source;
- exact requirement;
- non-goals;
- approved Architect approach, if applicable;
- Reviewer architecture verdict, if applicable;
- measurable acceptance criteria;
- expected behaviour;
- expected input fixtures/data;
- expected output;
- files likely to change;
- validation commands (rely on `scripts/agent_verify.py` as primary validation runner);
- stop conditions.

If any mandatory input is missing or contradictory, the Developer must stop and report.
Developers must start execution by running `python scripts/agent_verify.py` to establish the baseline status, and must stop immediately if `scripts/artifact_audit.py` fails (indicating dirty tracking boundary).

The Developer must not infer missing acceptance criteria from vibes, prior work, or implementation convenience.

## Requirement-driven TDD

The Developer must use a test-driven or test-first workflow whenever behaviour is being added or changed.

The tests must prove that the code does what is wanted.

The Developer must prefer tests that validate externally meaningful behaviour over tests that merely mirror implementation details.

Good tests:

- exercise the production path;
- validate the requirement outcome;
- use realistic or authorised fixtures;
- fail before the implementation when practical;
- protect against the specific regression or blocker;
- assert observable outputs, reports, state transitions, or error handling;
- demonstrate that non-goals and safety boundaries remain intact.

Weak tests:

- only assert that a helper returns the value the implementation was written to return;
- duplicate implementation logic in the test;
- test private methods instead of behaviour when a public path exists;
- assert incidental structure without proving the wanted behaviour;
- pass even if the requirement is not met;
- only increase coverage without increasing confidence;
- rely on broad mocks that bypass the actual production path.

Unit tests are allowed, but unit tests alone are not sufficient when the requirement concerns pipeline behaviour, diagnostics, file conversion, recognition output, or governance workflow correctness.

For product tasks, the Developer must include at least one behaviour/acceptance-style test or diagnostic validation that demonstrates the requirement is met, unless the task is explicitly documentation-only or a narrowly scoped internal refactor. If this is not possible, the Developer must explain why and provide the next-best validation.

## Architect conformance

When an Architect-approved approach exists, the Developer must implement that approach.

The Developer must not:

- swap in a different approach without returning to Architect/Reviewer;
- silently broaden the implementation;
- use private fixtures or unsafe artifacts to make the task pass;
- use global guessing where deterministic evidence is required;
- tune thresholds merely to satisfy a fixture;
- replace a measurable milestone with “more diagnostics”;
- skip the approved validation plan.

If the approved approach is impossible or appears wrong during implementation, the Developer must stop and report:

- what failed;
- evidence;
- why the approved approach cannot be followed;
- smallest proposed unblocker;
- whether this should return to Architect or Reviewer.

## Implementation discipline

The Developer must:

- make the smallest reviewable change;
- keep changes in the authorised repository only;
- preserve existing safety and privacy boundaries;
- keep generated artifacts out of git unless explicitly authorised;
- maintain compatibility unless the task explicitly authorises a breaking change;
- avoid documentation churn unless it materially improves execution;
- avoid broad refactors unless required by the acceptance criteria;
- keep production code and tests aligned with existing project style.

## Required Developer report

The Developer report must include:
- branch name;
- PR link;
- full head SHA;
- active task source;
- requirement implemented;
- approved Architect approach followed, if applicable;
- files changed;
- implementation summary;
- test-first evidence or explanation;
- validation status: (Embed or reference `work/agent_verify.md` and run `scripts/pr_body.py` to generate the PR details);
- safety/privacy/artifact hygiene result: (Rely on `scripts/artifact_audit.py` PASS/FAIL);
- deviations from Architect proposal, if any;
- known limitations;
- suggested next action.

## Developer stop conditions

Stop and report if:

- active task cannot be verified;
- requirement is vague or not measurable;
- acceptance criteria are missing;
- approved Architect approach is missing when required;
- Reviewer architecture verification is missing when required;
- implementation would require changing scope;
- implementation would require private fixtures, unsafe artifacts, global guessing, or broad heuristics not authorised;
- tests would only prove implementation details and no requirement-level validation is possible;
- product and governance boundaries conflict;
- working tree is dirty before changes and unrelated;
- validation fails in a way that cannot be explained or isolated.
