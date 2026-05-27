# ScoreToGP Acceptance Targets

Acceptance targets define what must be true before a ScoreToGP change can be considered successful for a benchmark rung.

They are not claims of product progress. They are gates for evidence.

## Universal Reporting Fields

Every target must report these separately:

- Strict mode.
- Remediation mode.
- Semantic comparison.
- Generated-file existence.

These fields must not be collapsed into one status. Generated-file existence confirms that an output was produced; it does not confirm conversion correctness.

## Initial Acceptance Target

The first acceptance target is the public tiny synthetic fixture.

Required evidence:

- Public fixture validation completes.
- Expected generated files exist.
- Strict mode result is reported.
- Remediation mode result is reported, even if not used.
- Semantic comparison status is reported.
- No private files are added.

This target is intentionally small. It verifies the workflow and evidence structure before private or noisy benchmarks are used.

## Private Minimal GP-Originated One-Page Score

Required evidence:

- Private asset remains outside version control.
- Maintainer can inspect source evidence locally.
- Strict mode result is reported.
- Remediation mode result is reported.
- Semantic comparison against known source evidence is reported.
- Generated-file existence is reported.
- Visual/source evidence is preferred over generated summaries.

## Major Triads Lesson 3

Required evidence:

- Private benchmark remains private.
- Visual/source evidence is inspected by the maintainer or reviewer with local access.
- Repeated patterns and lesson structure are checked.
- Strict mode, remediation mode, semantic comparison, and generated-file existence are reported separately.

## Ross Campbell Lead Melodies

Required evidence:

- Private benchmark remains private.
- Lead melody semantics are compared against source evidence.
- Any drift is classified by likely product layer.
- Strict mode, remediation mode, semantic comparison, and generated-file existence are reported separately.

## Derek Trucks Stress/Research Case

Required evidence:

- Case is labeled stress/research.
- No first-acceptance claims are based on this case.
- Failures are used for diagnosis and roadmap shaping.
- Strict mode, remediation mode, semantic comparison, and generated-file existence are still reported separately.

## Acceptance Language

Allowed:

- "The public tiny fixture workflow produced the expected files and reported all required fields."
- "The private one-page benchmark needs remediation because semantic comparison failed."
- "The stress case exposed an extraction failure."

Rejected:

- "ScoreToGP conversion is fixed."
- "The benchmark passed because an output file exists."
- "The diagnostic table proves correctness."
- "The prompt was good, so the implementation succeeded."
