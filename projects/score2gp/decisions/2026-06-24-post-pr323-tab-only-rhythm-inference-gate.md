# Decision: Record PR #323 Completion and Authorise Tab-Only Rhythm Inference Gate

## Context
Product PR #323 has been successfully merged into `tticom/score2gp`.
* **PR:** https://github.com/tticom/score2gp/pull/323
* **Merged Head SHA:** `bcbad586b8d9e28cf4ad130db0c0532db783b020`
* **Merge Commit:** `6afdd3195f37eca6e319caf33dbeccfbbf1d4b5c`
* **Title:** `feat: tab-only quarter rest candidate wiring`

This PR wires existing quarter-rest vector candidate extraction into the `--pdf-only-tab` path. This is real product progress and is now the accepted baseline.

## Unresolved Issues / Limitations
The product still lacks general tab-only rhythm inference:
1. Only quarter rests are supported. Whole, half, eighth, and sixteenth rests remain unsupported.
2. Broader bar-level rhythm reconstruction is not implemented.

## Active Blocker
The active blocker is no longer "can we recognise tab-only quarter rests?", as this is now baseline capability.
The active blocker is:
**Can Score2GP infer rhythm for tab-only PDF input using deterministic evidence from raster/vector/tab geometry, with enough reliability to justify implementation?**

## Next Authorised Task
The next authorised task is **Architect research only**. Developer implementation is blocked.
The Architect must answer the active blocker question and return exactly one of these outcomes:

### Outcome A
The current deterministic raster/vector/tab-geometry path is viable for tab-only rhythm inference on a defined fixture set. Developer work may be authorised only after Reviewer architecture verification approves the evidence and approach.

### Outcome B
The current deterministic path is not viable, but another concrete non-ML approach is viable. The Architect must define the alternative approach, required fixtures, measurable success criteria, and implementation boundary. Developer work remains blocked until Reviewer architecture verification approves it.

### Outcome C
No credible deterministic or non-ML path is currently viable. Developer work is not authorised. The project must stop or pivot, including considering model-assisted recognition or a different extraction architecture.

## Implementation Authorisation
* **Developer implementation is strictly prohibited** until an architecture path (Outcome A or B) has been concretely defined by an Architect and approved by a Reviewer via architecture verification.
