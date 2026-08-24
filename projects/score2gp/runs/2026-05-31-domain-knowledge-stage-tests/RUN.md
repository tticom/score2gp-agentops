# Domain Knowledge and Stage Integration Test Foundation

## Session Summary

- **Product Branch:** `research/domain-knowledge-stage-tests-v1`
- **AgentOps Branch:** `agent/pdf-to-gp-smoke-v1/tpo`
- **Task Overview:** Build the foundation for a domain-driven integration test system, including creating/improving `docs/domain/` documentation and building a comprehensive first suite of stage integration tests under `tests/integration/domain_contracts/`.

---

## 1. Problem & Context

1. **Unrealistic Pitch and Musical Correctness:** Standard "smoke.gp" generated outputs had severe pitch realism issues. Passing simple unit/module tests is insufficient; the pipeline requires rigorous stage-by-stage contract validation against verified guitar domain knowledge before downstream stages can be trusted.
2. **Comprehensive Domain Integration:** Establish clear boundaries across stages (PDF evidence extraction, tab event parsing, MusicXML alignment, ScoreIR construction, GP8 output creation) and turn these rules into executable, immutable contract tests.

---

## 2. Implementation & Corrective Work

1. **Verified Domain Documentation:**
   - Improved and consolidated all files under `docs/domain/` mapping verified guitar facts, transposition rules, timing capacity, and validation contracts.
   - Formally created `docs/domain/intermediate-products.md` mapping actual pipeline stages, inputs/outputs, invariants, and failure modes.
   - Created `docs/domain/domain-test-matrix.md` linking verified domain facts to specific test scenarios.
   - Maintained `docs/domain/unresolved-questions.md` to track open empirical unknowns.
2. **Immutable Integration Test Suite:**
   - Implemented 4 contract modules under `tests/integration/domain_contracts/`:
     - `test_tablature_semantics.py`: Ensures string/fret bounds and multi-digit fret parsing.
     - `test_timing_and_voices.py`: Verifies compound time signature capacity (12/8 ticks) and simultaneous chord onset alignment.
     - `test_guitar_pitch_validation.py`: Enforces physical standard guitar sounding pitch limits `[40, 88]` MIDI.
     - `test_intermediate_products.py`: Verifies intermediate stage sequencing and transposing written octave representation (G2 sounding maps to written octave 3 / concert octave 3 / transposed octave 4).
3. **Execution & Fixes:**
   - Fixed `test_guitar_pitch_validation.py` to assert that `score` is `None` upon validation failure.
   - Fixed `test_timing_and_voices.py` to use correct `MusicXmlNote` attributes (`duration_divisions`, `onset_divisions`) and check `r.code` for overfull/underfull bars.
   - Achieved 10/10 passing tests in the integration suite.

---

## 3. Verification & Compliance

### Automated Integration Tests
Ran the suite successfully, achieving 10/10 passed:
```bash
python -m pytest tests/integration/domain_contracts/
```

### Safety & Invariants
- Perfect private git safety: `git ls-files fixtures/private work` outputs strictly `fixtures/private/.gitkeep`.
- Verification commands run successfully.
