# ScoreToGP Benchmark Ladder

The benchmark ladder controls the order in which ScoreToGP work should be evaluated. It starts with simple controlled GP-originated PDFs and only later moves to noisy real-world scores.

Stress cases must not be used as the first acceptance target. They are valuable for research and failure discovery, but they are poor first gates for correctness.

## Ladder

### 1. Public Tiny Synthetic Fixture

Purpose: establish a public, deterministic smoke test that can be committed and run in CI.

Expected properties:

- Tiny scope.
- Public and safe to commit.
- Clear expected IR.
- Fast validation.
- No private source material.

Use for:

- Schema compatibility.
- CLI smoke tests.
- Regression checks for basic pipeline behavior.

Do not use for:

- Claims about real-world score conversion quality.

### 2. Private Minimal GP-Originated One-Page Score

Purpose: test the smallest private Guitar Pro-originated PDF that exercises real product conversion behavior while staying controlled.

Expected properties:

- One page.
- GP-originated source.
- Minimal notation complexity.
- Private asset kept outside version control.

Use for:

- First meaningful private conversion target.
- Comparing extracted structure against a known source.
- Separating strict mode from remediation mode.

### 3. Major Triads Lesson 3 Private Benchmark

Purpose: evaluate a realistic but still bounded private lesson score.

Expected properties:

- Private benchmark.
- Musically structured lesson content.
- Known source evidence available to the maintainer.
- Suitable for visual/source comparison.

Use for:

- Checking repeated patterns.
- Checking lesson-oriented notation.
- Measuring semantic comparison against private source evidence.

### 4. Ross Campbell Lead Melodies Private Benchmark

Purpose: evaluate a more musically varied private benchmark with lead-line behavior.

Expected properties:

- Private benchmark.
- Lead melody content.
- Greater phrase and notation variation than earlier rungs.
- Human-maintainer evidence review required.

Use for:

- Testing melody extraction and export behavior.
- Finding semantic drift that simple exercises miss.
- Confirming improvements generalize beyond one lesson style.

### 5. Derek Trucks Stress/Research Case

Purpose: expose difficult real-world behavior and guide research, not serve as an initial acceptance gate.

Expected properties:

- Stress/research case.
- Noisy or complex source characteristics.
- High failure likelihood.
- Evidence useful for diagnosis.

Use for:

- Research questions.
- Failure taxonomy.
- Long-range roadmap pressure testing.

Do not use for:

- First acceptance target.
- Broad conversion-quality claims.
- Blocking foundational benchmark progress.

## Advancement Rule

Advance to the next rung only when the current rung has clear evidence for strict mode, remediation mode, semantic comparison, and generated-file existence. Advancement is a maintainer decision, not an agent assertion.
