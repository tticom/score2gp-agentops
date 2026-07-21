# Active Task

**Task**: FS-03C: Rootless Audiveris Runtime Probe
**Authorised Role**: Developer
**Repository**: `tticom/score2gp` and `tticom/score2gp-agentops`

## Status

APPROVED

## Task Authorised

FS-02 is complete. Its canonical WSL evidence is merged in
`reports/2026-07-20-fs02-canonical-entry-point.md`: the supported `convert`
route requires a supplied MusicXML sidecar, while the standalone `omr` command
is not called by `convert`.

The human maintainer selected Model 1 from
`reports/2026-07-20-second-unauthorized-merge-attempt.md`: Agy retains branch
and PR write access, while GitHub `Main_Protect` provides technical
containment. Agy must never run any merge command, merge API, `--admin`, or
bypass flag. Any further prohibited command attempt ends unattended execution
for the cycle and returns the task to `BLOCKED`.

FS-03A is complete: governance PR #339 was externally merged as
`5ba1514430d83ecda1b137fad402c9bb239fb36e`. Its architecture report establishes
that `convert` requires an explicit MusicXML sidecar and that the standalone
`omr` command has no proven artifact contract or supported handoff.

FS-03B is complete. Product PR #379 was externally merged as
`df6e5c8178794f0ea7f98d69e069a1be3593f176` from reviewed head
`60b0fa1622292f42032aa98f0b3d99e7b5240d29`. It establishes a public-testable
contract for the standalone `omr` command, but does not prove that an
Audiveris runtime is available or produces a usable sidecar in this WSL
environment.

FS-03C is an evidence-only runtime probe. It does not authorise automatic
`convert` integration, timing repair, recognition logic, visual-output fixes,
or refactoring.

## Permissions and Boundaries

- Start from fresh `origin/main` worktrees. Before writing, prove the WSL,
  identity, and edit-coherency gates in `AGENT_CONTROL.md`. Record the actual
  product SHA, CLI executable, import path, and clean/dirty status.
- Create any required fresh worktree under a new task-specific path. Do not
  remove, prune, force, switch, reset, clean, or otherwise modify any existing
  worktree, including a Codex or human-maintainer worktree.
- Use only the official Audiveris 5.7.0 Ubuntu 24.04 x86_64 release asset:
  `Audiveris-5.7.0-ubuntu24.04-x86_64.deb`,
  `https://github.com/Audiveris/audiveris/releases/download/5.7.0/Audiveris-5.7.0-ubuntu24.04-x86_64.deb`,
  SHA-256 `b7d26b9a90136af8ffaaba789f842c7e1593180fc0200faa82256c5c51eae426`.
  First prove `uname -m` is `x86_64` and Ubuntu is 24.04. Download into a
  unique ignored directory below product `work/` and verify that exact hash.
- Do not use `sudo`, `apt`, system-package installation, shell profile edits,
  or a Windows path. Do not modify the package or write outside the unique
  ignored probe directory. Use `dpkg-deb -x` to extract the verified package
  there, locate its supplied launcher, and invoke that launcher directly.
- Run the committed `.venv/bin/score2gp omr` command once against
  `tests/fixtures/pdf/generated_standard_staff_whole_note.pdf`, with the
  extracted launcher and a fresh ignored output directory. Inspect its
  manifest. If it yields a valid handoff artifact, run the committed explicit
  `convert --musicxml <that exact artifact>` command once on the same public
  fixture and retain its JSON report in the ignored directory.
- Do not change product source, tests, configuration, generated assets, or
  fixture expectations. Do not attempt an alternate OMR engine, patch the
  extracted package, invoke auto-OMR from `convert`, or change timing,
  recognition, ScoreIR, GPIF, layout, embellishments, or refactor modules.
- If download verification, extraction, launcher execution, artifact
  validation, or the explicit conversion handoff fails, preserve the exact
  refusal/error and write a bounded evidence report. This is a valid task
  outcome; do not claim an OMR route is supported and do not start an
  unapproved repair task.
- Write the sanitized evidence report only in AgentOps at
  `projects/score2gp/reports/2026-07-21-fs03c-rootless-audiveris-probe.md`.
  It must state the exact runtime, asset hash, commands, product revision,
  manifest statuses, handoff result, and first remaining failure. Open one
  governance PR from a fresh branch. In that same branch, change this task's
  status only to `PR_OPEN`; do not authorise a successor. Use
  `PR_EVIDENCE_CONTRACT.md`, leave the PR `PR_OPEN`, and never invoke any merge
  command or API.

## Completion Evidence

1. The report proves the pinned asset's hash before use and that all execution
   occurred in the canonical WSL worktree.
2. The report gives the standalone OMR manifest status and, when available,
   the exact validated handoff artifact plus one explicit `convert --musicxml`
   result from the same revision and public fixture.
3. The report classifies the route as `supported`, `unavailable`, or
   `unproven`; it does not infer recognition or visual correctness from file
   creation or a passing command.
4. No product-tracked files change and all downloaded, extracted, and generated
   artifacts remain ignored.
5. The governance PR body contains a completed claim ledger and pre-submit
   challenge for its exact remote head. Agy leaves it `PR_OPEN` for independent
   review and human merge.
