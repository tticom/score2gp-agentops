# REQ-0003 — Dependency licences compatible with a proprietary product

- **Status:** `PROPOSED`. Not prioritised.
- **Owner:** maintainer (`tticom`)
- **Recorded:** 2026-09-25

## Requirement

Every dependency shipped with, or run as part of, a released Score2GP product or
service must have a licence compatible with proprietary distribution and with
operation as a network service. Copyleft terms that would require publishing
Score2GP source, such as AGPL-3.0 for network use, are not acceptable in a
release unless a commercial licence has been obtained.

Maintainer direction (2026-09-25): licensing "as narrow as possible", suitable for
taking the repositories private. No new spend until the Lesson PDFs reliably
produce a usable GP file.

## Findings

| Dependency | Licence | Used for | Consequence |
|---|---|---|---|
| `pymupdf` 1.28.2 | Dual: AGPL-3.0 or Artifex commercial | PDF text, vector and raster acquisition (5 product modules import it) | Fine for private prototyping. A closed distribution or web service requires an Artifex licence (a cost) or migration to a permissively licensed PDF library |
| `pydantic`, `typer` | Permissive (not re-verified in this record) | Models, CLI | Verify in the audit task |
| PyGuitarPro (candidate, not a dependency) | LGPL-3.0-only | Possible GP5 writer | Avoid, or isolate, per REQ-0002 Q2 |
| alphaTab (candidate validator) | MPL-2.0 | Possible independent reader | Acceptable as a development-only validator; not shipped |

## Acceptance criteria

1. A dependency licence audit lists every runtime and build dependency with its licence, checked mechanically in CI, and fails on an unapproved licence.
2. Before any release, each copyleft dependency is either replaced or covered by a recorded commercial licence.
3. Replacing a PDF library must preserve acquisition fidelity. The same observations on the real corpus, via characterization tests, must be produced before the old library is removed.

## Sequencing

Not on the L3-NATIVE critical path. The replacement decision is best taken before the acquisition layer is consolidated (REC-03/REC-06 successors), so the recognition lanes depend on an acquisition interface rather than on `fitz` directly.
