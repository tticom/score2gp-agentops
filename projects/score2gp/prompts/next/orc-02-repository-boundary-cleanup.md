# ORC-02: Repository Boundary Cleanup

## Objective

Isolate the three repositories by purpose:

- `tticom/score2gp` contains production-targeted code, tests, schemas, fixtures,
  and product documentation.
- `tticom/score2gp-agentops` contains agent governance, workflow,
  orchestration, operational scripts, task state, and durable evidence.
- `tticom/agy-skills` contains AGY-focused skills and explicitly justified
  harness-neutral material, without Claude-only artifacts.

## Required approach

1. Inventory Claude-specific, harness-specific, and legacy artifacts in all
   three repositories. Classify each as `REMOVE`, `MOVE`, `RETAIN_COMPATIBILITY`,
   or `RETAIN_ACTIVE` before changing it.
2. Trace references from bootstrap files, scripts, CI, plugin manifests,
   prompts, task records, and documentation. A file is not obsolete merely
   because it is old or not imported by Python.
3. Preserve durable task, review, and evidence records. If a record moves,
   preserve provenance and update every surviving pointer.
4. Keep production implementation changes out of this task. Repository
   relocation and documentation changes are allowed; product behavior changes
   require a separate product task.
5. Remove Claude-only artifacts from `agy-skills` and make AGY the primary
   runtime focus. Retain a compatibility artifact only with a written reason
   and a named owner.
6. Add or update deterministic boundary checks so stale references and
   reintroduced forbidden artifacts fail validation.

## Acceptance evidence

- A cross-repository inventory records every removed, moved, retained, and
  compatibility artifact with its reason and destination.
- Clean checkouts of all three repositories contain no active pointer to a
  removed artifact.
- `score2gp` contains no agent governance/workflow operations that belong in
  AgentOps.
- `score2gp-agentops` contains the canonical operational workflow and durable
  task evidence.
- `agy-skills` contains no unapproved Claude-only plugin, instruction, or
  installation artifact.
- Boundary/reference checks, repository tests, and `git diff --check` pass.

## Stop conditions

Stop and request architectural direction if removing an artifact would delete
durable evidence, break an active workflow, move production source or tests,
or require choosing between incompatible harness contracts without an explicit
decision.
