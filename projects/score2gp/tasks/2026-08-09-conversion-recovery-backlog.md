# Conversion Recovery Dependency Backlog

Status: PROPOSED; not executable authority
Programme: projects/score2gp/programmes/2026-08-09-conversion-recovery.md

## Ordered graph

| ID | Task | Role | Depends on | Required output |
|---|---|---|---|---|
| CRP-00 | Exact-revision evidence and PR disposition | Researcher and Reviewer | none | Reproduce conflicts; classify PRs 418–420 and 511–513; freeze known-good and known-bad SHAs. |
| CRP-01 | Full conversion architecture review | Architect | CRP-00 | Current and target seam map, preserve/replace/delete matrix, ADR candidates, migration graph. |
| CRP-02 | Private real-source oracle and CI architecture | Architect and Security/CI Researcher | CRP-00 | Private-repo runner, credential boundary, non-skip gate, provenance schema, reference isolation. |
| CRP-03 | Real-source harness implementation | Developer | reviewed CRP-02 | Generic product comparator plus private fixture runner; proves known-bad branches fail. |
| CRP-04 | Synthetic-test inventory and migration | Test Architect | CRP-03 | Per-test disposition and ordered replacement plan; replacement precedes deletion. |
| CRP-05 | Timing-complete sidecar bake-off | Researcher and Architect | CRP-03 | Compare current and corrected Audiveris, alternate routes, direct and hybrid timing; select A, B, or C. |
| CRP-06 | Source-modality and visual TAB research | Researcher and Architect | CRP-03 | Resolve text/vector/raster claims; choose adapters and real-source accuracy thresholds. |
| CRP-07 | Document-topology module | Developer | CRP-01, CRP-03 | Page, system, paired-staff and bar identity with stable global measure IDs. |
| CRP-08 | Recognition-adapter seam | Developer | CRP-01, CRP-06 | Typed text, vector, and raster evidence adapters; no semantics in acquisition. |
| CRP-09 | Paired-staff evidence fusion | Developer | CRP-07, CRP-08 | Associate notation, TAB, and bar evidence by topology with explicit ambiguity. |
| CRP-10 | Musical-timeline replacement | Developer | CRP-05, CRP-07, CRP-09 | Metre, tuplets, voices, rests and capacity invariants; remove scaling and fragmentation. |
| CRP-11 | TAB token and string ownership | Developer | CRP-06, CRP-08, CRP-09 | Context-aware fret recognition and fingering-marker separation. |
| CRP-12 | Fretboard fallback decision | Researcher and Architect | CRP-11 | Decide whether a labelled optimizer is useful when TAB is absent; never substitute it for observed fingering. |
| CRP-13 | ScoreIR and GPIF compiler refactor | Developer | CRP-10, CRP-11 | Preserve tempo, tracks, structure, supported techniques, and provenance. |
| CRP-14 | Legacy path and workaround removal | Developer | accepted replacements | Delete superseded scaling, auto-partition, open-string, proximity, and tolerance hacks with real-source proof. |
| CRP-15 | Corpus acceptance and release decision | Director and independent Reviewer | CRP-03, CRP-07–14 | Fresh no-reference outputs, first mismatch, supported-input statement, and release or pivot verdict. |

## Research task scopes

### CRP-00 — Evidence adjudication

- Re-run every material claim at its exact branch head and on current main.
- Resolve whether each private PDF exposes text, vector paths, raster images,
  or mixed evidence. Do not generalize from filenames or generator brands.
- Verify ground-truth counts and Lesson 6 metre and triplets from the source
  and validation reference without letting the reference affect generation.
- Produce a hunk-level PR disposition. Do not merge partial fixes merely
  because one report labels them true.

### CRP-01 — Architecture review

- Trace CLI through acquisition, topology, recognition, build_ir, ScoreIR and
  GPIF writing.
- Identify hidden shared state, global indexes, implicit fallbacks, duplicated
  timing ownership, shallow pass-through modules, and unsafe seams.
- Design the target twice and compare locality, depth, migration risk,
  observability, and rollback.
- Produce a preserve, replace, wrap, or delete matrix for every module and test
  family. The report does not authorize implementation.

### CRP-02, CRP-03, CRP-04 — Test-system replacement

- Define a private-fixtures-owned manifest with approved inputs,
  validation-only references, hashes, expected topology and event contracts,
  and privacy class.
- Keep the generator process incapable of opening the reference path.
- Make an independent oracle consume output after generation.
- Require known-bad proof: fail 300pt snapping, duration scaling, open-string
  synthesis, auto-fragmentation, page-index reset, and digit concatenation.
- Inventory every synthetic behavioural test and map it to a real-source
  replacement. Extracted cases retain hash, page, system, and bar provenance.

### CRP-05 — Sidecar technology decision

- Reuse and update the 2026-08-03 sidecar-alternatives research.
- Include current Audiveris batch export, editable OMR correction, alternate
  local OMR, credible commercial tools, direct Score2GP timing evidence, and a
  hybrid visual/topology-owned sidecar.
- Score note and rest recall, bar structure, metre, tuplets, voices, balance,
  determinism, correction effort, licensing, privacy, and headless operation.
- Lesson 6 is a mandatory 4/4-triplet discriminator.

### CRP-06 — Recognition technology decision

- Separately evaluate embedded text, vector-glyph classification, and raster
  recognition on real-source pages.
- Require held-out scores and confusion matrices for fret tokens 0–24,
  fingering digits, string labels, tempo text, and nearby numeric glyphs.
- Opaque training is not authorized. A learned recognizer requires a separate
  dataset, labeling, license, evaluation, and model-lifecycle decision.

## Implementation slicing rules

- One module seam per product PR.
- Add compatibility adapters before moving callers. Remove legacy code only
  after real-source equivalence or an approved improvement is proven.
- Every PR records first divergence before and after on two approved scores.
- Aggregate improvement cannot hide a newly corrupted bar or semantic field.
- Downstream skeletons must be completed from accepted upstream outputs before
  promotion.
