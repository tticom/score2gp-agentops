# Post-Semantic-Candidate Strategy and Backlog Architecture

**Date**: 2026-07-09
**Role**: Architect
**Scope**: Epic C (Post-Req-122 Appraisal & Strategy)

## 1. Review of Epic C Hardening Sequence (Req-111 to Req-122)

The completed tasks successfully hardened the observability, safety, and correctness of semantic candidate diagnostics:
- **Observability**: `LogicalClefCandidate` and `QuarterRestCandidate` diagnostics are exposed via `inspect-pdf` and `note-candidate-recognition` CLI outputs.
- **Fail-Closed Boundary**: We proved that complex rests (whole/half rests), noise, and overlapping polyphonic clusters are safely ignored, preventing invalid quarter rest classifications.
- **Zero-Leakage**: We established a strict boundary verifying that diagnostic candidates do not leak into downstream ScoreIR translation or GP packages.

---

## 2. Strategic Answers

### Q1: Is the current clef/rest candidate extraction mature enough for mapping work?
**Verdict**: **No**.
The current model only extracts candidates for a single clef class (treble) and a single rest class (isolated quarter rests). Rushing to map these into production ScoreIR or GP structures at this stage is highly premature because:
1. We do not support other basic clefs (like Bass or Alto) or other rest values (whole, half, eighth), which are necessary to compile any complete, valid musical system.
2. We lack the pitch translation engine that maps note staff position indices (like `staff_position_index = 4`) into actual MIDI pitches based on the active clef.
3. We do not have a rhythm timeline or voice cursor that supports inserting silence/rests into the ScoreIR timeline, since ScoreIR currently relies entirely on synthetic MusicXML timing alignment.

### Q2: What evidence is still missing before rhythm or pitch?
- **For Pitch Mapping**:
  - Heuristics to detect and validate Bass and Alto clefs.
  - A robust model associating ledger lines and accidentals to noteheads.
  - A clef-aware pitch conversion lookup table mapping staff positions to MIDI.
- **For Rhythm/Rest Mapping**:
  - Handlers for complex rests (whole rests, half rests, eighth/sixteenth rests).
  - Sync rules for polyphonic systems where rests share vertical space with notes in other voices.
  - A standalone rhythm/timeline inference parser.

### Q3: What should the next work phase target?
**Recommendation**: **Real-World Corpus Audit & Candidate Model Consolidation**.
Our heuristics were developed and validated using pristine, synthetically generated PDF fixtures. Real-world scores introduce scan skew, diverse layout parameters, line thickness anomalies, and handwritten artifacts that could trigger high false-positive rates. Before we commit to mapping these features into ScoreIR, we must audit them against a representative real-world PDF corpus and consolidate the candidate models.

### Q4: Which tasks must remain blocked?
- Pitch inference / clef-based note conversion in ScoreIR.
- Timeline duration inference / stand-alone rhythm reconstruction.
- Direct rest injection into playable GP files.

---

## 3. Prioritised Req-123+ Backlog Architecture

We propose the following sequence of tasks for the next phase:

### Req-123: Real-World PDF Corpus Audit for Semantic Candidates
- **Priority**: P2
- **Owner Role**: Architect/Developer
- **Allowed Repository**: `score2gp`
- **Purpose**: Run semantic candidate extraction over a set of real-world/scanned PDF files to calculate false positive rates and identify boundary failures.
- **Ready Criteria**: Bounded list of real-world PDF test fixtures compiled.
- **Done Criteria**: Audit report published in `score2gp-agentops` detailing failure modes, heuristic adjustments, and recommended bounds.

### Req-124: Semantic Candidate Model Consolidation & Schema Hardening
- **Priority**: P2
- **Owner Role**: Developer
- **Allowed Repository**: `score2gp`
- **Purpose**: Refine candidate schemas (`LogicalClefCandidate`, `QuarterRestCandidate`) and pydantic models based on Req-123 audit findings.
- **Ready Criteria**: Req-123 audit report completed.
- **Done Criteria**: Updated candidate schemas committed to `schemas/` and all unit/snapshot tests updated and passing.

### Req-125: Multi-Clef Candidate Classification (Bass and Alto)
- **Priority**: P2 (Blocked by Req-124)
- **Owner Role**: Developer
- **Allowed Repository**: `score2gp`
- **Purpose**: Extend left-margin classifiers to extract Bass and Alto clef geometries without OCR.
- **Ready Criteria**: Req-124 schema consolidation complete.
- **Done Criteria**: Integration and unit tests proving correct classification of treble, bass, and alto clefs on public fixtures.

### Req-126: Whole and Half Rest Candidate Extraction
- **Priority**: P2 (Blocked by Req-124)
- **Owner Role**: Developer
- **Allowed Repository**: `score2gp`
- **Purpose**: Implement staff-line alignment and aspect ratio heuristics to extract whole note rest and half note rest candidates.
- **Ready Criteria**: Req-124 schema consolidation complete.
- **Done Criteria**: Snapshot and unit tests proving correct extraction and fail-closed isolation of whole and half rests.

### Req-127: Clef-Aware Pitch Mapping Schema
- **Priority**: P1 (Blocked by Req-125)
- **Owner Role**: Architect
- **Allowed Repository**: `score2gp-agentops`
- **Purpose**: Design the lookup tables and metadata schema for mapping staff positions to MIDI pitches based on the detected clef candidate.
- **Ready Criteria**: Req-125 (multi-clef) complete.
- **Done Criteria**: Pitch translation lookup document approved and checked in.
