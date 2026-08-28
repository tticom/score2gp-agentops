# Recognition Architecture v1

**Status:** Accepted
**Date:** 2026-08-28
**Context:** NPG-00R & REC-00

## Architecture Decision

The Score2GP Recognition layer will adopt a **hybrid vector/raster, topology-first architecture**.

This architecture explicitly deprecates the legacy "geometry-first" model, which suffered from premature semantic scaling, aggressive coordinate snapping (e.g. 300pt hacks), and semantic leakage where acquisition stages made implicit musical assumptions.

### Key Pillars
1. **Topology-First Layout Extraction:** Systems, staves, and measures are structurally mapped (Document Topology) BEFORE any individual musical events or rhythms are interpreted. This ensures that floating barlines, layout fragmentation, and multi-staff structures form an immutable grid.
2. **Hybrid Vector/Raster Acquisition:** Initial primitive extraction prioritizes pristine vector geometry from digital-native PDFs. Raster/pixel evidence serves strictly as supplementary or diagnostic observations that may support or contradict the vector data, but never unilaterally mutate it.
3. **Graph-Based Competing Hypotheses:** All candidate geometry is loaded into a Recognition Graph. Competing hypotheses (e.g. fret `1 0` vs `10`) are preserved with their exact provenance until a Constrained Semantic Resolver applies hard musical invariants to adjudicate them.
4. **Fail-Closed Resolution (Abstention):** The system relies on explicit constraints. Any unresolvable contradiction immediately triggers a fail-closed `Unsupported` or `Ambiguous` state. The recognition pipeline is forbidden from "guessing", scaling durations, or coercing events to fit a measure's capacity.

## Rejected Alternatives

### 1. Pure Black-Box Machine Learning (e.g. Oemer)
- **Why Rejected:** ML models fail to meet the deterministic baseline and reproducibility requirements. They discard the perfectly accurate, digital-native vector instructions inherent in our PDFs in favor of probabilistic raster inferences. They also present unproven privacy and licensing risks, and their failures are difficult to geometrically diagnose or mechanically patch.

### 2. Commercial / Proprietary OCR Engines (e.g. PDFtoMusic Pro)
- **Why Rejected:** Commercial EULAs explicitly prohibit headless integration and distribution as a dependency for an open-source tool. The closed-source nature makes debugging layout resilience (like floating barlines) impossible.

### 3. Continuation of the "Geometry-First" Legacy (Audiveris fallback)
- **Why Rejected:** The legacy approach tightly coupled the parsing of line segments directly into musical event instantiation. This resulted in semantic leakage where raw line widths forced incorrect staff classification. It was fundamentally incapable of handling instructional layout quirks, repeatedly breaking bounds checks (`Capacity mismatch: Measure 1 is invalid`) and driving the addition of fragile, sweeping heuristic workarounds.
