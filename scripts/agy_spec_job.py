#!/usr/bin/env python3
"""Validate and resolve a multi-ticket implementation job for Orca.

The job manifest is planning input.  It describes a specification and its
ticket graph; it does not authorise a worker, a PR, or a merge.  Orca must
promote each frontier ticket into ORCHESTRATION_STATE.json before dispatch.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


class SpecJobError(ValueError):
    """Raised when a spec-job manifest is not executable as a graph."""


TERMINAL_STATUSES = {"COMPLETE", "COMPLETED", "MERGED", "DONE"}
ACTIVE_STATUSES = {"READY", "IN_PROGRESS", "IMPLEMENTING", "BLOCKED", "COMPLETE", "COMPLETED", "MERGED", "DONE"}


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise SpecJobError(f"job manifest does not exist: {path}") from error
    if not isinstance(value, dict):
        raise SpecJobError("job manifest must contain a mapping")
    validate_manifest(value)
    return value


def _required(mapping: dict[str, Any], key: str, context: str) -> Any:
    value = mapping.get(key)
    if value is None or value == "":
        raise SpecJobError(f"{context} requires {key}")
    return value


def _as_strings(value: Any, context: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise SpecJobError(f"{context} must be a list of non-empty strings")
    return list(value)


def validate_manifest(manifest: dict[str, Any]) -> None:
    if manifest.get("schema_version") != 1:
        raise SpecJobError("job manifest schema_version must be 1")
    job = _required(manifest, "job", "manifest")
    if not isinstance(job, dict):
        raise SpecJobError("manifest job must be a mapping")
    for key in ("id", "title", "spec", "repository", "base_branch", "integration_branch"):
        _required(job, key, "job")
    tickets = _required(manifest, "tickets", "manifest")
    if not isinstance(tickets, list) or not tickets:
        raise SpecJobError("manifest tickets must be a non-empty list")

    ids: set[str] = set()
    repository = str(job["repository"])
    base_branch = str(job["base_branch"])
    for index, ticket in enumerate(tickets):
        context = f"ticket[{index}]"
        if not isinstance(ticket, dict):
            raise SpecJobError(f"{context} must be a mapping")
        ticket_id = str(_required(ticket, "id", context))
        if ticket_id in ids:
            raise SpecJobError(f"duplicate ticket id: {ticket_id}")
        ids.add(ticket_id)
        for key in ("title", "objective", "status", "blocked_by", "allowed_paths", "acceptance", "validation"):
            _required(ticket, key, context)
        status = str(ticket["status"]).upper()
        if status not in ACTIVE_STATUSES:
            raise SpecJobError(f"{context} has unsupported status: {ticket['status']}")
        _as_strings(ticket["blocked_by"], f"{context}.blocked_by")
        _as_strings(ticket["allowed_paths"], f"{context}.allowed_paths")
        _as_strings(ticket["acceptance"], f"{context}.acceptance")
        _as_strings(ticket["validation"], f"{context}.validation")
        if ticket.get("repository", repository) != repository:
            raise SpecJobError(f"{context}.repository must match job.repository")
        if ticket.get("base_branch", base_branch) != base_branch:
            raise SpecJobError(f"{context}.base_branch must match job.base_branch")
        if ticket.get("cardinality", 1) != 1:
            raise SpecJobError(f"{context}.cardinality must be 1")

    for ticket in tickets:
        for blocker in ticket["blocked_by"]:
            if blocker not in ids:
                raise SpecJobError(f"ticket {ticket['id']} references unknown blocker {blocker}")
    _assert_acyclic(tickets)


def _assert_acyclic(tickets: list[dict[str, Any]]) -> None:
    graph = {str(ticket["id"]): list(ticket["blocked_by"]) for ticket in tickets}
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(ticket_id: str) -> None:
        if ticket_id in visiting:
            raise SpecJobError(f"ticket dependency cycle includes {ticket_id}")
        if ticket_id in visited:
            return
        visiting.add(ticket_id)
        for blocker in graph[ticket_id]:
            visit(blocker)
        visiting.remove(ticket_id)
        visited.add(ticket_id)

    for ticket_id in graph:
        visit(ticket_id)


def frontier(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    validate_manifest(manifest)
    statuses = {str(ticket["id"]): str(ticket["status"]).upper() for ticket in manifest["tickets"]}
    ready = []
    for ticket in manifest["tickets"]:
        if str(ticket["status"]).upper() != "READY":
            continue
        if all(statuses[blocker] in TERMINAL_STATUSES for blocker in ticket["blocked_by"]):
            ready.append(ticket)
    return sorted(ready, key=lambda ticket: str(ticket["id"]))


def resolved_job(manifest: dict[str, Any]) -> dict[str, Any]:
    validate_manifest(manifest)
    tickets = {str(ticket["id"]): ticket for ticket in manifest["tickets"]}
    return {
        "schema_version": 1,
        "job": manifest["job"],
        "frontier": frontier(manifest),
        "blocked": [
            {"id": ticket_id, "blocked_by": ticket["blocked_by"]}
            for ticket_id, ticket in sorted(tickets.items())
            if str(ticket["status"]).upper() == "READY"
            and any(str(tickets[blocker]["status"]).upper() not in TERMINAL_STATUSES for blocker in ticket["blocked_by"])
        ],
        "remaining": [
            ticket_id
            for ticket_id, ticket in sorted(tickets.items())
            if str(ticket["status"]).upper() not in TERMINAL_STATUSES
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate and resolve an Orca spec-job manifest")
    parser.add_argument("job", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        manifest = load_manifest(args.job)
    except SpecJobError as error:
        parser.error(str(error))
    output = resolved_job(manifest)
    if args.json:
        print(json.dumps(output, indent=2, sort_keys=True))
    else:
        print(f"VALID: {output['job']['id']}")
        frontier_ids = ", ".join(ticket["id"] for ticket in output["frontier"])
        print("frontier: " + frontier_ids if frontier_ids else "frontier: empty")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
