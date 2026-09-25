# Score2GP Requirements Register

A requirement records **what must be true** of the product, why, and how it will be
accepted. It sits before architecture decisions and tasks in the lifecycle. It is a
contract for the development effort: every task, ADR and acceptance claim that
delivers a requirement cites its ID, and a requirement is closed only by evidence
against its acceptance criteria.

## Lifecycle

| Status | Meaning | Exit evidence |
|---|---|---|
| `PROPOSED` | Stated by the maintainer and recorded; not yet researched in full | Record merged |
| `RESEARCHED` | Features, impact, risks and open questions investigated with sources | Research sections complete; open questions listed |
| `ACCEPTED` | Maintainer has answered the open questions and accepted scope and acceptance criteria | Maintainer decision recorded in the record |
| `PLANNED` | Backlog tasks exist in the task authority (`ORCHESTRATION_STATE.json`) with dependencies | Task IDs listed in the record |
| `IN_DELIVERY` | At least one task promoted | Task and PR links |
| `VERIFIED` | Every acceptance criterion met by independently reviewed evidence | Evidence links per criterion |
| `SUPERSEDED` / `WITHDRAWN` | Replaced or dropped by maintainer decision | Link to the decision |

Priority is recorded separately from status. A requirement can be `ACCEPTED` and
still wait for priority.

## Relationship to other records

- **How** a requirement is met is decided in an ADR (`ARCHITECTURE_DECISIONS.md`).
- **What to do next** is the task authority (`ORCHESTRATION_STATE.json`). Tasks cite
  the requirement ID they deliver.
- **Detailed programme plans** (`plans/`) may elaborate a requirement; the register
  entry points to them rather than duplicating them.

## Register

| ID | Title | Status | Priority | Record |
|---|---|---|---|---|
| REQ-0001 | Native, faithful PDF → Guitar Pro conversion (obligations U01–U14) | `IN_DELIVERY` | Current programme | [REQ-0001](REQ-0001-native-faithful-pdf-to-gp.md) |
| REQ-0002 | Pluggable, version-selectable Guitar Pro output (GP8/GP7 first; GP5/GP6 and future versions bolt-on) | `RESEARCHED` | Unprioritised; containment task recommended early | [REQ-0002](REQ-0002-pluggable-gp-output-targets.md) |
| REQ-0003 | Dependency licences compatible with a proprietary product | `PROPOSED` | Unprioritised; before release | [REQ-0003](REQ-0003-dependency-licence-compatibility.md) |
