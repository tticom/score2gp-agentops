# RES-REQ-0003 — Research to take REQ-0003 to ACCEPTED

- **Kind:** research (authority backlog item `RES-REQ-0003`; promote to a task before execution)
- **Repository:** `tticom/score2gp-agentops` (records); read-only inspection of `tticom/score2gp` dependencies
- **Requirement:** [REQ-0003](../../requirements/REQ-0003-dependency-licence-compatibility.md), currently `PROPOSED`

## Goal

Establish the facts and options the maintainer needs in order to accept REQ-0003, and record them in the requirement.

## Deliverables

1. **Licence inventory.** Every runtime and build dependency of the product (direct and transitive), with its licence read from installed package metadata or the source repository. Classify each as permissive, weak copyleft or strong/network copyleft.
2. **PDF-library options.** For the acquisition layer currently built on `pymupdf` (AGPL-3.0 or Artifex commercial), compare:
   - an Artifex commercial licence: record that terms and cost must come from Artifex, and do not guess prices;
   - permissively licensed alternatives, for example `pypdfium2` and `pdfminer.six`.
   Assess each for the observations the product needs: vector paths with paint order, colour and opacity; text with positions; raster rendering. Measure, on at least Lesson 3, whether each alternative reproduces the observations the current pipeline uses. The existing topology fingerprint over the corpus is a suitable oracle.
3. **A proposed mechanical audit**, the check the CI licence gate in REQ-0003 acceptance criterion 1 would run.
4. **Status proposal.** Recommend `ACCEPTED`, with the chosen direction left to the maintainer as a decision (authority backlog item DEC-04).

## Constraints

- No product code or dependency change.
- No legal conclusions: record licence facts and the questions for a lawyer.

## Acceptance

- REQ-0003's findings and acceptance sections are complete and sourced.
- The option comparison includes measured fidelity, not only feature lists.
