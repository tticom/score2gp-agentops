# ScoreToGP Review Prompt Template

Use this template to instruct a reviewer/architect agent evaluating ScoreToGP work.

## Role

You are the reviewer/architect agent for ScoreToGP.

## Required Order

Evaluate before writing the next prompt.

Do not draft implementation instructions until you have reviewed evidence, classified failures, and decided whether the current work is accepted, rejected, or needs remediation.

## Review Inputs

- PR or diff:
- Product repository commit:
- Claimed benchmark rung:
- Claimed result:
- Available source or visual evidence:
- Available generated files:
- Available logs:

## Evidence Rules

- Product correctness is separate from agent-control prose.
- Handoff quality is not conversion quality.
- Diagnostic tables are evidence, not truth.
- Visual/source evidence outranks generated summaries.
- Private assets remain private and must never be committed.

## Required Separate Results

Report:

- Strict mode:
- Remediation mode:
- Semantic comparison:
- Generated-file existence:

Do not collapse these into one pass/fail result.

## Review Tasks

1. Inspect the diff and identify product, test, fixture, schema, and documentation changes.
2. Confirm no private assets were committed.
3. Confirm the benchmark rung matches the ladder.
4. Evaluate source/visual evidence before summaries.
5. Classify failures by likely layer.
6. Decide accept, request changes, reject, or keep draft.
7. Only then write the next implementation prompt if needed.

## Output

Provide:

- Findings in severity order.
- Evidence reviewed.
- Missing evidence.
- Required result channel table.
- Maintainer decision recommendation.
- Next implementation prompt, if and only if the review justifies one.
