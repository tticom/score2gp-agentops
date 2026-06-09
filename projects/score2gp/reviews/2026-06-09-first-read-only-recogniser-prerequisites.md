# First Read-Only Recogniser Prerequisites and Acceptance Criteria

**Status:** PROPOSED
**Date:** 2026-06-09

## Purpose
This is a governance-only design note that defines the prerequisites and strict acceptance criteria for a later first recogniser implementation. It does **not** authorise product implementation. Instead, it establishes the evidence requirements and safety boundary for when product implementation begins.

## Verified Baseline
As verified live:
- Product PR #234 is merged, exposing `left_margin_candidates` and `x_aligned_cluster_candidates` as optional read-only supplementary fields on `NotationStaffDiagnostics`.
- Governance PR #101 is merged, producing the candidate diagnostics consumption boundary note (`2026-06-09-candidate-diagnostics-consumption-boundary.md`).
- That boundary explicitly restricts candidates to read-only geometry/evidence inspection and prohibits ScoreIR integration at the diagnostic boundary.

## Candidate Diagnostics Available
The following candidate diagnostic fields are available to the recogniser:
- `left_margin_candidates`
- `x_aligned_cluster_candidates`

These fields must be used strictly for read-only geometry and evidence inspection. The implementation must preserve the following semantics:
- **`None`**: Extraction was not run or prerequisite evidence was unavailable.
- **`[]`**: Extraction ran against a valid evidence array but found no candidates.
- **Populated list**: Valid candidates derived entirely from real visual/geometry evidence.

## Candidate Diagnostics Not Yet Available
The following prerequisite evidence may affect robust recognition but is currently missing:
- **Refined horizontal timelines / bar boxes:** May prevent accurate spatial alignment of events along the staff timeline.
- **System-level connectivity evidence:** May inhibit understanding of cross-staff grouping guarantees.
- **Precise stem and notehead candidate models:** Restricts the ability to accurately cluster or parse rhythmic structures.
- **Text-vs-notation distinction:** Prevents clear differentiation between annotations/lyrics and actual notation markings.

## First Recogniser Target Selection
**Target:** Read-Only Clef Candidate Classifier (Left-Margin)

Clef candidate classification is selected as the first design target because left-margin candidates may contain relevant evidence; implementation remains blocked until public tracked fixtures prove that the required evidence is present and distinguishable without synthetic geometry.
**Important:** This design note authorises only a candidate-level read-only recogniser. It does **not** authorise a ScoreIR Clef event implementation. The recogniser must classify the physical evidence only and must not emit ScoreIR. It must not group disconnected primitives unless a future design explicitly authorises a grouping rule.

## Allowed Inputs for the Future Recogniser
The future recogniser is strictly limited to reading fields accessed through `NotationStaffDiagnostics.left_margin_candidates` (and potentially `x_aligned_cluster_candidates`). It may read:
- **Staff Identity:** `page_index`, `system_index`, `staff_index` (from the parent diagnostic context)
- **Geometry:** `x0`, `y0`, `x1`, `y1` (from the candidate objects themselves)
- **Primitive Metadata:** primitive kind, font name, font size, input/evidence order (from the candidate objects themselves)

Original evidence must be preserved exactly and not mutated.

## Prohibited Behaviour for the Future Recogniser
The future product implementation must adhere to these prohibitions:
- No inference of pitch, duration, rhythm, voice, chord, note, rest, key-signature, or time-signature.
- No ScoreIR event emission.
- No synthetic bounds, placeholder candidates, or invented geometry.
- No reordering of evidence unless explicitly justified and the original order is preserved.
- No use of private PDFs or local screenshots as acceptance evidence.
- No broad "recognise music notation" tasks—the scope must remain tightly bounded to the selected target.

## Fixture and Smoke Requirements for Later Product Implementation
Later product work must prove its safety and efficacy before merge by providing:
- Use of public/tracked fixtures only.
- Empirical smoke against at least one realistic public fixture containing the target evidence (e.g., standard staff fixtures with left-margin data).
- Explicit tests confirming:
  - Safe handling of `None`.
  - Safe handling of `[]`.
  - Proper handling of a populated candidate list.
  - Complete preservation of geometry and metadata.
  - Zero ScoreIR emission.
  - No mutation of candidate bounds.

If suitable public fixtures to support this verification do not exist, the next immediate task must be prerequisite fixture/evidence creation, rather than recogniser implementation.

## Conditional Next Task
- **If suitable public/tracked fixture evidence exists:** Task 48 may be a product implementation task (`Task 48 — Implement read-only Clef Candidate Classifier over left-margin candidates`).
- **If not:** The next task must be prerequisite fixture/evidence definition or creation before any recogniser implementation begins.

## Stop Conditions for Future Product Implementation
Product implementation must immediately halt and report if:
- Candidate evidence is unavailable.
- Implementation requires inferred geometry or synthetic candidates.
- Private PDFs or local screenshots are needed to validate the target.
- The target cannot be validated using existing public/tracked fixtures.
- The recognition requires emitting ScoreIR events.
- It requires grouping disconnected primitives without a governance-approved rule.
- `None` and `[]` semantics cannot be preserved.
