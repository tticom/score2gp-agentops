# Antigravity Task: Domain Knowledge and Stage Integration Test Foundation

## Context

This repository is `score2gp`, a project intended to convert guitar score PDFs into useful Guitar Pro-compatible output.

The last generated `smoke.gp` had a serious musical correctness problem: unrealistic pitch. That means “a file was written” is not a sufficient success criterion. The project needs stage-level integration tests that validate intermediate products against verified domain knowledge before downstream stages are trusted.

The repo now contains or is expected to contain a `docs/domain/` folder with initial domain knowledge files, including guitar notation, tablature semantics, timing/voices, PDF score extraction, MusicXML modelling, Guitar Pro output notes and validation rules.

This task begins a new research-and-test-foundation phase.

The purpose is not to make the current implementation pass. The purpose is to build verified domain knowledge and turn that knowledge into immutable stage integration tests that reveal where the pipeline becomes musically wrong.

## Goal

Create the foundation for a domain-driven integration test system.

The final result should include:

1. A safe baseline commit on a new research branch containing the current intended code/docs changes, if appropriate.
2. New or improved `docs/domain/` files containing verified domain knowledge only.
3. A clear distinction between:
   * verified domain knowledge,
   * project decisions,
   * assumptions requiring validation,
   * unknowns.
4. A first suite of stage integration tests derived from the verified domain knowledge.
5. Integration tests that validate intermediate products, not only final output existence.
6. A report showing which stage first fails against the domain tests.
7. No private/generated artifacts committed unless explicitly safe and intended.
