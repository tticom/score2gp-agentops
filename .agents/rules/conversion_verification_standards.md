# Rule: Score Conversion Verification Standards

1. **Rejection of Synthetic Unit Test Signals**: Never treat unit test pass rates (e.g. 100% pytest pass rate) as proof of score conversion fidelity when tests use synthetic JSON mocks or assert on refusal codes.
2. **Ground-Truth Semantic Diffing**: All conversion fidelity claims MUST be empirically validated against real ground-truth score files (`.gp`) using semantic bar-level pitch, duration, tempo, track, and fingering comparators.
3. **Private Fixture Boundaries**: Held-out private score fixtures must serve as behavioral acceptance oracles, never as source inputs for hardcoded constants, hashes, coordinates, or fixture-specific logic.
