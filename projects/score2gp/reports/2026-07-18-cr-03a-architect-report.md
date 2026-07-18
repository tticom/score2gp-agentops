# CR-03A Architect Report: Local Tuplet-Group Evidence and Meter Resolution

## Active Blocker
CR-03A requires safely associating tuplet `3` marks with exactly one local group of three eighth-note events. We must avoid global fallback assumptions (such as an "11 eighth notes" fallback) and explicitly avoid false positives from TAB fret digits, measure labels, or other arbitrary text containing `3`.

## Verified Repository State
- Previous fallback logic led to overfull measures (e.g. 1280-tick false rest in Lesson 5) due to misidentifying chords or missing local tuplet bounds.
- Unrelated `3` digits exist in TAB, measure numbers, and metadata (e.g., `[3:50]`).
- Clean-Base rule applies: the *future product branch* must start from `origin/main` of the product repository, avoiding the `3b138a7f` prototype.

## Research Question
How can we definitively associate a printed tuplet `3` to exactly three sequential eighth notes in the standard staff while ignoring all adversarial `3` digits?

## Product Data Model and Integration Sequence
Tuplet association must occur before `build_staff_timeline_preview` performs X-delta proximity chord slicing. Because raw candidates do not yet have measure ownership at that point, we must define an intermediate model:
1. **Derive Measure Spans**: Derive staff-local measure spans from barlines or text anchors.
2. **Assign Candidates**: Assign note candidates to one span.
3. **Integration Point**: In `whole_note_recogniser.py`, directly after candidate composition and measure span assignment, but before `build_staff_timeline_preview` slicing.
4. **Intermediate Tuplet Models**: Construct `TupletMarkerEvidence` and `TupletAssociation` data classes. These must include:
   - `marker_id`
   - three ordered candidate IDs
   - `ratio` (e.g., 3:2)
   - `span_id`
   - `geometry_facts`
   - `status` (`associated` or `ambiguous`)
5. **Association Output**: The association must return exactly one unique group per marker or issue a fail-closed refusal.
6. **Downstream Integration**: Pass the resolved `TupletAssociation` models down to the deterministic MusicXML or existing IR tuplet path to accurately emit the `<time-modification>` tags alongside the bracket notations, scaling durations to exactly 2/3.

## Precise Local Geometric Tuplet Association Rule
A valid tuplet `3` association strictly demands:
1. **Normalized Tuplet Lane (Y-bounds)**: Restrict the valid lane to the above-staff case (defined as the region from the top staff line extending up to 2 staff-space heights above it) to guarantee a bounding lane proven clear of TAB regions.
2. **X Tolerance (Strict)**: The bounding box X-center of the digit `3` must fall strictly between the X-coordinate of the first notehead and the X-coordinate of the third notehead of the candidate sequence.
3. **Hierarchy Ownership**: Both the tuplet digit `3` and the three candidate events must share the exact same `page`, `system`, `staff`, and explicit `span_id`.
4. **Exact Three-Event Sequential Group**: The associated events must be exactly three *sequential* eighth-note events on the standard staff, containing no intervening events of other durations or rests.
5. **Fail-Closed Ambiguity Behavior**: If the geometric association is ambiguous (e.g., competing groups fall in the tolerance window, or the marker drifts out of the normalized lane), construct the `TupletAssociation` with `status="ambiguous"`. The parser must fail closed for that measure and refuse to guess.

## Rejection Rules for Adversarial Candidates
Geometric boundary and ownership rejection must occur first:
- **TAB fret digits & Measure labels**: Rejected automatically by the strictly defined above-staff Tuplet Lane Y-bounds.
- **Arbitrary text `3`**: Optional secondary rejector for metadata patterns (e.g., regex `\[\d+:\d+\]`), but primary rejection occurs because it fails the explicit X-tolerance bounding and ownership criteria.

## Public Synthetic Extraction Fixture Design
To prove these rules generically, a synthetic extraction test fixture must be designed containing:
1. **Genuine Tuplet `3`**: A standard 3:2 triplet block correctly formatted above the staff.
2. **Adversarial TAB digit `3`**: A TAB fret `3`, `13`, or `23`.
3. **Adversarial Measure Header `3`**: A measure box label `3`.
4. **Adversarial Metadata `3:50`**: Text `[3:50]` near the system.
5. **Ambiguous Geometry Refusal**: A tuplet `3` intentionally placed halfway between two valid sequential groups, triggering the `ambiguous` status and fail-closed refusal.

*Test criteria*: The extractor must only associate and scale the durations of the 3-note group under the genuinely unambiguous tuplet mark, leaving the remaining notes unscaled and correctly failing-closed on the ambiguous measure.

## Explicit Acceptance Evidence (Regression Guard)
- **4/4 Triplets**: Must output three eighth-note events spanning a total of one quarter-note duration with correct MusicXML time-modification emission.
- **6/8 and 12/8 Meter**: Ordinary grouped eighth notes in these meters do not require a tuplet mark and must output with their normal unscaled duration. The parser must distinguish 4/4 triplets (tuplet mark required) from 6/8 or 12/8 sequences (no tuplet mark required, meter-based duration).

## Selected Outcome
**Outcome A — Deterministic Heuristic Path is viable**: A precise vector-bounding heuristic approach (Local Geometric Association) via the defined intermediate span models is fully justified and explicitly measurable.

## Measurable Success Criterion
The extraction parser passes the public synthetic extraction fixture, correctly identifying the 1 genuine triplet, rejecting the 3 explicit adversarial candidates, intentionally failing on the 1 ambiguous candidate, and exhibiting no regressions in 6/8 and 12/8 test cases.

## Proposed Developer Task
Implement the intermediate `TupletMarkerEvidence` and `TupletAssociation` models, measure span assignment, and local geometric association logic in `whole_note_recogniser.py` before chord slicing. Provide unit tests using the specified synthetic extraction fixture design. Do not begin implementation until Reviewer approval.
