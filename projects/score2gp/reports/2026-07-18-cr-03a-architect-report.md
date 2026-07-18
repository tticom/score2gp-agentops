# CR-03A Architect Report: Local Tuplet-Group Evidence and Meter Resolution

## Active Blocker
CR-03A requires safely associating tuplet `3` marks with exactly one local group of three eighth-note events. We must avoid global fallback assumptions (such as an "11 eighth notes" fallback) and explicitly avoid false positives from TAB fret digits, measure labels, or other arbitrary text containing `3`.

## Verified Repository State
- Previous fallback logic led to overfull measures (e.g. 1280-tick false rest in Lesson 5) due to misidentifying chords or missing local tuplet bounds.
- Unrelated `3` digits exist in TAB, measure numbers, and metadata (e.g., `[3:50]`).
- Clean-Base rule applies: this branch starts from `origin/main` of the product repository, avoiding the `3b138a7f` prototype.

## Research Question
How can we definitively associate a printed tuplet `3` to exactly three sequential eighth notes in the standard staff while ignoring all adversarial `3` digits?

## Product Data Model and Integration Points
Tuplet association must occur **before chord slicing** and timeline coalescence to ensure sequential duration modifications are applied accurately.
- **Integration Point**: The tuplet recognizer should be invoked during or immediately after the raw notation event assembly (`ScoreIR` construction phase), before timeline coalescence groups notes into chords or evaluates measure tick capacity.
- **3:2 Duration Handling**: Each note in an associated three-event eighth-note tuplet group has its base duration modified to represent exactly 2/3 of its standard length (i.e. three 8th notes span the duration of two 8th notes, taking exactly 1 quarter note).
- **MusicXML Time-Modification Emission**: When generating MusicXML, the parser must emit the `<time-modification>` tags (`<actual-notes>3</actual-notes>`, `<normal-notes>2</normal-notes>`) alongside the `<tuplet>` bracket notations to faithfully represent the triplet without padding or false rests.

## Precise Local Geometric Tuplet Association Rule
A valid tuplet `3` association strictly demands:
1. **Normalized Tuplet Lane (Y-bounds)**: The digit `3` must exist strictly within the expected notation lane (just above or just below the standard 5-line staff). It must not impinge upon the TAB staff bounding box or the system header/measure box regions.
2. **X Tolerance**: The bounding box of the digit `3` (and any associated bracket lines) must horizontally overlap or span between the X-bounds of the first and third notehead of the candidate sequence. A strict X-delta threshold must be applied to prevent wide association.
3. **Hierarchy Ownership**: Both the tuplet digit `3` and the three candidate events must share the exact same `page`, `system`, `staff`, and `measure` ownership hierarchy.
4. **Exact Three-Event Sequential Group**: The associated events must be exactly three *sequential* eighth-note events on the standard staff, containing no intervening events of other durations or rests.
5. **Fail-Closed Ambiguity Behavior**: If the geometric association is ambiguous (e.g., tuplet label overlaps the TAB region or is X-shifted such that two different 3-note groups could claim it), the parser must fail closed for that measure. It must emit a specific tuplet-ambiguity warning and refuse to guess, avoiding downstream tick-corruption.

## Rejection Rules for Adversarial Candidates
- **TAB fret digits**: Reject any `3` whose Y-coordinate falls within or spans into the vertical bounds of the TAB staff.
- **Measure labels**: Reject any `3` located in the system header measure-box regions.
- **Arbitrary text `3`**: Reject any `3` (e.g., `[3:50]`) that violates the Tuplet Lane constraint or matches known textual metadata patterns.

## Public Synthetic Extraction Fixture Design
To prove these rules generically, a synthetic extraction test fixture must be designed containing:
1. **Genuine Tuplet `3`**: A standard 3:2 triplet block correctly formatted and placed.
2. **Adversarial TAB digit `3`**: A TAB fret `3`, `13`, or `23`.
3. **Adversarial Measure Header `3`**: A measure box label `3`.
4. **Adversarial Metadata `3:50`**: Text `[3:50]` near the system.
5. **Ambiguous Geometry Refusal**: A tuplet `3` intentionally placed halfway between two valid sequential groups or overlapping the TAB staff boundaries, triggering the fail-closed assertion.

*Test criteria*: The extractor must only associate and scale the durations of the 3-note group under the genuinely unambiguous tuplet mark, leaving the remaining notes unscaled and correctly failing-closed on the ambiguous measure.

## Explicit Acceptance Evidence (Regression Guard)
- **4/4 Triplets**: Must output three eighth-note events spanning a total of one quarter-note duration with correct MusicXML time-modification emission.
- **6/8 and 12/8 Meter**: Ordinary grouped eighth notes in these meters do not require a tuplet mark and must output with their normal unscaled duration. The parser must distinguish 4/4 triplets (tuplet mark required) from 6/8 or 12/8 sequences (no tuplet mark required, meter-based duration).

## Selected Outcome
**Outcome A — Deterministic Heuristic Path is viable**: A precise vector-bounding heuristic approach (Local Geometric Association) is fully justified and explicitly measurable.

## Measurable Success Criterion
The extraction parser passes the public synthetic extraction fixture, correctly identifying the 1 genuine triplet, rejecting the 3 explicit adversarial candidates, intentionally failing on the 1 ambiguous candidate, and exhibiting no regressions in 6/8 and 12/8 test cases.

## Proposed Developer Task
Implement the local geometric association rule, hierarchy matching, and fail-closed logic in the vector event parser before chord slicing. Provide unit tests using the specified synthetic extraction fixture design. Do not begin implementation until Reviewer approval.
