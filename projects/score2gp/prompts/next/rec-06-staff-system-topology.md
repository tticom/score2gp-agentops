# REC-06 — Staff and System Topology

Status: PROMOTED
Role: Developer
Repository: `score2gp`

## Objective

Reconstruct pages, reading order, systems, staff regions, notation/TAB pairings
and stable identities from document observations.

## Required work

1. Consume observations and scale estimates only through their interfaces:
   - `DocumentObservations` from `score2gp.recognition.schemas` (populated via `observations.py` and `raster.py`).
   - `LocalScaleModel` from `score2gp.recognition.scale`.
2. Construct and populate typed `DocumentTopology` data structures:
   - `PageTopology`: page indices, dimensions, content bounding boxes, and system reading order.
   - `SystemTopology`: bounding box, ordered staff region IDs, pairing IDs, division IDs.
   - `StaffRegion`: stable ID, staff kind (`notation`, `tab`, `unknown`), line count (e.g. 5 for notation, 6 for TAB), staff space, bounding box, and constituent `StaffLine` instances.
   - `StaffPairing`: paired notation/TAB systems with vertical gap and confidence, or standalone notation/TAB systems.
   - `PhysicalDivision`: barlines/system boundaries without asserting musical measure semantics.
3. Represent competing staff groupings and pairing support with confidence scores.
4. Support conventional notation (5-line), six-string TAB (6-line), and paired instructional layouts.
5. Return explicit `Unsupported` or `Ambiguous` hypotheses for degraded or inadequate layouts; never fall through to silent invalid defaults.
6. Expose no measure, duration, pitch, or final-event semantics.

## Acceptance and falsification

- Disconnected systems cannot cross-snap across horizontal or vertical boundaries.
- Titles, headers, diagrams, and horizontal noise primitives do not become supported staves.
- Competing staff hypotheses remain inspectable rather than silently collapsed.
- At least two structurally distinct real scores from the approved private corpus have stable identities and valid topology representations.

## Validation

- `python3 -m pytest tests/recognition/test_topology.py`
- `python3 -m mypy src/score2gp/recognition/topology.py tests/recognition/test_topology.py`
- Full test suite passes without regressions.
