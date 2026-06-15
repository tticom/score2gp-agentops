# Record Product Task 161 completion and authorise Product Task 162

## Product Task 161 Completion

Product Task 161 (Discover and design read-only ledger-line candidate boundary) is complete.

- **Product PR:** [https://github.com/tticom/score2gp/pull/281](https://github.com/tticom/score2gp/pull/281)
- **Final Head SHA:** `26fe76ed7b43d7a1da05f1be142517096de3541e`
- **Merge Commit:** `8e2e4a42158d50263214651dab25d6e32b6e600c`
- **Merged At:** `2026-06-15T09:13:50Z`
- **Exact File Changed:** `docs/design/read-only-ledger-line-candidate-boundary.md`
- **Design Document Path:** `docs/design/read-only-ledger-line-candidate-boundary.md`

### Key Evidence
- Ledger-like evidence exists as `horizontal_stroke` inside `x_aligned_cluster_candidate`.
- The same primitive class (`non_staff_horizontal`) can also become a `beam_candidate` if wide enough, leading to ambiguity.
- The implementation must strictly avoid double-emitting the same primitive as both a beam and a ledger line.

### Recommended Boundary
- Use a standalone `ledger_line_candidate` outcome boundary.
- Support optional `associated_note_candidate_ids`.
- Ensure fail-closed promotion only when geometry directly supports it, and strictly suppress duplicate emission against the `beam_candidate` path.

### Codex Disposition
- Codex correctly identified ambiguity with existing beam candidate emission.
- The design document and PR body were updated to require duplicate suppression or reclassification.
- The Product Task 162 prompt was updated to require tests proving:
  - a ledger-line primitive is not also emitted as a beam candidate;
  - eighth-note composition is not changed by ledger-line promotion.
- The Codex thread was resolved before merge.

### Preserved Non-Goals
- No extraction was implemented.
- No pitch mapping was implemented.
- No assumed-treble mapping was changed.
- No product behaviour was changed.

---

## Authorise Product Task 162

**Title:** `Product Task 162 — Implement read-only ledger-line candidate extraction`

### Scope
- Work in `tticom/score2gp`.
- Implement read-only `ledger_line_candidate` extraction from existing diagnostic evidence.
- Use `docs/design/read-only-ledger-line-candidate-boundary.md` as the controlling design.
- Emit `ledger_line_candidate` objects in the read-only recognition/reporting boundary.
- Add or update public generated fixtures only if required and safe.
- Add tests proving ledger-line candidates are emitted.
- Add tests proving a promoted ledger-line primitive is not also emitted as `beam_candidate`.
- Add tests proving eighth-note composition is not changed by ledger-line promotion.
- Preserve existing `staff_position_index`.
- Preserve existing `assumed_treble_pitch` behaviour.
- Preserve existing whole-note compatibility.
- Preserve default CLI/report behaviour except for the newly authorised read-only candidate exposure.

### Non-Goals
- Do not implement pitch inference.
- Do not implement ledger-line pitch mapping.
- Do not alter `staff_position_index` logic.
- Do not alter assumed-treble mapping.
- Do not implement clef recognition.
- Do not implement accidentals.
- Do not implement key signatures.
- Do not implement rhythm inference.
- Do not emit ScoreIR, MusicXML, Guitar Pro, GP output, OCR, or rests.
- Do not commit private fixtures, diagnostic dumps, scratch JSON, logs, credentials, screenshots, GP files, PDFs, images, or unrelated artifacts.
