# ScoreToGP Evidence Register

This register catalogues and tracks all agentic claims and their corresponding verified statuses. Reviewer/architect agents must record entries in this schema to maintain repository transparency and historical review posture.

## Template

### [Evidence Entry ID / Title]

- **Claim**: The precise claim made by the implementation agent (e.g., "Visual DP system alignment resolved System 6 and restored 100% of lead notes").
- **Source**: Local feature branch name, commit hash, or PR number.
- **Evidence Type**: `visual` / `source` / `logs` / `generated_outputs` / `diagnostic_tables` (visual comparison and source files outrank summaries).
- **Status**: `verified` / `unverified` / `contradicted` / `blocked` (a claim is verified only when supported by coherent, reproducible evidence).
- **Artifact Location**: Local workspace folder path or brain artifact path (e.g. `work/roundtrip_eval_clean_2026_05_27_reconciled`).
- **Private-Safe Summary**: Anonymized metrics and safe structural counts without exposing private musical text or fret sequences.
- **Review Decision**: `approve` / `keep_draft` / `request_changes` / `close_supersede`.
- **Next Required Evidence**: Exact evidence or Synthetic reproducing fixture required to resolve unverified/contradicted claims.

---

## Active Evidence Log

### EV-001: Derek Trucks Stress-Research Mismatched Measures

- **Claim**: Derek Trucks PDF omitted measures 15 and 16; source-pair inequivalence was proven.
- **Source**: branch `bugfix/gp-exported-pdf-layout-research-v0.1`, PR #137
- **Evidence Type**: `visual` / `diagnostic_tables`
- **Status**: **contradicted**
- **Artifact Location**: `work/roundtrip_eval_clean_2026_05_27_reconciled/roundtrip_report.json`
- **Private-Safe Summary**: The raw visual PDF inspection of the printed pages clearly shows that Measures 15 and 16 exist and feature visible tab fret numbers. The diagnostic parser failed to capture or associate the candidates, leading to a false "omitted measures" claim.
- **Review Decision**: **keep_draft** (PR remains in Draft state).
- **Next Required Evidence**: Investigation of visual PDF coordinate mapping, string line detection boundaries, or system barlines on the final page of the PDF to determine why these measures were ignored by the extraction engine.
