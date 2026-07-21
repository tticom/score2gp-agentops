# FS-03A: Supported Timing-Source Route Architecture

## 1. Provenance and Recorded Routes

**Product SHA**: `e72cd7c8` (from `score2gp` main)

**Exact Current `convert --musicxml` Route**:
The supported route for PDF conversion invokes `score2gp convert --pdf <path> --musicxml <sidecar_path>`. The command (defined in `src/score2gp/cli.py`):
1. Validates the PDF file.
2. Inspects and extracts tab vectors from the PDF.
3. Requires the MusicXML sidecar path and verifies its existence.
4. Proceeds to `build-ir` if the sidecar and valid vector geometries are provided.

**Standalone `omr` Route**:
The product supports a standalone OMR capability via `score2gp omr <pdf_path> --audiveris <audiveris_path>`. This route:
1. Validates the input PDF and Audiveris path.
2. Invokes Audiveris via a subprocess: `audiveris -batch -export -output <out> <pdf>`.
3. Records stdout/stderr to a log and captures the result/warnings.
It is completely decoupled from the `convert` command.

## 2. Integration Feasibility

Can Audiveris output become a validated MusicXML sidecar in the supported route?
**Yes.** The decoupled nature of the `omr` command allows Audiveris to generate a MusicXML (`.mxl` or `.xml`) artifact independently. This output file can be explicitly fed into the supported `convert --musicxml` route, fulfilling the timing-source requirement without violating the explicit separation of OMR logic from the deterministic build phase.

## 3. Route Classification

- **Supported Route**: Two-step decoupled process:
  1. Generate MusicXML sidecar (e.g., using `score2gp omr`).
  2. Execute `score2gp convert --pdf <path> --musicxml <path>`.
- **Unavailable Route**: Fully automated end-to-end `convert` that invisibly invokes Audiveris.
- **Uncontrolled Route**: Any uncommitted script or modified entry point that attempts to pipeline `omr` directly into `convert` in a single unmonitored execution without recording the intermediate artifact.

## 4. Governance Constraints

- **Provenance**: The source of timing data (the sidecar) must remain explicit on the CLI invocation (`--musicxml`).
- **Validation**: Any generated sidecar must be valid MusicXML prior to integration. `convert` performs semantic validation in its orchestration gate.
- **Failure Behaviour**:
  - If Audiveris fails to produce MusicXML, the `omr` command fails cleanly and writes to the warnings manifest.
  - If `convert` receives an invalid or missing sidecar, it fails in the `orchestration-gate` phase.
- **Lessons 3-7 Corpus Acceptance Matrix**:
  - The integration will be tested against the Lessons 3-7 corpus.
  - Acceptance requires the decoupled process to yield successful alignments and valid `.gp` package generation for the corpus, matching the expected output baseline.

## 5. Recommendation

**Smallest First Product Implementation Task**:
Implement a CI or diagnostic script that orchestrates the two-step supported route for a single fixture from the Lessons 3-7 corpus: first running `score2gp omr`, asserting output existence, and then running `score2gp convert --musicxml` using that artifact. This validates the pipeline practically before further tooling.

## 6. Recogniser Refactoring

Any internal refactoring of note, rest, or symbol recognisers inside `score2gp` is **explicitly deferred**. The priority is establishing the architecture of the timing-source route; recogniser behaviour must not be changed at this stage.
