# Formal Architecture Review Record — CR-07 Bounded Embellishment Attachments Architecture

- **Target Repository**: `tticom/score2gp`
- **Target PR**: #405
- **Head SHA**: `cc2598acfd41ee2c2f49484f3fd387b0becc814e`
- **Branch**: `agy/cr07-bounded-embellishment-attachments-architecture`
- **Reviewer Role**: Architect / Sceptical Reviewer (Hard-Review Protocol)
- **Verdict**: **`APPROVED`**

---

## 1. Summary of Architecture Proposal

Architect task **CR-07** (`docs(design): publish bounded embellishment attachments architecture`) defines a generic, testable, and decoupled technical architecture for detecting and attaching bounded score embellishments (vibrato, slides, bends, hammer-ons, pull-offs, palm muting, let-ring) on the PDF-tab seam.

### Key Architectural Standards Defined:
1. **Decoupled Evidence Models**: Introduces `VisualVibratoEvidence` and `VisualSlideEvidence` Pydantic models in the OMR candidate layer before alignment.
2. **Proximity & String Identity Invariants**: Mandates that visual slides and legato slurs must connect notes sharing the same string identity (or adjacent position coordinates).
3. **Span-Based Embellishment Boundaries**: Requires palm-muting and let-ring spans to be bound via explicit `end_event_id` event ranges rather than unmapped global text scopes.
4. **Bounded Implementation Slice (`CR-07A`)**: Authorizes Developer slice `CR-07A: Bounded Visual Vibrato and Slide Glyphs Evidence Seam` targeting `src/score2gp/pdf_geometry.py`, `src/score2gp/pdf.py`, and `tests/test_cr07_embellishment_attachments.py`.

---

## 2. Adversarial Evidence & Source Code Audit Ledger

| Reference / Claim | Code / Reference Checked | Status | Audit Findings |
| :--- | :--- | :--- | :--- |
| **`ScoreIR` Technique Models** | [`src/score2gp/ir.py#L280-L474`](file:///home/tticom-codex/work/score2gp-workspace/score2gp/src/score2gp/ir.py#L280) | **VERIFIED** | `VibratoTechnique`, `SlideTechnique`, `PalmMuteTechnique`, `LetRingTechnique` exist with exact field attributes as documented. |
| **GPIF Embellishment Serialization** | [`src/score2gp/gpif.py#L790-L805`](file:///home/tticom-codex/work/score2gp-workspace/score2gp/src/score2gp/gpif.py#L790) | **VERIFIED** | `let_ring_notes` and `palm_mute_notes` collections correctly map to GPIF XML nodes `<LetRing>` and `<PalmMute>`. |
| **PDF Extraction Gap** | [`src/score2gp/pdf.py`](file:///home/tticom-codex/work/score2gp-workspace/score2gp/src/score2gp/pdf.py) | **VERIFIED** | Confirmed vector PDF parser lacks visual wavy-line (vibrato) and diagonal-line (slide) candidate extraction. |

---

## 3. Second Opinion & Task Minimization Assessment

- **Second Opinion**: `well supported`
  - The design grounds visual OMR embellishment extraction in existing PyMuPDF vector drawing primitives (`"c"` bezier curves, line segments) and decouples visual candidates from pitch resolution.
- **Task Minimization**:
  - Slice `CR-07A` is strictly bounded to visual vibrato and slide candidate extraction in `pdf_geometry.py` and `pdf.py`, leaving downstream compiler changes to subsequent task slices.

---

## 4. Verdict & Next Task Authorization

- **Verdict**: **`APPROVED`**
- **Authorized Next Action**: Merge PR #405 in `tticom/score2gp`, promote slice **CR-07A** in `score2gp-agentops`, and authorize Developer (`tticom-automation`) to implement `CR-07A`.
