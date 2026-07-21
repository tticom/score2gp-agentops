# Active Task

**Task**: FS-03B: OMR Artifact Contract
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

FS-03B is the smallest implementation needed to establish that contract. It
does not authorise automatic `convert` integration, timing repair, recognition
logic, visual-output fixes, or refactoring.

## Permissions and Boundaries

- Begin a fresh product branch from `origin/main`; do not use an earlier spike
  or prototype branch.
- Implement a bounded artifact-contract helper for the existing `score2gp omr`
  route. Given a PDF and an OMR output directory, it must deterministically
  discover exactly one candidate MusicXML artifact, reject zero or multiple
  candidates, validate XML or MXL structure, and write a machine-readable
  manifest containing PDF and artifact SHA-256 values, product SHA, configured
  executable, discovery result, validation status, and explicit handoff path.
- The command must fail with stable, documented refusal codes for no artifact,
  multiple artifacts, malformed XML/MXL, and unbound or invalid artifact.
- Public tests must use synthetic output directories and fixtures or mocks;
  public CI must not require Audiveris. A private probe is optional evidence
  only and must remain ignored.
- Do not call `convert` from `omr`, do not make `convert` invoke `omr`, and do
  not change ScoreIR, GPIF, timing, recognition, layout, or refactor modules.
- Follow `PR_EVIDENCE_CONTRACT.md` before creating the product PR. Leave the
  PR open for independent review and human merge; never invoke a merge command.

## Completion Evidence

1. Unit tests demonstrate each discovery and validation failure mode and one
   valid XML/MXL manifest path without calling an external OMR binary.
2. The manifest makes the artifact path and explicit next `convert --musicxml`
   handoff unambiguous, without automatically running conversion.
3. Product verification is run from the canonical WSL executable, and private
   evidence remains ignored.
4. The product PR body contains a completed claim ledger and pre-submit
   challenge for its exact remote head.
5. A distinct Reviewer verifies the exact remote PR head. Agy leaves the PR
   for human merge and never invokes a merge command.
