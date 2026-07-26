# 0015 - CR-04D4 Consolidate PDF-Only Tab Test Fixtures (Wireframe)

## Status

INACTIVE WIREFRAME until CR-04D3 is merged, revalidated, and promoted.

## Intended Objective

Reduce duplicated TabRaw/JSON setup while retaining explicit behavioural
assertions and regression meaning.

## Boundary and Evidence

A duplication inventory must identify concrete builders and fixtures. Introduce
small test helpers only where scenario intent becomes clearer. Preserve distinct
tests for duration consistency, mixed-rest refusal, CLI refusal, chord grouping,
bar identity, and GP validation. Do not hide unrelated behaviours in an opaque
parameter matrix or change production code to simplify tests.

Prove no required scenario disappeared and each key test would fail for its
named regression; run targeted and full verification.

If consolidation obscures event sequences or weakens assertions, retain the
duplication as intentional. Publish one test-only PR and stop before CR-04D5.
