# Guitar Pitch Range Validation & Transposition Correction

## Session Summary

- **Product Branch:** `agent/pdf-to-gp-smoke-v1/developer`
- **Product Commit:** `2f552363b290d915e361d6c856c6d8375af572f2`
- **Task Overview:** Fulfill the distillation and implementation of physical guitar pitch range validation based on the `guitar_pitch_range.md` domain knowledge, implement an octave-clef alignment transposition correction strategy, and create invalid IR tests.

---

## 1. Problem & Context

1. **Physical Guitar Limits:** Standard 6-string guitar tuning (`[40, 45, 50, 55, 59, 64]`) has strict physical boundaries. The lowest note is E2 sounding (MIDI 40). A standard 24-fret guitar's highest pitch is E6 sounding (MIDI 88). Pitches outside `[40, 88]` are physically impossible to play.
2. **Written vs. Sounding Octave transpositions:** The guitar is an octave-transposing instrument. Sheet music represents notes 1 octave higher than they sound. If OMR parses standard treble clef written notes directly, they contain a 12-semitone pitch offset compared to physical sounding pitches.
3. **No Safety Validation:** Previously, ScoreIR did not assert absolute physical pitch limits, allowing impossible pitches to go unchecked.

---

## 2. Implementation & Corrective Strategy

1. **Semantic Pitch Bounds Check:** Added a validation check to `ScoreIR.semantic_errors()` in [ir.py](file:///\\wsl.localhost\Ubuntu-24.04\home\tticom\work\score2gp-workspace\score2gp\src\score2gp\ir.py). If standard 6-string guitar tuning is detected, any note with sounding pitch `< 40` or `> 88` triggers a clear semantic error message.
2. **Octave clef transposition correction:** Modified `_aligned_note()` in [build_ir.py](file:///\\wsl.localhost\Ubuntu-24.04\home\tticom\work\score2gp-workspace\score2gp\src\score2gp\build_ir.py) to calculate mismatch differences modulo 12. If a pitch mismatch is exactly a multiple of 12 semitones, it is treated as a standard clef transposition offset. The compiler automatically logs a lightweight `musicxml-transposition-corrected` info/warning and aligns it with the physical tab-derived sounding pitch.
3. **Robust Test Suite Integration:**
   - Created [impossible_guitar_pitch_low.ir.json](file:///\\wsl.localhost\Ubuntu-24.04\home\tticom\work\score2gp-workspace\score2gp\fixtures\public\invalid\impossible_guitar_pitch_low.ir.json) (pitch 39)
   - Created [impossible_guitar_pitch_high.ir.json](file:///\\wsl.localhost\Ubuntu-24.04\home\tticom\work\score2gp-workspace\score2gp\fixtures\public\invalid\impossible_guitar_pitch_high.ir.json) (pitch 89)
   - Parameterized both in `tests/test_ir.py` to ensure they raise precise, readable semantic errors under the automated test suite.

---

## 3. Verification & Compliance

### Automated Tests
Ran pytest successfully, achieving **393/393 passed** (including the two new validation cases):
```bash
wsl .venv/bin/python -m pytest
```

### CLI Verification
Ran `validate-ir` successfully:
```bash
wsl .venv/bin/python -m score2gp.cli validate-ir fixtures/public/invalid/impossible_guitar_pitch_low.ir.json
wsl .venv/bin/python -m score2gp.cli validate-ir fixtures/public/invalid/impossible_guitar_pitch_high.ir.json
```
Both rejected invalid inputs with high-fidelity, musician-readable error descriptions.

### Compliance Safety Checks
- Git check command `git diff --check` passed with 0 errors.
- Private-safety invariant check `git ls-files fixtures/private work` returned strictly:
  `fixtures/private/.gitkeep`
