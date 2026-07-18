# CR-03A Architect Report: Local Tuplet-Group Evidence and Meter Resolution

## Active Blocker
CR-03A requires safely associating tuplet `3` marks with exactly one local group of three eighth-note events. We must avoid global fallback assumptions (such as an "11 eighth notes" fallback) and explicitly avoid false positives from TAB fret digits, measure labels, or other arbitrary text containing `3`.

## Verified Repository State
- Previous fallback logic led to overfull measures (e.g. 1280-tick false rest in Lesson 5) due to misidentifying chords or missing local tuplet bounds.
- Unrelated `3` digits exist in TAB, measure numbers, and metadata (e.g., `[3:50]`).
- Clean-Base rule applies: this branch starts from `origin/main` of the product repository, avoiding the `3b138a7f` prototype.

## Research Question
How can we definitively associate a printed tuplet `3` to exactly three sequential eighth notes in the standard staff while ignoring all adversarial `3` digits?

## References Reviewed
- CR-03 Recovery Review (`projects/score2gp/reviews/2026-07-17-cr-03-recovery-review.md`): Identifies adversarial elements (TAB, headers, metadata).
- Visual Output Correctness Backlog (`projects/score2gp/tasks/2026-07-17-visual-output-correctness-backlog.md`): Specifies the requirements for CR-03A.

## Options Considered
1. **Global Count Thresholds**: Fallback if 11 eighth notes are present to assume triplets. (Rejected: explicitly forbidden by CR-03A).
2. **Local Geometric Association (Selected)**: Match the bounding box and X/Y coordinates of a genuine tuplet `3` to a sequential run of three rhythmically grouped eighth-note events on the standard staff.
3. **Voice/Measure Capacity Balancing**: Wait until measure validation to detect triplet needs. (Rejected: this belongs to CR-04A; tuplet recognition must be explicit).

## Local Geometric Association Rule
1. **Candidate Selection**: Identify a digit `3` whose Y-coordinate is strictly within the vertical bounds established for tuplet markers above/below the standard staff, and whose X-coordinate is horizontally bounded by the first and third noteheads of a sequential 3-note eighth-note group.
2. **Sequential Grouping**: The three eighth-note events must be sequential (no intervening rests or notes of other durations) and belong to the standard staff.
3. **Association**: The tuplet mark is associated *only* with the geometrically enclosing 3-note group.

## Rejection Rules for Adversarial Candidates
- **TAB fret digits**: Reject any `3` whose Y-coordinate falls within the vertical bounding box of the TAB staff.
- **Measure labels**: Reject any `3` located at the system header Y-coordinates, typically flush left with the system start or in a dedicated measure-box region.
- **Arbitrary text `3`**: Reject any `3` (e.g., in `[3:50]`) that fails to geometrically align over exactly three sequential eighth notes in the standard staff, or that matches known metadata text templates (e.g., regex `\[\d+:\d+\]`).

## Public Synthetic Extraction Fixture Design
To prove these rules generically, a synthetic fixture must be designed containing:
1. **Genuine Tuplet `3`**: A standard 3:2 triplet block.
2. **Adversarial TAB digit `3`**: A TAB fret `3`, `13`, or `23`.
3. **Adversarial Measure Header `3`**: A measure box label `3`.
4. **Adversarial Metadata**: Text `[3:50]` near the system.
*Test criteria*: The extractor must only scale the durations of the 3-note group under the genuine tuplet mark, leaving the remaining notes unscaled.

## Explicit Acceptance Evidence (Regression Guard)
- **4/4 Triplets**: Must output three eighth-note events spanning a total of one quarter-note duration (scaled to 2/3 of their base tick value).
- **6/8 and 12/8 Meter**: Ordinary grouped eighth notes in these meters do not require a tuplet mark and must output with their normal unscaled duration. The parser must explicitly distinguish 4/4 triplets (tuplet mark required) from 6/8 or 12/8 sequences (no tuplet mark required, meter-based duration) based on the presence of the geometric tuplet mark.

## Pivot Conditions
If local association cannot be proven generically (e.g., due to extreme layout distortions where a tuplet `3` geometrically overlaps with a TAB `3`):
- **Pivot**: Fall back to failing closed for that measure, emitting a recognition warning and requiring manual review, rather than guessing.
- **Pivot Task**: Create a diagnostic tool to flag geometrically ambiguous tuplet candidates before structural conversion, allowing human verification before proceeding.

## Selected Outcome
**Outcome B**: Raster path is not viable (or applicable here as this relies on vector geometry), but an alternative geometric bounding-box approach is justified.

## Measurable Success Criterion
The extraction parser passes the public synthetic extraction fixture, correctly identifying the 1 genuine triplet and rejecting the 3 adversarial candidates, with no regressions in 6/8 and 12/8 test cases.

## Proposed Developer Task (Outcome B)
Implement the local geometric association rule and rejection logic in the vector event parser. Provide unit tests using the specified synthetic extraction fixture design. Do not begin implementation until Reviewer approval.
