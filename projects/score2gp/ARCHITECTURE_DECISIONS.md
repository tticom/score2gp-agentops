# ScoreToGP Architecture Decisions (ADR)

This document records the architectural decisions governing agent workflows and review posture for the ScoreToGP project.

---

## ADR-001: Separate Product Repo from Agent-Governance Repo
- **Status**: **Approved**
- **Decision**: Product logic, CLI commands, tests, and public schemas live in `score2gp`. Agent governance, sceptical review rules, prompt templates, and benchmark ladders live in `score2gp-agentops`.
- **Reason**: Decoupling the control plane (agent instruction) from the data plane (product logic) prevents product codebases from being polluted with LLM coordinating prose or brittle prompts.

## ADR-002: Reviewer/Architect Agent Must Review Before Prompting
- **Status**: **Approved**
- **Decision**: The reviewer agent must verify all local evidence and checks before generating the next implementation prompt.
- **Reason**: Ensures next implementation prompts are grounded in strict observed failures and verified evidence, preventing "blind steering" or recurring loop regressions.

## ADR-003: Visual/Source Evidence Outranks Generated Diagnostic Summaries
- **Status**: **Approved**
- **Decision**: Direct visual/source page inspection always outranks intermediate diagnostic tables, summaries, or logs. If they disagree, the tool output is assumed to be wrong.
- **Reason**: Diagnostic tables are compiled by the compiler itself and can easily mis-index or omit failures (e.g. failing to capture Measures 15 & 16 in the PDF).

## ADR-004: Strict, Remediation, Semantic, and File Existence Are Separate States
- **Status**: **Approved**
- **Decision**: Every review and prompt must report strict mode, remediation mode, semantic comparison, and generated-file existence separately.
- **Reason**: Combining these metrics creates false confidence. An output file existing does not imply semantic correctness, and remediation success does not prove strict gate compliance.

## ADR-005: Private Benchmarks Are Local Diagnostics, Not Public Fixtures
- **Status**: **Approved**
- **Decision**: Private lesson PDFs and GP oracle files must remain strictly private and outside version control. They guide local human-verified diagnosis but must never be committed to either repository.
- **Reason**: Respects intellectual property boundaries, prevents data leakage, and preserves repository hygiene.

## ADR-006: Forbid Biomechanical Position Inference
- **Status**: **Approved (2026-08-13)**
- **Decision**: The system must not attempt to infer biomechanical hand positions (e.g. sequential finger stretches or jumps) when string/fret data is missing. It must rely strictly on explicit TAB evidence provided by the OMR. Notes lacking explicit fretboard ownership must be explicitly dropped or result in a clear error.
- **Reason**: Musicians play chords as unified hand shapes, and stylistic variations exist across different players (e.g. preferring jumps vs. stretches). Inferring physical positions without explicit notation leads to musically corrupt outputs and silent failures (such as the previous synthetic `(string=1, fret=0)` injections). Relying strictly on the TAB provides a deterministic, faithful representation of the score.

## ADR-007: Own Native Extraction Layer and Retire Audiveris
- **Status**: **Conditional Recommendation (2026-08-20)**
- **Decision**: Score2GP will build and own a native vector-based recognition layer instead of consuming a third-party recognition object. Audiveris is recommended for retirement due to its unsuitability for modern born-digital instructional PDFs (e.g. failing on floating barlines and irregular layouts).
- **Reason**: Commercial alternatives like PDFtoMusic Pro are proprietary and brittle on messy instructional layouts. An owned vector pipeline allows us to specifically target the heuristic needs of instructional scores, including layout resilience, geometric rhythm extraction, and floating barlines.

## ADR-008: Guitar Pro Output Targets Are Pluggable Modules Behind a Versioned Interface
- **Status**: **Proposed (2026-09-25)**. Awaits maintainer acceptance, together with the open questions in REQ-0002 §12.
- **Requirement**: [REQ-0002](requirements/REQ-0002-pluggable-gp-output-targets.md)
- **Context**: The product writes one GPIF-in-ZIP package and then post-processes it into "GP6" and "GP8" (`src/score2gp/version_adapter.py`). Comparison with real Guitar Pro 8.1.0 and 8.1.4 files shows that the adapter invents tags and version stamps, and that its "GP6" output is a ZIP, whereas real GP6 files use the BCFZ/BCFS `.gpx` container. Guitar Pro spans three unrelated encodings: binary GP3–5, GPIF in BCFZ/BCFS (GP6), and GPIF in ZIP (GP7/8). The maintainer requires GP5–GP8 output, with future versions added as bolt-on modules.
- **Decision**:
  1. Output is produced by **output targets**. Each target implements a versioned interface: identity, capability matrix, `compile(canonical document, options) -> package + report`, and self-validation.
  2. Targets are found through a **registry**. First-party and separately installed targets register the same way, and core code never names a concrete target.
  3. Targets are grouped by **family** (binary, GPIF-BCFZ, GPIF-ZIP). Version differences within a family are **profiles** built from Guitar Pro-authored evidence, not conditionals.
  4. Before writing, the **capability check** refuses, or under explicit policy degrades with a report, every canonical feature the target cannot represent. Silent loss is forbidden.
  5. The canonical musical document is target-neutral. Targets never infer musical semantics.
  6. Each target is accepted independently: an independent reader, plus an open/play/save/reopen round trip in that Guitar Pro version.
- **Alternatives rejected**:
  - One writer with post-hoc per-version patching (the current design). It cannot express different containers or encodings, and it has already produced fabricated output.
  - Version conditionals inside `gpif.py`. This couples every version to one module and makes adding a version a core change.
  - Delegating to an external converter. Guitar Pro has no headless converter, and alphaTab exports only GP7.
- **Deferred**: Whether targets ship in this repository or as separate packages (the dormant `score2gp-exporter` scaffold) is a packaging decision for OUT-02.
- **Consequences**:
  - The current adapter's GP6/GP8 paths must be contained (REQ-0002 OUT-01) before the interface exists.
  - Target acceptance requires access to each Guitar Pro version and licensing decisions per dependency.
  - The pytest-conditional serializer and the canonical clamps must be removed first, so that target tests exercise production output and target limits are enforced by capability checks rather than by silent clamping.
