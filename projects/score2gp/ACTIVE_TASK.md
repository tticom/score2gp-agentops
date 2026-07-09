# Active Task

**Task**: Req-132 / Task 82: Design consolidated diagnostics schema and CLI reporting format
**Authorised Role**: Architect
**Repository**: `score2gp-agentops`

## Status
APPROVED

## Task Authorised
Yes

## Completion Evidence
Architect must design the JSON schema, CLI display parameters, and output formats for consolidating semantic candidates, pitch mapping, and timeline previews into a single diagnostic report under Req-132, checking in the consolidated diagnostics schema document.

## 1. Baseline
- Req-131 read-only rhythm timeline diagnostics implementation is complete.
- Page-level semantic candidates and staff-level timeline previews are integrated in Python.

## 2. Context
Having completed the implementation of pitch and timeline previews, we can now design how these disparate diagnostic signals are merged into a single report schema and formatted for CLI display.

## 3. Goal
Create a consolidated diagnostics schema and CLI display format document.

## 4. Non-goals
- Do not modify product code in score2gp.
- Do not implement CLI print formatting in Python.

## 5. Scope
All changes must be within `score2gp-agentops`.

## 6. Suggested Work Branch
`governance/req-132-consolidated-diagnostics-schema-v0.1`

## 7. Required Validation
Check that the document defines JSON schema fields, CLI display tables, and error/validation reporting.

## 8. Acceptance Criteria
- Consolidated diagnostics schema document completed and approved.
- Defines fields, CLI table formatting, and validation constraints.

## 9. Next Steps
- Review Req-132 consolidated diagnostics schema design.
- Implement the consolidated report.
