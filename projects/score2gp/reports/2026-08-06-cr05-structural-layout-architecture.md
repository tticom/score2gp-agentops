# CR-05 Architecture Report: Structural Layout, Barline Decoupling, and Title Ownership

**Date**: 2026-08-06  
**Task**: CR-05: Structural Layout and Titles Architecture  
**Repository**: `tticom/score2gp` / `tticom/score2gp-agentops`  
**Authorised Identity**: `tticom-automation`  
**Role**: Architect  

---

## 1. Executive Summary & Objective

Task `CR-05` investigates structural layout, barline classification, and title/text ownership in `score2gp`. The objective is to define a generic, testable architecture for independently classifying:
1. Ordinary, double, and final barlines (`regular`, `double`, `end`, `section`, `repeat-start`, `repeat-end`).
2. System and page layout breaks (`line`, `page`, `none`).
3. Phrase or piece titles and their ownership by a system or measure.

**Key Rule**: A double or final barline must **never** imply a system break merely because of its barline type. System layout breaks must be inferred independently from spatial staff geometry.

---

## 2. Baseline & Codebase Verification

- **Accepted Baseline**: Commit `f3cf042c96defdaf09c3353f16f9dbcb38e542d3` / `origin/main` (`a9b127c311617dced5422e97e46a7bab840f7981`).
- **Codebase Verification**: Executed `python scripts/agent_verify.py` in `score2gp` (task-285). Verification overall status: **`PASS`**.
- **Path Tracing**:
  - `src/score2gp/ir.py` (L676, L678): Defines `Bar` with distinct `layout_break` (`"line"`, `"page"`, `"none"`) and `barline` (`"regular"`, `"double"`, `"end"`, `"section"`, etc.).
  - `src/score2gp/pdf_staff_geometry.py`: Extracts staff bounding boxes and vertical barline stroke candidates (`StructuralSkeletonBarlineCandidate`).
  - `src/score2gp/pdf.py`: Extracts vector text primitives near staves.

---

## 3. Required State Separation & Architecture

The architecture mandates strict decoupling across the following independent states:

| Dimension | Representation | Primary Evidence |
| :--- | :--- | :--- |
| **Barline Type** | `regular`, `double`, `end`, `section`, `repeat-start`, `repeat-end` | Vertical stroke thickness, count (dual lines), and repeat dots |
| **System Break** | `layout_break: "line"` | Vertical Y-displacement exceeding system staff height |
| **Page Break** | `layout_break: "page"` | Y-coordinate reset or page index transition |
| **Title / Text** | `piece_title`, `phrase_title`, `technique_text` | Font size, horizontal alignment, and bounding box Y-distance |
| **System Ownership** | `system_index: int` | Spatial containment in system header region |
| **Measure Ownership** | `measure_index: int` | Horizontal X-range overlap with measure grid bounds |

---

## 4. Disconfirmation & Falsification Matrix

1. **Disconfirmed**: *Every double barline implies a new system break.*  
   - **Counter-example**: A double barline at a key or time signature change mid-system must retain `layout_break: "none"`.
2. **Disconfirmed**: *Every system break requires a double barline.*  
   - **Counter-example**: Standard line breaks at system right margins end with regular single barlines (`barline: "regular"`, `layout_break: "line"`).
3. **Disconfirmed**: *Page-edge proximity causes a system break.*  
   - **Counter-example**: Staff margins near top/bottom page bounds must evaluate Y-delta to adjacent staves, not absolute page height.
4. **Disconfirmed**: *Arbitrary text above a staff becomes a piece title.*  
   - **Counter-example**: Technique text (e.g. "P.M.", "Let Ring") above a staff must be classified separately from titles.

---

## 5. Decision & Bounded Developer Slice

**Decision**: **`CONTINUE`** to a single, bounded Developer slice (`CR-05B`).

### Developer Implementation Slice Proposal (CR-05B)
- **Scope**: Decouple barline style from layout break in `build_ir.py` and enforce independent `layout_break` assignment.
- **Allowed Product Files**:
  - `src/score2gp/build_ir.py`
  - `src/score2gp/pdf_staff_geometry.py`
  - `tests/test_cli_convert.py`
- **Validation Commands**:
  - `PYTHONPATH=. pytest tests/test_cli_convert.py`
  - `python scripts/agent_verify.py`
