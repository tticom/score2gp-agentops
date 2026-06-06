# ASCII Alignment Sidecar Architecture v0.1

This report outlines the research, design, and next steps for establishing a safe, explicit ASCII alignment sidecar contract for born-digital ASCII-tab inputs in `score2gp`.

## Verdict
`ASCII alignment sidecar contract designed; cryptographic hash verification proposed to solve stale-sidecar risks; smallest next task defined`

---

## Current ASCII pipeline state
The current ASCII pipeline in `score2gp` is diagnostic-only. It categorizes born-digital ASCII PDFs into the `born_digital_ascii_tab` layout class but refuses to generate `ScoreIR` or a GP package unless an explicit alignment sidecar is passed. Without a sidecar, the pipeline halts during `build-ir` with the refusal code `pdf_input_class_ascii_tab_requires_alignment` (exit code 4).

## Current refusal codes
- `pdf_input_class_ascii_tab_requires_alignment`: Emitted when an ASCII tab is processed without an alignment sidecar.
- `ascii_musicxml_timing_risk`: Emitted when the MusicXML timing preflight detects timing anomalies.
- `ascii_scoreir_gate_invalid_alignment_schema`: Emitted when the sidecar does not match the expected alignment schema.
- `ascii_alignment_status_unavailable`: Emitted when candidates lack usable timing.
- `ascii_alignment_status_ambiguous`: Emitted when column alignment mapping is ambiguous.
- `ascii_alignment_status_incompatible`: Emitted when layout segments do not match measures.
- `ascii_polyphony_not_supported`: Emitted when multi-voice standard notation is matched to ASCII.
- `ascii_unsupported_chord_symbol`: Emitted when chord symbols are present in the ASCII tab.
- `ascii_unsupported_technique_required`: Emitted when techniques are present.
- `ascii_alignment_not_one_to_one`: Emitted when candidate-to-note mapping is not one-to-one.

## Existing alignment evidence
- **Data Models**: `src/score2gp/ascii_alignment.py` defines `AsciiMusicXmlAlignment` and `AsciiMusicXmlCandidateMapping` using Pydantic. It tracks schema version, sources, tracks, and candidates mapped to MusicXML note IDs and ticks.
- **Gating Logic**: `src/score2gp/build_ir.py` runs the `ascii-scoreir-gate.v0.1` gate. It reads the sidecar, verifies its overall status is `compatible`, validates structural counts, and annotates the `TabRaw` candidates before `build-ir` builds the intermediate representation.
- **Tests**: `tests/test_ascii_scoreir_gate.py` runs validation tests verifying missing sidecars, mismatched schemas, and mapping limits.

---

## Proposed sidecar contract
We propose updating the `ascii-musicxml-alignment.v0.1` schema to introduce strict cryptographic file validation to prevent stale alignment mappings.

The updated sidecar JSON contract will include:
1. **Cryptographic Source Verification**:
   - `source_pdf_hash`: SHA-256 hash of the input digital PDF file.
   - `source_musicxml_hash`: SHA-256 hash of the input MusicXML sidecar.
2. **Structural Metadata**:
   - `schema_version`: Must strictly match `"ascii-musicxml-alignment.v0.1"`.
   - `overall_status`: Evaluated status (e.g. `"compatible"`).
3. **Explicit Candidate-to-Note Mapping**:
   - For each playable candidate:
     - `candidate_id`: References the unique ID from `TabRaw`.
     - `musicxml_measure_index`: Target measure index.
     - `nearest_musicxml_note_ids`: Target note ID strings in the MusicXML.
     - `nearest_musicxml_onset_ticks`: Musical onset tick integer.
     - `onset_distance`: Normalized distance float between the visual column and musical onset.
     - `confidence`: Confidence score.

## Validation rules
- **Cryptographic Match**: The computed SHA-256 of the run's PDF and MusicXML files must match the hashes declared in the sidecar.
- **1-to-1 Mapping**: Every playable candidate must map to exactly one pitched, single-voice note.
- **No Overlaps**: Two candidates cannot map to the same voice onset in the same measure.
- **Onset Boundary**: Mapped tick offsets must lie within the bounds of the time-signature divisions for that measure.

## Failure/refusal behaviour
- If hashes do not match, the compiler must abort with the specific refusal code `ascii_alignment_stale_sidecar_hash` (exit code 4).
- If any validation rule is violated, the gate aborts with `ascii_alignment_status_incompatible` or `ascii_alignment_status_ambiguous`.
- Pre-existing user output files are protected, and no GP output is written on failure.

## Privacy and artifact hygiene
- The sidecar file must contain only structural candidate IDs, hashes, column floats, and onset tick integers.
- No copyrighted musical text, fret values, score titles, or artist metadata will be included.
- Sidecars will reside in gitignored `work/` folders or under test fixtures.

