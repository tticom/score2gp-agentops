# Active Task

**Task**: Task 109 — Remediation 05: Intuitive Human-Focused Error Reporting
**Status**: MERGED
**Assigned Identity**: tticom
**Authorised Role**: Supervisor
**Repository**: tticom/score2gp
**PR Branch**: `feat/remediation-05-human-error-reporting`
**Pull Request**: null
**Original Prompt**: `projects/score2gp/prompts/next/remediation-05-human-error-reporting.md`

## Context
When the system encounters conversion failures or unowned notes, it must not silently skip or favour failure, nor should it simply print stack traces. The system needs to accurately and intuitively report what went wrong. The report must be tied directly to the exact element in the document that caused the error (not just the document as a whole). The assumption is that the end user (a musician) is not computer literate and will not read a long technical document. Therefore, the report must be intuitive and as short as possible to convey the issue.

## Goal
Design and implement a human-focused error reporting system. When an error occurs (such as an unowned note, a capacity violation, or unrecognized chord), the system must generate a report that:
1. Clearly ties the error to the specific musical element and location in the original score.
2. Is intuitive and easily understood by a non-technical musician.
3. Is as short as possible while still conveying the necessary information.
*Note: This may require first generating a computer-literate technical report that is then processed into the final user-facing report.*

## Acceptance
- The conversion pipeline no longer fails silently or with cryptic tracebacks.
- Errors produce a concise, musician-friendly report.
- Error reports pinpoint the exact location (e.g., page, measure, staff, note) of the failure in the original document.
