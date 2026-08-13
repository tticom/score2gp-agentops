# Remediation 04 — Migrate Private Fixtures to Product Repository

Status: SKELETON

## Context
Private integration tests use `pytest.skip` when the private fixture is missing on the CI server. This creates a false sense of security where CI runs "green" without ever testing real PDF data. Because the project heavily relies on these private fixtures for real-world verification, they must be moved back into the `score2gp` product repository.

## Goal
Migrate the private test fixtures (such as `Lesson-5.pdf`, `Lesson-6.pdf`, etc.) from the separate `score2gp-private-fixtures` repository (or external storage) directly into the main `score2gp` repository. Update all test suites, CI configurations, and scripts to use these fixtures directly and remove all `pytest.skip` fallbacks that trigger when the fixture is missing.

## Acceptance
- Private fixtures are committed to the `score2gp` repository.
- `pytest.skip` logic is removed from all private integration tests.
- CI fails hard if the real-source fixtures are missing or if the tests fail.
- All integration tests execute successfully on the CI server using the committed real PDF data.