## Public test plan
Using public synthetic fixtures (`tests/fixtures/pdf/generated_ascii_tab_scoreir_gate.pdf`):
1. **Mismatched PDF Hash**: Edit the sidecar's `source_pdf_hash` and confirm rejection with `ascii_alignment_stale_sidecar_hash`.
2. **Mismatched MusicXML Hash**: Edit `source_musicxml_hash` and confirm rejection.
3. **Missing Hash Field**: Omit the hash fields and check validation refusal.
4. **Valid Hash Success**: Ensure that when hashes match, the gate passes and outputs a valid GP file.

---

## Recommended smallest next task
Introduce cryptographic input file hash validation into the `ascii-scoreir-gate` in `build_ir`.

- **Branch name**: `feature/ascii-alignment-sidecar-validation-v0.1`
- **Affected files/modules**:
  - `src/score2gp/ascii_alignment.py` (add hash fields to `AsciiMusicXmlAlignment` schema)
  - `src/score2gp/build_ir.py` (verify SHA-256 hashes of input files inside `_ascii_scoreir_gate`)
  - `tests/test_ascii_scoreir_gate.py` (add unit tests covering mismatched and missing hashes)
- **Goal**: Harden the alignment gate against stale sidecars by enforcing matching SHA-256 checks on input files.
- **Non-goals**:
  - Do not implement automatic ASCII timing inference.
  - Do not modify scanned PDF gating behaviors.
- **Implementation Approach**:
  1. Add optional `source_pdf_hash` and `source_musicxml_hash` fields (as string) to `AsciiMusicXmlAlignment`.
  2. Implement a helper function to compute the SHA-256 checksum of a file.
  3. Inside `_ascii_scoreir_gate(...)`, calculate hashes of the active `--pdf` and `--musicxml` files.
  4. Compare with the sidecar fields. If they mismatch, raise `BuildIrInputRiskError` with the category `ascii_alignment_stale_sidecar_hash`.
- **Tests required**:
  - Test that mismatched PDF hash raises `ascii_alignment_stale_sidecar_hash`.
  - Test that mismatched MusicXML hash raises `ascii_alignment_stale_sidecar_hash`.
  - Test that valid matching hashes compile successfully.
- **Validation commands**:
  ```bash
  PYTHONPATH=. .venv/bin/pytest tests/test_ascii_scoreir_gate.py
  PYTHONPATH=. .venv/bin/python3 scripts/private_e2e_smoke.py
  PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py
  git ls-files fixtures/private work
  git diff --check
  ```
- **Acceptance criteria**:
  - All public tests pass.
  - Mismatched files successfully propagate refusal code `ascii_alignment_stale_sidecar_hash`.
- **Stop conditions**:
  - Any public test fails.
  - Tracked private files are detected.

---

## Files likely affected
- `src/score2gp/ascii_alignment.py`
- `src/score2gp/build_ir.py`
- `tests/test_ascii_scoreir_gate.py`

## Commands run
```bash
wsl git -C /home/tticom/work/score2gp-workspace/score2gp switch main
wsl git -C /home/tticom/work/score2gp-workspace/score2gp pull --ff-only origin main
wsl git -C /home/tticom/work/score2gp-workspace/score2gp status --short --branch
wsl git -C /home/tticom/work/score2gp-workspace/score2gp log --oneline --decorate --max-count=50
PYTHONPATH=. .venv/bin/pytest
PYTHONPATH=. .venv/bin/python3 scripts/private_e2e_smoke.py
PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py
wsl git -C /home/tticom/work/score2gp-workspace/score2gp ls-files fixtures/private work
wsl git -C /home/tticom/work/score2gp-workspace/score2gp diff --check
```

## Test results
- Public tests: **478 / 478 passed**
- Private E2E smoke tests: **Passed**
- GP quality audit: **Passed** (private_input_1: 153/153 matched, Lessons 3–7 stable, Melodic Soloing stable at 82/82)

## Private-safety result
`git ls-files fixtures/private work` outputs exactly:
```text
fixtures/private/.gitkeep
```
The private-safety invariant is fully intact.

## Known limitations
- The proposed verification requires pre-computed SHA-256 hashes inside the sidecar file. Any manual changes to the source PDF/MusicXML will invalidate the sidecar and require a new calibration mapping to be generated.
- The alignment logic remains limited to single-track, single-voice, homophonic ASCII-tab bars within the current v0.1 gate scope.

## Stop conditions
- Product `main` is dirty or not up to date.
- Public tests fail.
- Private smoke or quality audit fails.
- Private-safety invariant fails.
