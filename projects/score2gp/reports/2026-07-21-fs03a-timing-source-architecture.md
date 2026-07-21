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
**Unproven.** The current `omr` command merely launches Audiveris as a subprocess and records warnings. It does not establish an explicit output contract, nor has it been proven that it consistently produces a discoverable, valid `.xml` or `.mxl` artifact. While the decoupled architecture allows an artifact to be fed into `convert --musicxml`, the reliable generation and discovery of that artifact remains unverified.

## 3. Route Classification

- **Supported Route**: Providing a valid MusicXML sidecar to `score2gp convert --pdf <path> --musicxml <sidecar_path>`.
- **Unavailable Route**: Fully automated end-to-end `convert` that invisibly invokes Audiveris, or relying on `omr` output without an explicit, proven artifact contract.
- **Uncontrolled Route**: Any uncommitted script or modified entry point that attempts to pipeline `omr` directly into `convert` in a single unmonitored execution.

## 4. Governance Constraints

- **Provenance**: The source of timing data (the sidecar) must remain explicit on the CLI invocation (`--musicxml`).
- **Validation**: The `convert` command currently only verifies the existence of the sidecar file before proceeding to `build-ir`. It does not perform semantic validation at the orchestration gate. Therefore, the artifact contract must guarantee valid MusicXML.
- **Failure Behaviour**:
  - The `omr` command currently only reports if the subprocess fails or writes to a log.
  - If `convert` receives a structurally invalid sidecar, it will fail downstream during `build-ir` processing.
- **Lessons 3-7 Corpus Acceptance Matrix**:
  - Acceptance requires proving that an explicit Audiveris artifact contract can yield successful alignments and valid `.gp` package generation for the corpus, matching expected output baselines.

## 5. Recommendation

**Smallest First Product Implementation Task**:
Before attempting to orchestrate the full pipeline, the project must establish a proper artifact contract for the `omr` command. The recommended first task is to prove that Audiveris produces a discoverable, valid `.xml`/`.mxl` artifact for a single fixture, and to define the exact pathing and validation rules for that artifact.

## 6. Recogniser Refactoring

Any internal refactoring of note, rest, or symbol recognisers inside `score2gp` is **explicitly deferred**. The priority is establishing the architecture of the timing-source route; recogniser behaviour must not be changed at this stage.
