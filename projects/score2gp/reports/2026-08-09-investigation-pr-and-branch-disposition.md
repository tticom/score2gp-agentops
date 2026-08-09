# Investigation PR and Branch Disposition

Date: 2026-08-09
Status: REVIEWED_FOR_ARCHIVAL
Product main: 4a4f5c339e09987b9f41641397f1db7e8ab1be5d
AgentOps main: c1c7305c81ff800eface43867406728715af8e20

## Purpose

This record preserves the useful evidence from the parallel conversion-failure
investigations without merging contradictory reports or unsafe product code.
Each retired head is retained by an annotated archive tag. The tags preserve
the complete commit tree; this report supplies the claim and disposition index.

The consolidated recovery programme and Task 88 architecture review remain the
decision authority. Archived code is evidence and a source of counterexamples,
not implementation authority.

## Independent source-modality check

A fresh PyMuPDF inspection of the approved private Lesson 5 and Lesson 6 PDFs
contradicted the repeated claim that these specific files contain zero
extractable text:

| Fixture | Pages | Words per page | Digit-bearing words per page |
|---|---:|---|---|
| Lesson 5 | 3 | 304, 298, 106 | 286, 271, 106 |
| Lesson 6 | 6 | 224, 251, 223, 221, 251, 119 | 208, 227, 197, 195, 219, 101 |

Both documents also contain substantial drawing geometry. The correct
classification is therefore mixed evidence at least at document level; Task
88 must determine page, system, and staff modality rather than generalising
from producer or filename.

## Product PR review

### score2gp PR 418

- Head: 6f8e438a600a3b33b1b017de462ba906e4861a9d
- Archive tag: archive/investigation/2026-08-09/pr-418
- Disposition: close as superseded; do not merge.
- Blocking evidence:
  - Four production modules change with no changed tests.
  - The claimed E2E repair is supported only by a barline-list probe, not by an
    ordered final GP semantic oracle.
  - A prior approval is dismissed and targets the earlier head 006fe118.
  - The generator flattens every staff preview into one measure stream without
    proving staff ownership or duplicate suppression.
  - The 20pt inherited-width and staff-relative height rules are unvalidated
    global thresholds.
- Preserve as hypotheses:
  - staff-relative barline-height classification;
  - notation-to-TAB structural barline evidence;
  - multi-page preview traversal;
  - notehead-overlap rejection for stem/barline discrimination.

### score2gp PR 419

- Head: 28c8a5965cb7a19a88ad76a38c86406dedb4655c
- Archive tag: archive/investigation/2026-08-09/pr-419
- Disposition: close as contradicted and superseded; do not merge.
- Blocking evidence:
  - Three production modules change with no changed tests.
  - The branch adds open-string pitch-to-fret synthesis, capacity-based measure
    fragmentation, duration truncation, and deduplication that can replace
    observed musical truth.
  - Its own report records 133 measures and 354 notes for Lesson 5 and 166
    measures and 602 notes for Lesson 6, rather than reference structure.
  - Its zero-extractable-text premise is directly contradicted by the fresh
    source probe above.
- Preserve as evidence:
  - first-preview/multi-page sidecar truncation;
  - OMR timing and missing-barline failure modes;
  - the branch as a known-bad oracle for synthesized fingering and automatic
    capacity partitioning.

### score2gp PR 420

- Head: 70a2d05077374640cf496503506226ac71b5ce38
- Archive tag: archive/investigation/2026-08-09/pr-420
- Disposition: close as incomplete and unsafe; do not merge.
- Blocking evidence:
  - Five production modules change with no changed tests or PR evidence body.
  - Page-continuous bar indexing addresses a plausible defect, but no
    real-source ordered-measure oracle proves it.
  - A maximum-fret check cannot distinguish a true multidigit fret from nearby
    event or fingering digits when the accidental concatenation is at most 24.
  - The branch enables duration scaling, so overfull recognition can be forced
    into a measure by changing every event duration.
- Preserve as hypotheses and counterexamples:
  - page-continuous document measure identity;
  - context-aware digit tokenisation;
  - duration scaling as a mandatory known-bad mutation.

