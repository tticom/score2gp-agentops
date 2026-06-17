# Score2GP Requirement Prompting Contract

## Purpose

The requirement writer is responsible for producing specific, measurable, bounded prompts that agents can execute and reviewers can verify.

A weak prompt causes weak work. The requirement writer must not delegate ambiguity to the agents.

## Mandatory prompt structure

Every product or governance task prompt must include, where applicable:

- title;
- context;
- current verified state;
- active blocker;
- goal;
- non-goals;
- repository scope;
- branch suggestion;
- required pre-flight checks;
- Architect research requirement, if uncertain;
- Reviewer architecture verification requirement, if uncertain;
- implementation guidance;
- required tests or validation;
- acceptance criteria;
- stop conditions;
- privacy/artifact constraints;
- PR requirements;
- reporting format.

## Requirement quality bar

A requirement is not ready unless it answers:

- What exact outcome is wanted?
- What observable evidence proves it?
- What must not change?
- What assumptions are allowed?
- What assumptions are forbidden?
- What data/fixtures may be used?
- What data/fixtures must not be used?
- What counts as success?
- What counts as failure?
- What should cause stop or pivot?
- Which agent role owns each decision?

## Behaviour-first testing rule

Prompts must require tests that prove the code does what is wanted.

The requirement writer must not accept “add unit tests” as sufficient when the desired outcome is behavioural, diagnostic, pipeline, recognition, conversion, or governance workflow correctness.

Prompts should prefer:

- acceptance tests;
- regression tests tied to a known blocker;
- production-path tests;
- fixture-based tests;
- CLI/report tests;
- end-to-end diagnostic checks within safe scope;
- tests that fail if the requirement is not met.

Prompts may also require unit tests, but unit tests are supporting evidence, not the main proof, unless the task is genuinely a small pure function or internal helper.

## Single-task loop rule

When a task includes Architect, Reviewer, and Developer responsibilities, the prompt must define the loop explicitly:

1. Architect researches options and chooses Outcome A or Outcome B.
2. Reviewer verifies the research and gives an architecture verdict.
3. Developer implements only after architecture approval, unless the task is mechanical and explicitly exempt.
4. Developer uses requirement-driven TDD.
5. Reviewer verifies implementation conformance to:
   - the requirement;
   - the approved Architect proposal;
   - the acceptance criteria;
   - the privacy/artifact rules.
6. Reviewer verifies PR readiness separately.

The prompt must define what happens if any stage fails.

## Anti-vagueness rule

The prompt must not use vague goals such as:

- “improve recognition”;
- “make progress”;
- “try raster”;
- “add diagnostics”;
- “investigate”;
- “support future work”;
- “clean up”;
- “make it robust”.

Unless those phrases are accompanied by measurable success criteria, they are not valid requirements.

## Prompt writer stop condition

The requirement writer must stop and ask for clarification or create a governance task if:

- the requirement cannot be measured;
- success evidence cannot be named;
- scope boundaries are unclear;
- the next task depends on research not yet done;
- the next task would combine too many roles without a defined loop;
- the task risks another diagnostic loop without a stop/continue/pivot decision.
