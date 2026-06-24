# Active Task: Developer Implementation for Tab-Only Timing Policy A+B+C

## Repository
tticom/score2gp

## Current Governance State
Outcome C for tab-only rhythm inference has been verified. The Supervisor has authorised the A+B+C product policy. Developer implementation is now authorised and unblocked.

Decisions:
`projects/score2gp/decisions/tab-only-timing-policy-a-b-c.md`

## Product Baseline
- Product PR #323 is merged.
- Product baseline: `6afdd3195f37eca6e319caf33dbeccfbbf1d4b5c`

## Authorised Developer Task
The Developer must implement the A+B+C tab-only timing policy in `tticom/score2gp`.

1. **Inspect** existing CLI/API timing options and warning/diagnostic conventions.
2. **Preserve** default `--pdf-only-tab` approximate output where already supported.
3. **Ensure** approximate/default timing emits clear warning/provenance (e.g., preserving or strengthening `pdf_only_tab_inferred_timing`).
4. **Add/Wire** strict precise-timing rejection using the smallest suitable existing or new CLI/API option (e.g., `--require-precise-timing`).
5. **Ensure** precise mode does not accept tab-only missing-timing input as precise.
6. **Preserve** MusicXML/sidecar precise timing behaviour.
7. **Add** tests proving the policy behaviour.

## Required Acceptance Tests
1. **Default approximate mode**: Using an existing public tab-only fixture with insufficient timing evidence, the normal/default tab-only path succeeds and emits/retains a warning/provenance marker that timing is inferred/defaulted.
2. **Strict precise-timing mode**: Using the same or equivalent fixture, strict precise-timing mode fails cleanly and does not produce a misleading GP file.
3. **Error/warning content**: The warning/error explains that precise timing requires MusicXML/sidecar or explicit reliable timing evidence.
4. **Sidecar/precise path preservation**: Existing MusicXML/sidecar precise timing behaviour remains unchanged.
5. **Existing product tests**: Existing tests continue to pass.
6. **Artifact hygiene**: No private PDFs, GP files, screenshots, logs, dumps, or generated artifacts are committed.

## Non-Goals & Stop Conditions
Stop any agent that:
- Implements broad rhythm inference.
- Starts ML research or ML-assisted extraction implementation.
- Implements new tab stem/beam extraction.
- Implements standard-notation PDF-only timing inference.
- Changes MusicXML sidecar architecture.
- Produces generated GP/PDF artifacts in tracking.
- Ignores artifact/privacy constraints.

## Next Authorised Task
After Developer implementation is complete and merged into a product branch, the next task is Reviewer implementation conformance review.

## Developer Implementation Authorised
Yes (on a product branch in `tticom/score2gp`).
