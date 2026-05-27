# ScoreToGP Acceptance Targets

Acceptance targets define what must be true before a change can be considered successful for any benchmark rung.

> [!IMPORTANT]
> **Product correctness is never confused with file generation or diagnostics.**
> - **Generated GP is not success.**
> - **Generated ScoreIR is not success.**
> - **Permissive/remediation output is not strict success.**
> A conversion is successful only when all safety gates are preserved and the **semantic round-trip status passes**.

---

## Universal Separate Reporting Statuses

Every review and implementation agent must report the following statuses separately. Under no circumstances may they be collapsed into a single pass/fail status:

1. **Strict Conversion Status**: Successful compilation under strict safety gates (`allow_skip_unboxed=False`) without warning suppressions or bypasses.
2. **Remediation / Diagnostic Status**: Successful compilation under permissive, skipped-system, or zero-barline recovery modes (`allow_skip_unboxed=True`) for debugging.
3. **Generated File Existence**: Physical presence of `.ir.json` and `.gp` output files in the work directory.
4. **Semantic Round-Trip Status**: Pairwise note comparison against the GP/MusicXML oracle (requires >90% string/fret match rates and 0 poor/unknown bars).

---

## Major Triads Lesson 3 Staged Acceptance Gates

To prevent agents from jumping to complete conversion without verifying individual layers, Major Triads Lesson 3 has the following staged acceptance gates:

### Gate MT3-A: Smallest Safe Page/Window
- **Criteria**: Successful extraction, grouping, and coordinate mapping of a single system or the first measure run in the score.

### Gate MT3-B: First Page
- **Criteria**: Full layout grouping (systems, staves, string lines, bar boxes) and candidate extraction for Page 1 of the lesson PDF.

### Gate MT3-C: Full Score Extraction/Layout
- **Criteria**: All pages of the lesson PDF successfully pass extraction, staff line tracking, and bar box grouping with 0 unboxed systems.

### Gate MT3-D: Strict Build-IR
- **Criteria**: The pipeline successfully runs `build-ir` in strict mode (`allow_skip_unboxed=False`) on the full score, writing a valid, schema-compliant `score.ir.json` file.

### Gate MT3-E: Semantic Round-Trip
- **Criteria**: Symmetrical extraction of notes from both the generated GP file and the original GP parent, achieving `fret_match_rate > 0.95` and `string_match_rate > 0.95` in the roundtrip report.
