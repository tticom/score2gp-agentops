# Decision: Tab-Only Timing Policy A+B+C

## Context
Architect research concluded (Outcome C) that precise tab-only rhythm inference is not deterministically viable given the lack of explicit timing evidence (like stems/beams) and the elasticity of tab spatial layout. This outcome was approved as evidence-backed by the Reviewer.

The project must decide how `--pdf-only-tab` handles tab-only PDFs lacking timing evidence without misleading users.

## Decision

The Supervisor authorises the following A+B+C product policy for tab-only rhythm handling:

### A. Default / Approximate Output
When `--pdf-only-tab` is used on tab-only input and reliable timing evidence is absent, Score2GP may produce a GP output using approximate/default timing (e.g., fallback grid assignment).
- The output must not be represented as precise.
- The pipeline must emit or preserve a visible warning/provenance marker.
- Existing warning keys (e.g., `pdf_only_tab_inferred_timing`) must be preserved or strengthened.
- User-facing CLI output and structured diagnostics must make the approximation clear.

### B. Strict Rejection
When the user or caller requests precise timing and reliable timing evidence is missing, Score2GP must reject/fail cleanly.
- Implementation should inspect existing CLI/API options and either use a suitable existing flag or add a new minimal explicit option like `--require-precise-timing`.
- It must fail before producing a misleading GP file.
- It must return a clear error or diagnostic stating that tab-only input lacks reliable timing evidence and requires MusicXML/sidecar or explicit timing evidence for precise rhythm.

### C. Precise Mode Requires Reliable Evidence
Precise rhythm conversion is only allowed when reliable timing evidence is available.
- Supported mechanisms include MusicXML/sidecar timing alignment and already-supported explicit markers.
- New standard-notation PDF-only timing inference or general tab rhythm inference is **not authorised**.

### D. ML-Assisted Extraction
ML-assisted tab rhythm extraction remains a future/nice-to-have direction only and is **not authorised**.

## Consequences
- The Developer is now authorised to implement this bounded A+B+C policy.
- The Developer task must not expand into broad rhythm inference or ML.
- Sidecar/precise path preservation must be ensured via tests.
