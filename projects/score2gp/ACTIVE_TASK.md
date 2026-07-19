# Active Task

**Task**: FS-01: Runtime provenance baseline and corpus stabilisation harness - Developer Phase
**Authorised Role**: Developer
**Repository**: `tticom/score2gp` (product) and `tticom/score2gp-agentops` (governance)

## Status

APPROVED

## Task Authorised

Yes. FS-01R was externally merged as product PR #377. The Runtime-Provenance
and Functional-Stabilisation Programme may now begin its clean FS-01 baseline.

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
- Obtain a distinct Reviewer verdict and address review findings with normal
- follow-up commits. After acceptance, Agy must record
  `READY_FOR_EXTERNAL_MERGE` and the exact head SHA. It must never merge the
  product PR, merge a governance PR, use `gh pr merge`, use `--admin`, or push
  directly to `main`.

## Completion Evidence

1. A commandable corpus harness writes an ignored machine-readable provenance
   record for each selected input.
2. The record proves product SHA, clean/dirty classification, executable and
   import path, command, sidecar SHA/provenance when present, output/report
   path, exit status, and refusal codes.
3. Public tests cover record validation and no private artefact is tracked.
4. A distinct Reviewer verifies the exact PR head and the reports distinguish
   observed facts from unknowns.
5. Agy leaves the accepted PR `READY_FOR_EXTERNAL_MERGE`; FS-02 remains
   blocked until an external maintainer merges it.

## Unattended Continuation

This task opts into the Unattended Consecutive Loop Protocol for developer and
review rework only. After acceptance, Agy must prepare the external-merge
handoff and may continue only with an independent approved task. It must not
advance FS-02 until an external maintainer merges the product PR.
