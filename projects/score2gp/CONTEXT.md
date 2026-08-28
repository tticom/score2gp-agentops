# Recognition Ubiquitous Language & Context

This glossary defines the canonical vocabulary for the Score2GP Recognition layer. Every domain term has one meaning, and each term must be owned by the correct stage to prevent semantic leakage.

## Core Vocabulary

### 1. Observation
- **Meaning:** A raw, typed fact acquired deterministically from the source material (e.g., a vector line, a text string, a raster pixel region) combined with coordinates, modality, and provenance.
- **Stage Ownership:** Stage 1 (Acquisition / Raster Observation Adapter).
- **Invariants:** Observation contracts MUST NOT contain any musical assignments, staff associations, or duration semantics. They are purely physical properties of the document.

### 2. Hypothesis
- **Meaning:** A provisional interpretation of one or more Observations (e.g., a line might be a stem or a barline, a text string might be a fret number). 
- **Stage Ownership:** Stage 2 (Hypothesis Generation / Token Evidence).
- **Invariants:** Hypotheses preserve alternatives and conflicts. A hypothesis never asserts final musical truth and must carry its explicit provenance.

### 3. Document Topology
- **Meaning:** The structured, hierarchical layout of the page (Pages, Reading Order, Systems, Notation/TAB Staff Regions).
- **Stage Ownership:** Stage 3 (Staff and System Topology).
- **Invariants:** Must reconstruct the stable identities of staff groupings and pairings. Refuses unsupported layouts instead of mutating them.

### 4. Physical Division
- **Meaning:** Vertical boundaries identified on the page (e.g., repeating barlines, structural barlines) that segment the Document Topology horizontally.
- **Stage Ownership:** Stage 4 (Physical Divisions).
- **Invariants:** These are geometric divisions on the staff, independent of logical measure boundaries.

### 5. Measure Boundary
- **Meaning:** The resolved, logical encapsulation of musical time based on Physical Divisions, staff spans, and system alignment.
- **Stage Ownership:** Stage 4 (Measure Topology) & Stage 5 (Page-Continuous Topology).
- **Invariants:** Must cover fragmented, floating, double, and repeat-adjacent cases. Defines the strict boundaries within which events are grouped.

### 6. Recognition Graph
- **Meaning:** An assembled graph of typed nodes (e.g., Notehead, Stem) and bounded relations (e.g., `IN_STAFF`, `ATTACHED_TO_STEM`, `SAME_ONSET`, `CONFLICTS_WITH`).
- **Stage Ownership:** Stage 6 (Recognition Graph Assembler).
- **Invariants:** Assembles all hypotheses and topological constraints into a single network of competing interpretations. It makes no final decisions.

### 7. Resolution
- **Meaning:** The process of applying hard and soft constraints to the Recognition Graph to yield a single, non-contradictory musical outcome.
- **Stage Ownership:** Stage 7 (Constrained Semantic Resolver).
- **Invariants:** Returns specific, bounded outcomes: Resolved, Ambiguous, Unsupported, or Contradictory. It MUST NEVER coerce inconsistent physical observations into an assumed musical capacity.

### 8. Musical Document
- **Meaning:** The final, typed structural interface output by the Recognition layer, ready to be mapped into the ScoreIR compiler path.
- **Stage Ownership:** Stage 8 (Musical Document Compiler).
- **Invariants:** Represents stable, domain-oriented semantics (Tempo, Tracks, Events) fully decoupled from the original geometry and layout.

### 9. Abstention
- **Meaning:** A deliberate, fail-closed refusal by any stage to emit an unsupported or contradictory semantic, rather than guessing or scaling it.
- **Stage Ownership:** All Stages.
- **Invariants:** Any unresolvable conflict must bubble up as an Abstention (or `Unsupported` state), protecting the downstream compilation path.

## Stage Ownership and Semantic Leakage
- **Forbidden Leakage:** A stage MUST NOT assign semantics owned by a later stage to satisfy its own invariants. (e.g., Stage 1 Observations cannot assign string ownership; Stage 6 Graph cannot resolve chord durations).
- **Provenance Preservation:** All final decisions in the Musical Document must maintain a traceable path back through the Recognition Graph to the original Observations.
