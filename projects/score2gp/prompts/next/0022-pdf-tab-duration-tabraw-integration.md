# Developer Task: PDFTAB-DUR-05 (TabRaw Duration Evidence Pipeline Integration)

Execute Slice 2 of the PDF-Tab Duration Candidate Extraction Architecture defined in `docs/design/pdf-tab-duration-candidate-extraction.md`.

## Preflight

1. Work exclusively as `tticom-automation` in `/home/tticom-automation/work/score2gp-workspace/score2gp`.
2. Verify identity, HOME, GitHub CLI user, Git global user (`tticom-automation`), and canonical workspace path.
3. Read:
   - `docs/design/pdf-tab-duration-candidate-extraction.md`
   - `src/score2gp/pdf_tab_duration_types.py`
   - `src/score2gp/pdf_tab_duration_associator.py`
   - `src/score2gp/tabraw.py`
4. Checkout branch `agy/pdftab-duration-tabraw-integration` from `origin/main` (`545d0bea36513969d0e53fc56e93cbc6c3e35518`).

## Requirements

1. **TabCandidate Raw Metadata Extension (`src/score2gp/tabraw.py`)**:
   - Extend `TabCandidate` and `make_tab_candidate` helper in `src/score2gp/tabraw.py` to support optional `duration_evidence` (instance of `TabDurationEvidence` or dictionary matching its schema).
   - When provided, store `duration_evidence` in `candidate.raw["duration_evidence"]` as a validated dict or model payload matching `TabDurationEvidence`.
   - Add property `duration_evidence` on `TabCandidate` that converts `raw.get("duration_evidence")` into `TabDurationEvidence | None`, returning `None` if absent or gracefully handling schema mismatch.

2. **Schema & Normalization Validation (`src/score2gp/tabraw.py`)**:
   - Ensure `TabRaw.from_json_file`, `TabRaw.to_json_file`, `normalize_tabraw_payload`, and Pydantic model serialization preserve `duration_evidence` in candidate raw metadata across round-trip JSON serialization.
   - Maintain strict `extra="forbid"` on `TabCandidate` and `TabRaw` models while permitting `duration_evidence` inside `raw`.

3. **Mandatory Test Cases (`tests/test_tabraw_duration_metadata.py`)**:
   Create `tests/test_tabraw_duration_metadata.py` with 100% test coverage including:
   - **Direct Construction & Helper Access**: Constructing `TabCandidate` via `make_tab_candidate` with `TabDurationEvidence` and accessing `.duration_evidence`.
   - **JSON Serialization & Deserialization**: Saving a `TabRaw` container holding candidates with duration evidence to JSON and verifying lossless round-trip recovery.
   - **Legacy & Dict Payload Normalization**: Passing raw dict payloads to `normalize_tabraw_payload` and verifying candidate `raw["duration_evidence"]` is preserved.
   - **Malformed Evidence Boundary**: Testing invalid or corrupt `duration_evidence` dict structures (e.g. invalid duration names or negative tick counts), asserting fail-closed behavior or property returning `None`/raising validation errors cleanly.

4. **Validation**:
   Run `.venv/bin/python scripts/agent_verify.py` and ensure all unit tests pass cleanly.

5. **Publication**:
   Open PR on `tticom/score2gp` and publish exact-head handback comment with `AWAITING_GOVERNANCE_REVIEW`.
