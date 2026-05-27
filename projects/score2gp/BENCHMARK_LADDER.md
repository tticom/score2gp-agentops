# ScoreToGP Benchmark Ladder

The benchmark ladder controls the execution order in which ScoreToGP changes should be validated. Work must proceed sequentially up the ladder.

> [!IMPORTANT]
> **Stress cases must not be used as the first acceptance target.**
> The Derek Trucks / BB King score is a noisy stress-research case, not an initial or primary acceptance benchmark. 
> The next serious private benchmark is **Major Triads Lesson 3**, which represents the expected minimum real-world capability of the compiler.

---

## The Staged Validation Principle

Every benchmark rung must be validated through separate, staged quality gates:
1. **Extraction**: Confirm candidates, barlines, and coordinates are cleanly parsed.
2. **Grouping**: Verify staff lines, bar boxes, and system bounding boxes are safely constructed.
3. **Strict Build-IR**: Confirm the compiler builds a ScoreIR successfully under strict mode (`allow_skip_unboxed=False`).
4. **Semantic Round-Trip**: Ensure recovered notes match the GP/MusicXML oracle and achieve high string/fret match rates.

---

## Rungs of the Ladder

### Rung 1: Public Tiny Synthetic Fixture
- **Purpose**: Establish a public, deterministic smoke test that can be committed and run in CI.
- **Scope**: Tiny, public, safe to commit, no private source material.
- **Use for**: Schema validation, CLI smoke tests, and basic pipeline regression checks.
- **Non-Goal**: Claims about real-world score conversion quality.

### Rung 2: Private Minimal GP-Originated One-Page Score
- **Purpose**: Test the smallest private Guitar Pro-originated PDF that exercises real product conversion behavior while staying controlled.
- **Scope**: One page, GP-originated source, minimal notation complexity. Private asset kept outside version control.
- **Use for**: Basic private conversion validation and separating strict mode from remediation mode.

### Rung 3: Major Triads Lesson 3 Private Benchmark
- **Purpose**: The primary active private benchmark for verifying clean, technique-free conversion.
- **Scope**: Multi-page, GP-originated triads runs, straight note runs, minimal expressive technique burden (no noisy bends or tremolo picking).
- **Use for**: expected minimum real-world capability checks, visual/source comparison, and re-establishing baseline correctness.

### Rung 4: Ross Campbell Lead Melodies Private Benchmark
- **Purpose**: Evaluate a more musically varied private benchmark with lead-line behavior.
- **Scope**: Lead melody content, greater phrase and notation variation.
- **Use for**: Testing melody extraction, finding semantic drift, and checking generalizability.

### Rung 5: Derek Trucks / BB King Stress-Research Case
- **Purpose**: Expose complex real-world behavior and guide research.
- **Scope**: Noisy or complex source characteristics, multi-track layouts, extreme lead/rhythm complexity, high failure likelihood.
- **Use for**: Research questions, failure taxonomy, and long-range roadmap pressure testing.
- **Do Not Use For**: First acceptance target or blocking foundational benchmark progress.
