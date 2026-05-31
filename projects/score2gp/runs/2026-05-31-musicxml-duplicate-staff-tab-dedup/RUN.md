# Run Record: MusicXML Duplicate Staff/TAB Voice Deduplication

Durable record of deduplication implementation, public test coverage, and private E2E validation for resolving `musicxml_scoreir_polyphony_gate_refused`.

## Metadata
- **Run ID**: `2026-05-31-musicxml-duplicate-staff-tab-dedup`
- **Product Repository**: `tticom/score2gp`
- **Governance Repository**: `tticom/score2gp-agentops`
- **Product Branch**: `feature/musicxml-duplicate-staff-tab-dedup-v0.1`
- **Agentops Branch**: `agent/pdf-to-gp-smoke-v1/tpo`

---

## 1. Architectural Strategy & Implementation

We resolved the polyphony timing blocker without resorting to bypassing the safety gates by implementing a 100% strict duplicate voice detection and deduplication pass:

### Rhythmic Authority & Playability Merger
1. **Deduplication Hook**: Hooked `deduplicate_suspected_staff_tab_voices(musicxml)` at the beginning of `build_ir_with_diagnostics_from_imports` before any timing/preflight checks.
2. **Identification & Classification**:
   - `classify_musicxml_voice_duplication` checks for voice note sets measure by measure.
   - Requires 100% duplicate evidence across active measures: same active measures, identical pitched-note count per measure, identical note onset/duration sequences, stable pitch offset of exactly 0 or 12 semitones, no same-voice overlaps/timing risks, and no chord-stack confusion.
   - Protects against ambiguity: if multiple competing voices could potentially qualify as a duplicate, deduplication is rejected.
   - Emits private-safe diagnostics warnings (e.g., `musicxml_duplicate_staff_tab_detected`, `musicxml_duplicate_staff_tab_dedup_applied`, etc.)
3. **Preserving TAB Evidence Without Duplicate Timing**:
   - Copies techniques (slides, bends, vibratos, hammer-ons, pull-offs, slurs) and ties from the duplicate TAB voice note into the standard notation note.
   - Stores rich duplicate TAB note metadata (`dedup_tab_note_id`, `dedup_tab_note_voice`, `dedup_tab_note_staff`, etc.) on the notation note for downstream alignment.
   - Sets `n2.is_suppressed = True` on the duplicate TAB voice notes.
4. **Preflight Timing Safety**:
   - `analyze_musicxml_timing` ignores suppressed notes, completely bypassing cross-voice timeline overlaps and avoiding gate refusals under default `allow_remediation=False`.
5. **Rhythmic Timelines & Target Staff**:
   - Suppressed notes are ignored during target staff selection in `build_ir.py`.
   - The standard notation staff (Staff 1) is automatically chosen as `target_staff` and serves as the rhythmic authority.
6. **ScoreIR Double-Provenance**:
   - `_aligned_note` appends both the standard notation note provenance and the TAB-voice note provenance alongside the matched `TabCandidate` provenance, preserving a complete paper trail.

---

## 2. E2E Smoke Metrics

Running the E2E smoke tests on the private melodic soloing guitar score yielded outstanding results. The score successfully bypasses the timing gate and outputs a fully serialized GP package under default `allow_remediation=False`!

| Input Score | Type | Pages | Extract | Playable Frets | ScoreIR | GP | Failure Reason | Next Recommendation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `private_input_custom_melodic_soloing` | `pdf-tab-musicxml` | 1 | Yes | 59 | Yes | Yes | `none` | `inspect-poor-or-unknown-bars-before-conversion` |
| `private_input_custom_lesson_3` | `pdf-tab-musicxml` | 4 | Yes | 454 | Yes | Yes | `none` | `inspect-poor-or-unknown-bars-before-conversion` |
| `private_input_custom_lesson_4` | `pdf-tab-musicxml` | 5 | Yes | 549 | Yes | Yes | `none` | `inspect-poor-or-unknown-bars-before-conversion` |
| `private_input_custom_lesson_5` | `pdf-tab-musicxml` | 3 | Yes | 297 | Yes | Yes | `none` | `inspect-poor-or-unknown-bars-before-conversion` |
| `private_input_custom_lesson_6` | `pdf-tab-musicxml` | 6 | Yes | 115 | Yes | Yes | `none` | `inspect-poor-or-unknown-bars-before-conversion` |
| `private_input_custom_lesson_7` | `pdf-tab-musicxml` | 5 | Yes | 624 | Yes | Yes | `none` | `inspect-warning-bars-before-conversion` |

- **Former Blocker**: `musicxml_scoreir_polyphony_gate_refused` -> **Resolved 100%**.
- **Layout Spacing**: The large-spaced detector remained active and detected all TAB systems properly.
- **GP packages generated successfully**: Yes.

---

## 3. Public Test Verification

We added 7 comprehensive synthetic test cases in `tests/test_musicxml_polyphony_diagnostics_edge_cases.py` verifying all boundary conditions:

1. `test_duplicate_staff_tab_voice_detected`: Verifies duplicate voice pairs are correctly identified.
2. `test_duplicate_staff_tab_voice_unified`: Confirms single ScoreIR timeline is generated, techniques/ties are merged, and double-provenance is present.
3. `test_genuine_independent_polyphony_still_refuses`: Ensures differing rhythms remain refused by the polyphony gate.
4. `test_valid_chord_stack_not_misclassified_as_duplicate`: Chord stacks inside the same voice are left untouched.
5. `test_partial_duplicate_emits_warning`: Partial mismatches emit `musicxml_duplicate_staff_tab_partial_match` and do not deduplicate.
6. `test_same_voice_timing_error_still_refuses_after_dedup`: Verifies same-voice timing overlap errors inside either voice are still refused.
7. `test_multiple_candidate_duplicate_pairs_refuse_as_ambiguous`: Down-grades and rejects deduplication if more than one matching duplicate pair exists to prevent layout ambiguity.

**All 421 tests in the repository pass perfectly.**

---

## 4. Private-Safety Audit

- Verification Command: `git ls-files fixtures/private work`
- Output: `fixtures/private/.gitkeep`
- **Result**: **No private files, private PDFs, or work outputs were committed.** The private-safety invariant is strictly maintained.

---

## 5. Recommended Next Branch

`feature/gpif-technique-verification-v0.1`
Verify full serialization details for advanced guitar techniques (bends, slides, slurs, hammer-ons, and pull-offs) in the output GPIF/GP package structures.
