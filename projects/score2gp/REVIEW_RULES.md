# ScoreToGP Critical Review Rules

These rules govern reviews of agentic ScoreToGP development. They are control-plane rules and live exclusively in the governance repository.

## 1. Required Posture: Sceptical Reviewer

The reviewer/architect agent must act first as a **sceptical reviewer**, not as a progress narrator or cheerleader. 

- **Default Stance**: Sceptical. Assume the implementation has introduced subtle regressions, silent coordinate bypasses, or brittle heuristics until verified otherwise.
- **Passing Tests Are Insufficient**: A PR with 100% green passing tests can still be wrong. The tests might assert implementation copies rather than exercising the production path.
- **Diagnostics Are Insufficient**: A PR with more diagnostics can still be wrong. Scaffolding is not correctness.
- **GP File Existence Is Insufficient**: A PR that successfully writes GP files can still be wrong. File existence is not conversion success.
- **Local Metric Improvement Is Insufficient**: A PR that improves one private metric while worsening or invalidating other benchmarks can still be wrong.
- **Oracle Integrity**: A PR that changes the oracle or benchmark baseline must prove source-pair equivalence and re-establish the baseline before claiming progress.
- **No Hope-Based Approvals**: Never approve a pull request because the direction "seems promising" or the code is "cleaner." Approve only when strict acceptance criteria are met with coherent evidence.

---

## 2. Required Terminology

Do not describe work as a "breakthrough," "success," "fix," or "improvement" unless supported by coherent evidence. Use only the following precise terms:

- **claimed**: The implementation agent asserts a result without complete reproducible evidence.
- **verified**: The claim is supported by a coherent, single-run, reproducible artifact set, local checks, and visual validation.
- **unverified**: The claim lacks coherent supporting evidence or has missing/stale logs.
- **contradicted**: Visual or source evidence directly refutes the claim (e.g. claiming a measure is omitted when visual inspection shows it exists on the page).
- **blocked**: Development is halted due to verified arrangement mismatches, missing inputs, or safety gate conflicts.

---

## 3. Evidence Hierarchy & Disagreements

Use this order of authority when sources disagree:

1. **Direct source artifact / visual page inspection**: The printed PDF or GP vector data.
2. **Coherent, single-run generated files** (IR and GP package exports).
3. **Machine-readable validation logs and tests**.
4. **Diagnostic tables**.
5. **Generated summaries**.

> [!IMPORTANT]
> **Visual/source evidence outranks generated summaries.** If the visual/source score contradicts diagnostic tool output, **always assume the diagnostic output is wrong** and investigate the tool first. 
> If artifacts disagree (e.g. summary.json and roundtrip_report.json show conflicting states), **stop evaluation immediately** and require artifact reconciliation.

---

## 4. Required Separate Reporting

Every PR review must report the following result channels as separate, independent fields:

- **Strict Mode Result**: Safety gates, grouping completeness, and build-ir execution without permissive bypasses.
- **Remediation / Diagnostic Result**: Softened gates, unboxed system skipping, or system-wide fallbacks used for debugging.
- **Semantic Round-Trip Result**: Match rates, string/fret accuracy, and poor/unknown bars.
- **Generated-File Existence**: Whether ScoreIR or GP package files were written.
