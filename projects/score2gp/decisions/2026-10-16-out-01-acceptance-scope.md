# 2026-10-16: OUT-01 acceptance 3 scoped to adapter-injected tags

**Trigger:** the OUT-01 author stopped on a contradiction I wrote into the task (PR 493, reviewed CHANGES_REQUESTED): acceptance 3 required an audit finding no tag absent from real references, but the default output already contains `<Barline>` (absent from every readable reference), while acceptance 4 requires the default output byte-identical to base. Both cannot hold.

**Decision (maintainer approved this amendment on 2026-10-16: "approved"; governance wrote it under the delegation that keeps tests that can fail on unfit code and accuracy to requirement):** acceptance 3 covers what the version adapter injects; the base writer's `<Barline>` is OMIT-02-FU1's scope. Acceptance 4 stays unchanged. No criterion is loosened: the negative tests and mutants required are the same, applied to the adapter.
