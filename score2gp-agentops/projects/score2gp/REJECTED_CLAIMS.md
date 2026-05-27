# ScoreToGP Rejected Claims

This file records claims that agents must not make without evidence.

## Rejected Claim: Handoff Quality Proves Conversion Quality

Reason: a good prompt, summary, or handoff can improve coordination but does not prove ScoreToGP converted a score correctly.

Required replacement: cite benchmark evidence and report strict mode, remediation mode, semantic comparison, and generated-file existence separately.

## Rejected Claim: Diagnostic Tables Are Truth

Reason: diagnostic tables are evidence, not truth. They may reflect incomplete extraction, wrong assumptions, or summarized failures.

Required replacement: compare tables against source artifacts, visual evidence, generated files, and validation logs.

## Rejected Claim: Generated File Exists Therefore Conversion Passed

Reason: output existence only proves generation occurred.

Required replacement: report generated-file existence separately from semantic comparison and mode results.

## Rejected Claim: Remediation Success Equals Strict Success

Reason: remediation can recover or mask a failure. Strict mode and remediation mode answer different questions.

Required replacement: report both modes separately.

## Rejected Claim: Stress Case Failure Blocks Foundational Work

Reason: the Derek Trucks case is a stress/research case. It should inform research, not replace earlier acceptance gates.

Required replacement: classify the failure and return to the active benchmark rung.

## Rejected Claim: Private Benchmark Artifacts Can Be Committed For Convenience

Reason: private assets remain private and must never be committed.

Required replacement: refer to private benchmark names and keep files outside version control.

## Rejected Claim: Agent-Ops Scaffold Is A Product Improvement

Reason: this scaffold changes governance only.

Required replacement: describe it as agent-ops scaffolding only, not a ScoreToGP conversion improvement.
