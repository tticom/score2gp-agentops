# FS-03A: Supported Timing-Source Route Architecture

## 1. Provenance and Recorded Routes

**Product SHA**: `e72cd7c8de5277d3d3ba91234c0eea4fbd63e145` (from `score2gp` main)

**Exact Current `convert --musicxml` Route**:
The supported route for PDF conversion invokes `score2gp convert --pdf <path> --musicxml <sidecar_path>`. The command (defined at `src/score2gp/cli.py:658`, `convert_command`):
1. Validates the PDF file.
2. Inspects and extracts tab vectors from the PDF.
3. Requires the MusicXML sidecar path and verifies its existence (`src/score2gp/cli.py:796-847`).
4. Proceeds to `build-ir` if the sidecar and valid vector geometries are provided.

**Standalone `omr` Route**:
The product supports a standalone OMR capability via `score2gp omr <pdf_path> --audiveris <audiveris_path>`. The command (defined at `src/score2gp/cli.py:350`, `omr_command`):
1. Resolves the input PDF and Audiveris executable paths.
2. Invokes Audiveris via a subprocess: `audiveris -batch -export -output <out> <pdf>` (`src/score2gp/cli.py:364-370`).
3. Records stdout/stderr to a log and captures the result/warnings.
It does not validate the input PDF content or establish an explicit artifact contract. It is completely decoupled from the `convert` command.

## 2. Integration Feasibility

Can Audiveris output become a validated MusicXML sidecar in the supported route?
**Unproven.** The current `omr` command merely launches Audiveris as a subprocess and records warnings. It does not establish an explicit output contract, nor has it been proven that it consistently produces a discoverable, valid `.xml` or `.mxl` artifact. While the decoupled architecture allows an artifact to be fed into `convert --musicxml`, the reliable generation and discovery of that artifact remains unverified.

## 3. Route Classification

- **Supported Route**: Providing a valid MusicXML sidecar to `score2gp convert --pdf <path> --musicxml <sidecar_path>`.
- **Unavailable Route**: Fully automated end-to-end `convert` that invisibly invokes Audiveris, or relying on `omr` output without an explicit, proven artifact contract.
- **Uncontrolled Route**: Any uncommitted script or modified entry point that attempts to pipeline `omr` directly into `convert` in a single unmonitored execution.

## 4. Governance Constraints

- **Provenance**: The source of timing data (the sidecar) must remain explicit on the CLI invocation (`--musicxml`).
- **Validation**: The `convert` command currently only verifies the existence of the sidecar file before proceeding to `build-ir`. It does not perform semantic validation at the orchestration gate.
- **Failure Behaviour**:
  - The `omr` command currently only reports if the subprocess fails or writes to a log.
  - If `convert` receives a structurally invalid sidecar, it will fail downstream during `build-ir` processing.
- **Artifact Contract**: The `omr` output contract must concretely define: a configured executable, deterministic output discovery, zero-or-many output refusal, XML/MXL parse and root validation, PDF-to-sidecar binding, hashes, manifest fields, and an explicit handoff to `convert`.
- **Lessons 3-7 Corpus Acceptance Matrix**:
  | Input | Timing Source | Expected Stage | Pass/Refusal Outcome |
  | :--- | :--- | :--- | :--- |
  | `lesson-3.pdf` + Sidecar | Provided via `--musicxml` | `build-ir` | Pass (Valid GP Output) |
  | `lesson-4.pdf` + Sidecar | Provided via `--musicxml` | `build-ir` | Pass (Valid GP Output) |
  | `lesson-5.pdf` + Sidecar | Provided via `--musicxml` | `build-ir` | Pass (Valid GP Output) |
  | `lesson-6.pdf` + Sidecar | Provided via `--musicxml` | `build-ir` | Pass (Valid GP Output) |
  | `lesson-7.pdf` + Sidecar | Provided via `--musicxml` | `build-ir` | Pass (Valid GP Output) |
  | Any PDF + Missing Sidecar | None | `orchestration-gate` | Refusal (`missing_musicxml`) |
  | Any PDF + Invalid Sidecar | Invalid | `build-ir` | Refusal (Parse/Validation Error) |
  | `omr` (No Audiveris) | None | `omr` | Refusal (`audiveris-not-configured`) |
  | `omr` (Multiple Outputs) | Ambiguous | `omr` (Future) | Refusal (Ambiguity Refusal) |

## 5. Recommendation

**Smallest First Product Implementation Task**:
Implement the artifact contract capability for the `omr` command. This bounded task must create the manifest, deterministic output discovery, and XML/MXL validation capabilities for Audiveris output (including ambiguity refusal and hashing), without integrating auto-OMR directly into `convert` or requiring an external OMR executable in public CI.

## 6. Recogniser Refactoring

Any internal refactoring of note, rest, or symbol recognisers inside `score2gp` is **explicitly deferred**. The priority is establishing the architecture of the timing-source route; recogniser behaviour must not be changed at this stage.
