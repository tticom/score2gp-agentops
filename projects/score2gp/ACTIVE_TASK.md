# Active Task

**Task**: FS-02: Canonical Entry-Point Reconciliation - Reviewer Phase
**Authorised Role**: Reviewer
**Repository**: `tticom/score2gp` (product) and `tticom/score2gp-agentops` (governance)

## Status

APPROVED

## Task Authorised

Yes. The Runtime-Provenance and Functional-Stabilisation Programme is
authorized for unattended execution under its guarded continuation rules.

## Permissions and Boundaries

- Start from `origin/main` in both repositories. Do not use any historical
  branch or uncommitted implementation as a baseline.
- Implement only FS-01 as defined in
  `projects/score2gp/programmes/2026-07-19-runtime-provenance-functional-stabilisation.md`.
- The product change is limited to a reproducible, private-safe runtime
  provenance and corpus-harness capability. It must not change recognition,
  timing, MusicXML, ScoreIR, GPIF, or conversion semantics.
- Reuse or extend the existing private smoke tooling where appropriate. Private
  PDFs, GP files, MusicXML sidecars, and detailed diagnostics remain ignored.
- Create one product PR, obtain a distinct Reviewer verdict, address review
  findings on the same branch without amending or force-pushing, then use the
  guarded continuation protocol to move to FS-02.

## Completion Evidence

1. A commandable corpus harness writes an ignored machine-readable provenance
   record for each selected input.
2. The record proves product SHA, clean/dirty classification, executable and
   import path, command, sidecar SHA/provenance when present, output/report
   path, exit status, and refusal codes.
3. Public tests cover record validation and no private artefact is tracked.
4. A distinct Reviewer verifies the exact PR head and the reports distinguish
   observed facts from unknowns.

## Unattended Continuation

This task opts into the Visual Output Correctness Recovery Programme's
Unattended Consecutive Loop Protocol. After review, rework, or guarded merge,
agents must continue to the next required role or eligible task without routine
maintainer confirmation. Before a genuine stop, they must commit the required
human-focused end-of-run report in AgentOps.
