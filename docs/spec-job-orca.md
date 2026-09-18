# Spec jobs in Orca

`plan/spec-job.example.yaml` is the planning format for a multi-ticket
implementation job. It names the specification, integration branch, and
dependency graph. It is not an execution authority.

Validate and resolve the ready frontier with:

```bash
python3 scripts/agy_spec_job.py plan/spec-job.example.yaml --json
```

The resolver fails closed for duplicate IDs, unknown blockers, dependency
cycles, inconsistent repositories or base branches, empty scopes, empty
acceptance, and empty validation contracts. A ticket is on the frontier only
when it is `READY` and every blocker is terminal.

Orca uses the output as planning input. For each selected frontier ticket it
must still create or update the versioned `ORCHESTRATION_STATE.json` authority,
capture live GitHub facts, resolve the current state, and generate the bounded
assignment with `score2gp_orca_control.py`. The job manifest never grants a
worker permission to edit, review, approve, merge, or select a successor.

The integration branch is a coordination pointer for the job. Existing
Score2GP policy remains one bounded task, one worker assignment, and one PR at
a time; adopting a single final integration PR requires a later policy change
and a separate merge-controller design. Until then, Orca can execute the
frontier safely while preserving the current exact-head and role gates.
