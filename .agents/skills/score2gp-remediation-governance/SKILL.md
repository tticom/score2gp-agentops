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
* **Real-Source Unit/Contract Requirement**: Recognition, grouping, timing, fingering, conversion, and GP correctness tests must use whole private fixtures or provenance-linked cases extracted from them. Hand-authored geometry, IR, MusicXML, or mock musical events cannot prove behaviour.
* **CI Portability**: Public CI may run pure format/schema tests, but a skipped private-corpus suite is NOT_EVALUATED, never PASS. Required merge evidence must include a non-skipped isolated private-fixture run.
* **Banned**: Synthetic behavioural tests as acceptance, tests encoding the implementation, and refusal-only completion claims.
* **Known-Bad Gate**: Every regression must fail on the exact bad branch or mutation it claims to detect before authorizing legacy-test removal.

### 2. Snapping Tolerance & Synthesis Fallbacks
* **No Unreviewed Constants**: 24.0, 20.0, 15.0, and 24-fret guards remain hypotheses until real-source evidence and negative counterexamples prove a context-dependent rule.
* **No Unlabelled Synthesis**: Missing TAB remains absent or ambiguous. Any optimizer is separately researched, provenance-labelled, and never observed arranger fingering.

### 3. Workflow & Promotions
* Load the conversion-recovery programme, dependency backlog, and director skill before the older M6 backlog.
* Do not promote M6 skeletons until the architecture review accepts their assumptions, files, and oracle.
* Maintain sequentially incrementing page measure indexing. Revert any commit that resets `next_bar_index` to 1 on page change.

## Verification Checklist for Reviews
Before promoting any task in Milestone 6:
1. Run `python3 scripts/score2gp_governance_audit.py` to check for leaks.
2. Confirm no private PDF files or debug logs are staged/committed.
3. Verify ordered bar/event evidence and first divergence; a measure count alone cannot prove correctness.
4. Verify the generator had no access to the reference GP.
5. Verify required private tests ran and were not skipped.
