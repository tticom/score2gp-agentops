# Safe Corpus Audit Fixture Policy and Manifest

**Date**: 2026-07-09
**Role**: Architect
**Scope**: Req-128 / Task 58 (Corpus Audit Policy definition)

## 1. Corpus Fixture Policy

To expand test coverage and audit the robustness of semantic candidates without compromising IP or privacy, the following hybrid policy governs the corpus audit:

- **Public/Generated Fixtures**: Only pristine synthetic or open-licensed public fixtures (e.g., standard staff Mutopia/generated PDFs) may be committed to the public Git repository. All test assertions inside standard Pytest execution must run exclusively on these public fixtures.
- **Private/Local-Only Corpus**: For large-scale real-world audits, developers may inspect local private PDFs. These files must be kept outside the tracked repository path or explicitly excluded via `.gitignore` to prevent any accidental leakage.

---

## 2. Invariant Rules for Private PDFs

1. **No Commits**: Private or copyrighted PDFs must never be added to any branch or committed to git under any circumstances.
2. **Local Inspection Only**: Analysis of private PDFs must be performed locally. Temporary intermediate assets (like rendered page PNGs or extracted diagnostic JSON files) generated during the audit must be placed in a directory ignored by git (e.g. `work/`, `tmp/`, or a dedicated `local_corpus/` folder added to `.gitignore`).
3. **No Private Benchmarks Leakage**: No artist names, track titles, or copyrighted lyrics/lyrics fragments may be stored in committed logs or metadata files.

---

## 3. Safe Audit Metadata Manifest

The following page and staff-level metrics are safe to record and commit in the audit report:
- **SHA-256 File Hash**: A cryptographic hash of the PDF to uniquely identify it without disclosing its contents.
- **Structural Metrics**: Page count, staff notation geometry system counts, staves per system.
- **Anonymized Layout Statistics**: Average staff height, staff line spacing ratios.
- **Candidate Counts**: Total extracted `LogicalClefCandidate` and `QuarterRestCandidate` objects.
- **Anonymized Audit Verdict**: E.g., `PASS`, `FAIL_CLEF_MISSING`, `FAIL_REST_MISIDENTIFIED`.

---

## 4. Error Classification Metric Policy

To measure audit accuracy, failures must be categorized as follows:
- **False Positive (FP)**: The classifier/heuristic extracts a candidate (e.g. treble clef or quarter rest) at a location where no such symbol exists in the score.
- **False Negative (FN)**: A valid treble clef or quarter rest exists in the score, but the heuristic fails to extract it.
- **Measurement Resolution**: Error counts are aggregated per PDF hash and summed to compute the overall error rate of the heuristic model.

---

## 5. Verification and Compliance

Any audit branch or PR must pass the following compliance checks:
1. **Git Check**: `git status --short` must not show any private/local PDF files or untracked binary files.
2. **Diff Check**: `git diff --check` to ensure no formatting or trailing whitespace violations.
3. **Artifact Audit**: Run `python3 scripts/artifact_audit.py` in the product repository to scan for forbidden private keywords or file leakages.
4. **Governance Audit**: Run `python3 scripts/score2gp_governance_audit.py` in the governance repository.
