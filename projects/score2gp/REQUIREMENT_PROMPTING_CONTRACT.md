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
- reporting format;
- Incremental Progress Check.

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

1. Architect researches options and chooses Outcome A, Outcome B, or Outcome C.
2. Reviewer verifies the research and gives an architecture verdict.
3. Developer implements only after Outcome A or Outcome B architecture approval, unless the task is mechanical and explicitly exempt. Developer work must not occur if Outcome C is selected.
4. Developer uses requirement-driven TDD.
5. Reviewer verifies implementation conformance to:
   - the requirement;
   - the approved Architect proposal;
   - the acceptance criteria;
   - the privacy/artifact rules.
6. Reviewer verifies PR readiness separately.

The prompt must define what happens if any stage fails.

## Reviewer Prompt Requirement — Adversarial Verification

Any prompt that asks for architecture review, implementation conformance review, PR readiness review, or merge readiness review must explicitly invoke adversarial verification mode as defined in `projects/score2gp/AGENT_PR_READINESS.md`.

Reviewer approval must be earned from independently verified evidence. Architect, Developer, Orchestrator, or PR-body self-reporting must not be treated as evidence unless checked against source, diff, command output, tests, diagnostics, generated artifact inspection, PR metadata, CI/check status, or exact repository state.

Every reviewer prompt must require the Reviewer to:

- start from `cannot verify`;
- test the strongest failure modes before approving;
- label key claims as `verified`, `partially verified`, `not verified`, `contradicted`, or `out of scope`;
- reject summary-only approval;
- verify that the proposed next task is the smallest safe task;
- reject tasks that merely repeat prior evidence;
- define exact approved scope and exact excluded scope;
- require product-level tests or diagnostics for recognition, export, conversion, pipeline, or workflow behaviour.

Reviewer prompts must not ask the Reviewer to “confirm,” “approve if reasonable,” or “check whether this looks good.” They must ask the Reviewer to find blockers, missing evidence, false progress, unsafe scope expansion, and unsupported readiness claims.

## Mandatory Architect Decision Gate for Note Recognition

For uncertain, technical, experimental, architectural, product-changing, or behaviour-changing note-recognition work, the Architect must not end with an unbounded diagnostic recommendation.

The Architect must choose exactly one of:

1. **Outcome A — Raster path is viable:**
   Provide a concrete measurable raster approach, references, validation plan, and the smallest next Developer task.
2. **Outcome B — Raster path is not viable but another approach is:**
   Provide the alternative approach, references, why it is more viable than raster, validation plan, and the smallest next Developer task.
3. **Outcome C — No currently viable approach:**
   State that Score2GP cannot currently progress toward reliable note recognition under present constraints. Identify the missing prerequisite and the smallest unblocker, if one exists. Do not authorise Developer work.

The wording must make clear:
* The Architect must not end with an unbounded diagnostic recommendation.
* “Do more diagnostics” is only acceptable if it is bounded by a specific hypothesis, fixture set, metric, expected result, pass/fail threshold, and stop/pivot condition.
* If the Architect cannot choose A, B, or C with evidence, the correct result is failure/cannot justify next implementation, not another vague research task.

## Reviewer Prompt Requirement — Adversarial Verification

Any prompt that asks for architecture review, implementation conformance review, PR readiness review, or merge readiness review must explicitly invoke adversarial verification mode as defined in `projects/score2gp/AGENT_PR_READINESS.md`.

Reviewer approval must be earned from independently verified evidence. Architect, Developer, Orchestrator, or PR-body self-reporting must not be treated as evidence unless checked against source, diff, command output, tests, diagnostics, generated artifact inspection, PR metadata, CI/check status, or exact repository state.

Every reviewer prompt must require the Reviewer to:

* start from `cannot verify`;
* test the strongest failure modes before approving;
* label key claims as `verified`, `partially verified`, `not verified`, `contradicted`, or `out of scope`;
* reject summary-only approval;
* verify that the proposed next task is the smallest safe task;
* reject tasks that merely repeat prior evidence;
* define exact approved scope and exact excluded scope;
* require product-level tests or diagnostics for recognition, export, conversion, pipeline, or workflow behaviour.

Reviewer prompts must not ask the Reviewer to “confirm,” “approve if reasonable,” or “check whether this looks good.” They must ask the Reviewer to find blockers, missing evidence, false progress, unsafe scope expansion, and unsupported readiness claims.

## Mandatory Incremental Progress Rule

Every agy prompt must identify the smallest project-forwarding outcome it will produce.

A valid task must produce at least one of:
* new decision-useful evidence that was not already available;
* new verified product capability;
* a required governance state change;
* a bounded review verdict that changes merge/readiness/blocker state.

A task is invalid if it only:
* repeats existing diagnostic output;
* copies evidence from an already merged PR into a product PR;
* creates a report from already-known data without adding new analysis, decision criteria, or implementation consequence;
* says “more diagnostics needed” without a bounded hypothesis, fixture set, metric, expected result, pass/fail threshold, and stop/pivot condition;
* creates documentation churn that does not change execution, decision-making, or project state.

Exception:
Recording previous results should normally be included as the first section of the next development-cycle task. Standalone recording tasks are allowed only when they record completion, authorise next work, update policy, change active governance state, or change readiness/blocker status. Product PRs must not be used merely to repackage prior evidence.

Speed, volume, formatting quality, and rapid PR creation are not success criteria unless the task produces verified progress over the stated baseline.

## Required Prompt Field

Every task must define a Progress Baseline before the Incremental Progress Check.
The baseline must name the existing evidence/state being built from:
PR/report/diagnostic/decision/fixture result/product capability/blocker/review verdict.

Every future agy prompt must include an explicit `Incremental Progress Check` answering:
* What new evidence, capability, governance state, or review verdict will this task produce?
* Which prior result must it not merely repeat?
* How will we know the task moved the project forward?
* What exact result means the task should stop as duplicate/no-progress?
* What is the smallest next decision this task enables?

The Incremental Progress Check must explicitly compare the proposed task result against that baseline.

The task is not ready if:
* the baseline is missing;
* the baseline is vague;
* the baseline is false or unverified;
* the task output would merely repeat/reformat/repackage the baseline;
* the task cannot explain what smallest next decision it enables.

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
