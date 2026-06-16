# Decision Record: 2026-06-16 Post-Task 169 — Authorise Task 170

## Context

Product Task 169 has successfully implemented the deterministic, read-only quality/coverage report `build_clef_resolved_pitch_coverage_report` and appended it to the recognition outcomes as `clef_resolved_pitch_coverage`. 

Product PR #289 was verified as merged with final head SHA `7b829866e107035d8ccf68de8142a57f60cb5ce9`. The report logic safely handles malformed input and correctly identifies boundaries like out-of-range pitches versus missing ledger lines.

Codex reviewed the changes, identified an issue with out-of-range notes being tracked as ledger line skips. This was fixed, the thread replied to, and natively resolved.

The next necessary action is to understand where the current clef evidence coverage stands on the existing corpora. Before writing more bridging logic or implementing more clef identification mechanisms, we must quantify exactly which failure cases (e.g., missing evidence, ambiguous evidence, missing ledger lines, or out of range) dominate our missed pitch-mappings. 

## Decision

We authorise Product Task 170 to execute this diagnostic analysis. 

Product Task 170 will run the newly built `clef_resolved_pitch_coverage` report against the authorized fixtures and document the findings. It will NOT alter pitch-mapping logic. The sole outcome will be a diagnostic findings summary that points clearly to the next most impactful recognition task (e.g. bridging missing clef candidates, relaxing ledger line strictness, etc.).

## Consequences

- We maintain a strict data-driven approach to recognition improvement.
- We will be able to target the most common mapping failure mode confidently in Task 171.
- No playable output or mapping semantic changes will be introduced in Task 170, maintaining the boundary.
