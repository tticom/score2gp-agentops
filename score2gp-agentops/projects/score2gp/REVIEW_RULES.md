# ScoreToGP Review Rules

These rules govern reviews of agentic ScoreToGP development. They are control-plane rules and do not belong in ScoreToGP product code.

## Required Review Stance

The reviewer/architect agent must evaluate before writing the next prompt. A review that immediately drafts a new implementation prompt without first assessing evidence is incomplete.

Reviews must distinguish:

- Product correctness.
- Handoff quality.
- Evidence quality.
- Benchmark relevance.
- Safety of committed artifacts.

Handoff quality is not conversion quality. A clear prompt, neat summary, or well-structured report does not prove that ScoreToGP converted a score correctly.

## Evidence Ranking

Use this evidence order when sources disagree:

1. Direct source artifact inspection.
2. Visual comparison against the original score or known-good export.
3. Machine-readable product outputs, such as IR and GP exports.
4. Test and validation logs.
5. Diagnostic tables.
6. Generated summaries.

Visual/source evidence outranks generated summaries. Diagnostic tables are evidence, not truth.

## Required Separate Reporting

Every review must report these fields separately:

- Strict mode result.
- Remediation mode result.
- Semantic comparison result.
- Generated-file existence result.

Do not merge these into a single pass/fail summary. A file existing does not imply semantic correctness. Remediation success does not imply strict mode correctness.

## Review Checklist

- Confirm no private assets were committed.
- Confirm the target benchmark rung is appropriate.
- Confirm stress cases were not used as the first acceptance target.
- Confirm the implementation did not alter agent-control documents inside product code.
- Confirm the PR does not claim conversion progress beyond observed evidence.
- Confirm product tests and validation commands were run or explicitly marked unavailable.
- Confirm failures are classified by likely layer: extraction, parsing, IR semantics, export, rendering, workflow, or benchmark setup.

## Reviewer Output

A reviewer response should include:

- Findings ordered by severity.
- Evidence used.
- Missing evidence.
- Acceptance target status.
- Whether to accept, request changes, or narrow the next implementation prompt.
- A next prompt only after the evaluation is complete.
