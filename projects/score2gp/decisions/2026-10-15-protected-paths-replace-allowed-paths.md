# Decision: protected paths, not a per-task file allowlist (2026-10-15)

## Maintainer decision

On 2026-10-15 the maintainer asked whether the `allowed_paths` protocol should be removed or specified more carefully,
favoured removing the restriction ("Historically restrictions were added to constrain antigravity, we're not using it
anymore"), and approved the change ("Yes to the protocol change"). The goal is a smooth, hands-free but accurate
development process.

## Evidence

UNREAD-02 (percussive strikes) stopped five times at the scope gate (score2gp-agentops #782, #783, #785, #786 and the
`compare.py` amendment). Each stop found a real consumer or superseded assertion that no one could name in advance, and
each cost one stop, one governance PR, one review and one relaunch. No stop caught a bad edit.

No control-plane code compares an author's diff with `allowed_paths`; the field is passed to the author as an
instruction and non-empty is the only validation. The real controls are the non-author review, the executor merge, the
exact-head CI, the real-source acceptance and the byte-preservation of bars written at base.

## Rule

1. A task keeps `allowed_paths` as the **expected area** and the author's starting scope. It may be broad
   (`src/**`, `tests/**`, `docs/**`).
2. A task may also carry `protected_paths` (a list of globs). An author **never** edits a protected path; touching one is
   a hard stop that is reported with the path. The default protected set for product tasks is:
   - `.github/**` (CI and automation);
   - `fixtures/private/**` and any reference `.gp`/PDF (the oracles and evidence);
   - `AGENTS.md`, `CLAUDE.md`, `HANDOFF.md`, `TESTING.md`, `PRIVACY.md` (agent and process instructions);
   - the control plane in AgentOps: `scripts/score2gp_*`, `projects/score2gp/ORCHESTRATION_STATE.json`, prompts, skills.
3. A path outside `allowed_paths` and outside `protected_paths` may be edited when the change is **required by the task**
   (a consumer of a changed type, a test asserting a superseded refusal). It is never a stop. Every such path is listed in
   the handback under "paths outside the expected area", each with the reason.
4. Changing an existing assertion is allowed only to name the new behaviour the task introduces: the replacement
   evidence is listed with the old and new assertion; numeric and reference checks stay; no test is deleted or skipped.
   An assertion weakened without a replacing source reading is a REQUEST_CHANGES finding.
5. The reviewer receives the full changed-path list, checks each path outside the expected area against the stated
   reason, and checks that every protected path is untouched. An unexplained path is a blocking finding.
6. Unchanged: non-author review at the exact head, merge only through the executor, no gate weakened, acceptance rests
   on real approved sources, byte-preservation of previously written output, and a stop for protected paths or unclear
   intent.

## Rollout

- This PR makes `protected_paths` an optional validated task field passed to the author assignment, and rewrites the
  scope rule in `ORCHESTRATOR-RUNBOOK.md` and the developer skill.
- Existing promoted tasks are unchanged until they are next amended or promoted; new promotions use the rule above.
- UNREAD-02 moves to it by a later revision after run 8 ends, so a running author keeps one scope.
