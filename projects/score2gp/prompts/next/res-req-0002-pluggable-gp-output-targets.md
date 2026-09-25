# RES-REQ-0002 — Research to take REQ-0002 to ACCEPTED

- **Kind:** research (backlog item `RES-REQ-0002`; promote to a task before execution)
- **Repository:** `tticom/score2gp-agentops` (records), with read-only use of the private corpus
- **Requirement:** [REQ-0002](../../requirements/REQ-0002-pluggable-gp-output-targets.md), currently `RESEARCHED`

## Goal

Complete the research that REQ-0002 needs before the maintainer can accept it, and record it in the requirement's own sections (§4, §8, §12).

## Deliverables

1. **Open questions.** Answers or decision-ready options for §12 Q3 (the default target when none is given) and Q4 (whether the plugin interface is public or first-party only), with the consequences of each option.
2. **GP8 evidence** (the OUT-00 scope, GP8 first):
   - a blank-score and a blank-track package saved by Guitar Pro 8, and every GP8-authored reference in the corpus, catalogued by hash;
   - version stamps and container facts, with no musical content;
   - the per-version feature limits that can be established from these files and from documentation, each with its source.
3. **GP7 route.** Establish whether Guitar Pro 8 can save or export GP7-compatible files, and whether a GP7-authored reference (`Ex 2 Hands Up.gp`) survives a GP8 open and re-save. Keep in mind the rule already recorded in REQ-0002: a GP8 re-save is not a GP7 round trip.
4. **Capability matrix draft** for the `gp8` target: every canonical feature marked exact, degraded or refused, each with its evidence.
5. **Status proposal.** Recommend `ACCEPTED` or state what is still missing.

## Constraints

- No product code change.
- No private musical content, coordinates or files committed; hashes and counts only.
- Every claim cites a real file, a document or an executed probe.

## Acceptance

- REQ-0002 §4, §8 and §12 are updated with sourced findings.
- An independent reviewer can reproduce every probe from the recorded commands.