## AgentOps report PR review

### AgentOps PR 511

- Head: b99fc3b218eff4311236283ca4d6079edfad5a64
- Archive tag: archive/investigation/2026-08-09/pr-511
- Disposition: close as superseded and materially contradicted.
- Reason: it duplicates the PR 419 report and repeats the false zero-text claim.
  Its useful OMR and sidecar observations remain available through the tag.

### AgentOps PR 512

- Head: f9d81b31c4419c039cda4db7efaff4aaf187d8eb
- Archive tag: archive/investigation/2026-08-09/pr-512
- Disposition: close as superseded and unproven.
- Reason: useful compact-staff and barline geometry observations are mixed with
  unsupported conversion-success claims, local file links, and no final
  semantic artifact. Retain the geometry observations as Task 88 hypotheses.

### AgentOps PR 513

- Head: 648d750489faf849e30d78d391d3d5d275db7649
- Archive tag: archive/investigation/2026-08-09/pr-513
- Disposition: close as superseded but useful.
- Reason: the page-index reset and digit-overmerge mechanisms are plausible and
  should be reproduced, but the proposed <=24 digit guard is not a sufficient
  token classifier and the associated product branch changes timing as well.

## Additional branch disposition

| Repository | Branch head | Archive tag | Disposition and retained value |
|---|---|---|---|
| score2gp | 7ad7cb54a5106738c0ea5faf8c51a9b7ee759621 | archive/investigation/2026-08-09/diagnose-conversion-failures | Delete branch after archival. Retain as the 300pt-snap, warning-suppression, and overbroad-tuplet known-bad implementation. |
| AgentOps | 8ffd0e48b91cba9901d89f6f9eeaf89421d019f1 | archive/investigation/2026-08-09/diagnose-conversion-failures | Delete branch after archival. Retain the report's source-text contradiction and combined-fix claim for adjudication; 301 matched occurrences is not a final semantic oracle. |
| AgentOps | 4bf8adc50e5f1b2c76d6da9eaf4d8a0e4bd89aa1 | archive/investigation/2026-08-09/diagnose-master-report | Delete branch after archival. Retain the longer root-cause synthesis, but mark its zero-text generalisation contradicted for Lesson 5 and 6. |
| AgentOps | bd6c38132a7714cac5df2824df33925b527d85a3 | archive/investigation/2026-08-09/diagnose-report | Delete branch after archival. Retain the alternate root-cause report for claim provenance; it is superseded by the longer report and Task 88. |
| AgentOps | 5e7a3239d7e1925a31b97d15b89cb2261e021763 | archive/investigation/2026-08-09/codex-root-cause | Delete branch after archival. Retain its independent destructive-workaround audit and digit-token counterexample. |

The PR 511, 512, and 513 branch heads use their matching archive tags. The
only non-main working branch to remain after cleanup is
agy/master-conversion-failure-diagnosis while AgentOps PR 514 is under review.

## Claims carried into Task 88

Task 88 must reproduce rather than inherit these claims:

1. staff-relative barline geometry and paired-staff barline fusion;
2. page-continuous system and measure identity;
3. contextual TAB-event, fret, fingering, page-number, tempo, and tuplet-digit
   tokenisation;
4. multi-page preview ownership without duplicate staff streams;
5. timing-complete sidecar generation for Lesson 6 4/4 triplets;
6. mixed text, vector, and raster modality classification at the smallest
   useful topology unit.

Known-bad archive heads must be used to prove that the real-source oracle
detects 300pt snapping, warning suppression, capacity fragmentation, duration
scaling, open-string synthesis, and proximity-only digit concatenation.

## Instruction improvement

Every future investigation task must end with an exact-head claim ledger and a
branch disposition. Before a superseded branch is deleted, unique evidence
must be either merged as reviewed documentation or retained by a verified
archive tag. Diagnostic code and product fixes must not share a PR unless the
active task explicitly authorises both. A combined-fix claim must identify the
exact integration commit; an uncommitted workspace is not durable evidence.
