# PDF-Tab Duration-Evidence Audit Promotion

## Verified predecessor

- AgentOps PR #383 merged at
  `b3918e19d9130b52bcfacfe53133f5794efbad82`.
- The permanent `go` and `got` dispatchers are present on `origin/main`.
- Product main remains at
  `d70d559152c5aa357a7d2eb38e65b09f288bb08f`.
- CR-04D is complete and the post-refactor public replay is merged.

## Selection evidence

The replay identifies fixed spatial eighth-note timing as the first current
PDF-only tab limitation. The product contains public flag/beam diagnostic
tests and many generated PDFs, but current durable evidence does not show that
one fixture simultaneously provides:

- multi-bar tablature;
- visible varied duration marks;
- an independent expected-duration oracle; and
- a production seam carrying those marks into PDF-only tab events.

Promoting implementation now would risk treating standard-staff diagnostics
or green structural tests as proof of PDF-tab readiness.

## Authorisation

Prompt 0018 authorises a read-only product adequacy audit and one AgentOps
report. It authorises no product edit, new fixture, private input,
implementation prompt, automatic promotion, approval, or merge.

The audit must return exactly one of `IMPLEMENTATION_READY`,
`PUBLIC_FIXTURE_GAP`, `ARCHITECTURE_GAP`, or `BLOCKED`. This makes the next
decision measurable and prevents another open-ended diagnostic loop.

## Skills

The task uses workflow skills locked at
`0d6d84879eff0d352b444fdeceb3bb7a098e0c47`. Skills versioning remains
separate from Score2GP conversion work.
