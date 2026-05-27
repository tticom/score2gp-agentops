# ScoreToGP Rejected Claims

This document maintains a permanent historical record of rejected, unverified, or contradicted claims made during agentic development. Agents must consult this document to avoid repeating invalid failure interpretations.

---

## Active Rejected Claims

### 1. The Derek Trucks "Omitted Measures" / "Source Pair Inequivalence" Claim
- **Claim**: The Derek Trucks PDF omitted measures 15 and 16, proving that the PDF and GP/MusicXML are not equivalent arrangements.
- **Status**: **Contradicted** (visual inspection outranks generated summaries).
- **Reason**: Direct visual inspection of Page 2 of the printed PDF clearly shows that Measures 15 and 16 **do exist** on the printed sheet music with visible tab fret numbers.
- **Correct Interpretation**: The visual parser or system coordinate mapper failed to detect, segment, or index the final system/bar boxes correctly, causing the compiler to silently drop these playable fret candidates. The mismatch is a product pipeline extraction bug, not an oracle arrangement difference.
- **Governing Rule**: Do not claim source-pair arrangement mismatch or structural omissions unless supported by direct visual/page/system/bar evidence. If the visual score contradicts diagnostic output, **the diagnostic output is wrong**.

### 2. Handoff Quality Equals Conversion Quality
- **Claim**: The implementation was successful because the HANDOFF.md report is clean and well-formed.
- **Status**: **Rejected**.
- **Reason**: Handoff quality is a workflow metric, not a product correctness metric.
- **Governing Rule**: Report strict mode, remediation mode, semantic comparison, and generated-file existence separately.

### 3. Diagnostic Tables Are absolute Truth
- **Claim**: The diagnostic table shows no errors, proving the conversion is complete.
- **Status**: **Rejected**.
- **Reason**: Diagnostic tables are intermediate summaries and can mask, misclassify, or smooth over underlying geometry failures.
- **Governing Rule**: Cross-reference tables with raw generated files, validation logs, and direct visual evidence.

### 4. Output File Existence Equals Conversion Success
- **Claim**: The compiler succeeded because a `.gp` package was successfully written.
- **Status**: **Rejected**.
- **Reason**: Output existence only proves compile loop termination, not musical or semantic correctness.
- **Governing Rule**: Semantic round-trip comparison must pass before claiming conversion success.

### 5. Remediation Success Implies Strict Mode Success
- **Claim**: The pipeline works because allow_skip_unboxed=True built the ScoreIR.
- **Status**: **Rejected**.
- **Reason**: Skipping unboxed systems or applying system-wide fallbacks masks layout grouping errors.
- **Governing Rule**: Strict mode and remediation mode are separate states and must always be reported independently.
