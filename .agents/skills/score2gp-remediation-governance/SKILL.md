---
name: score2gp-remediation-governance
description: Governing the master remediation backlog for E2E PDF-to-GP conversion failures. Enforces the ban on synthetic tests, mandates real-world in-situ testing on private fixtures, and governs task promotions for barline inheritance, page indexing, and digit over-merging.
---

# Score2GP Remediation Governance Skill

## Purpose
This skill provides specific rules and checks for executing the Milestone 6 conversion failure remediation tasks safely. It ensures agents enforce testing against real fixtures and prevent regression of barlines, page indexing, and digit merging.

## Core Rules

### 1. Test Writing and Isolation Standards
* **Real-World Test Requirement**: Every code modification MUST be verified by an in-situ integration test loading `Lesson-5.pdf` or `Lesson-6.pdf` from the private fixtures repository.
* **Isolated Unit Test Requirement**: If isolated unit testing adds coverage value, write a separate unit test using public/synthetic inputs.
* **CI Portability**: All in-situ integration tests that require private fixtures MUST use a graceful skip mechanism (e.g., `@pytest.mark.skipif`) when the private fixtures repository is not present. This ensures that the public unit tests still run in public GitHub Actions.
* **Banned**: Purely synthetic/mocked tests are banned from being the *sole* validation instrument.

### 2. Snapping Tolerance & Synthesis Fallbacks
* **Tolerance Restriction**: Snapping tolerance `outer_tolerance` in `pdf.py` must remain at `24.0` points. Do not expand it.
* **No Synthesis**: The pitch-to-fret synthesis fallback (`synthesize_missing_tab`) is permanently disabled and removed to prevent fake fret/string assignments.

### 3. Workflow & Promotions
* Load `projects/score2gp/tasks/2026-08-09-master-conversion-failure-remediation-backlog.md` to review approved tasks.
* Maintain sequentially incrementing page measure indexing. Revert any commit that resets `next_bar_index` to 1 on page change.

## Verification Checklist for Reviews
Before promoting any task in Milestone 6:
1. Run `python3 scripts/score2gp_governance_audit.py` to check for leaks.
2. Confirm no private PDF files or debug logs are staged/committed.
3. Verify that the generated `.gp` file for Lesson-5 contains exactly `38` measures and matching note occurrences.
