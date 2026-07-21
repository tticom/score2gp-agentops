# Active Task

**Task**: FS-03A: Supported Timing-Source Route Architecture
**Authorised Role**: Architect
**Repository**: `tticom/score2gp` (read-only) and `tticom/score2gp-agentops`

## Status

PR_OPEN

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

FS-03A defines the smallest credible supported timing-source route before any
product implementation. It does not authorise FS-03 implementation, FS-04,
or refactoring.

## Permissions and Boundaries

- Read the product repository and existing public/private fixture evidence;
  do not modify product files.
- Write one governance architecture report and, if necessary, update only this
  active task to `PR_OPEN` on the task branch.
- Establish the contract for obtaining, validating, and recording a MusicXML
  timing source for `score2gp convert`.
- Assess the committed standalone `omr` command, its Audiveris dependency, and
  any other committed option. Classify unavailable or uncommitted routes as
  unavailable or uncontrolled; do not invent an integration.
- Define a corpus acceptance matrix for Lessons 3 through 7 and the first
  source-to-output divergence to address after a timing source exists.
- Keep the refactor deferred. `whole_note_recogniser.py` naming and package
  design are not in scope until the functional route is stable.

## Completion Evidence

1. A revision-bound source-to-output map for each candidate timing-source
   route.
2. A recommended supported route, with prerequisites, failure behaviour,
   provenance fields, and a reason it is preferable to the alternatives.
3. Explicitly deferred work and a narrowly scoped first implementation task.
4. No product code changes, no fixtures or generated artifacts committed, and
   a clean named-file diff.
5. A distinct Reviewer verifies the exact remote PR head. Agy leaves the PR
   for human merge and never invokes a merge command.
