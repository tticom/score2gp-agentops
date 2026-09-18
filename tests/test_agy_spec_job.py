from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "agy_spec_job.py"
SPEC = importlib.util.spec_from_file_location("agy_spec_job", MODULE_PATH)
assert SPEC and SPEC.loader
agy_spec_job = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(agy_spec_job)


def manifest() -> dict:
    return {
        "schema_version": 1,
        "job": {
            "id": "JOB-001",
            "title": "Example implementation",
            "spec": "docs/specs/example.md",
            "repository": "tticom/example",
            "base_branch": "main",
            "integration_branch": "codex/job-001",
        },
        "tickets": [
            {
                "id": "T-001",
                "title": "Foundation",
                "objective": "Provide the first vertical slice.",
                "status": "COMPLETE",
                "blocked_by": [],
                "allowed_paths": ["src/**"],
                "acceptance": ["The slice works."],
                "validation": ["python -m pytest"],
            },
            {
                "id": "T-002",
                "title": "Follow-up",
                "objective": "Provide the second vertical slice.",
                "status": "READY",
                "blocked_by": ["T-001"],
                "allowed_paths": ["src/**"],
                "acceptance": ["The follow-up works."],
                "validation": ["python -m pytest"],
            },
        ],
    }


def test_frontier_contains_only_unblocked_ready_tickets() -> None:
    assert [ticket["id"] for ticket in agy_spec_job.frontier(manifest())] == ["T-002"]


def test_unknown_blocker_is_rejected() -> None:
    value = manifest()
    value["tickets"][1]["blocked_by"] = ["T-999"]
    with pytest.raises(agy_spec_job.SpecJobError, match="unknown blocker"):
        agy_spec_job.validate_manifest(value)


@pytest.mark.parametrize("field", ["allowed_paths", "acceptance", "validation"])
def test_required_contract_lists_must_not_be_empty(field: str) -> None:
    value = manifest()
    value["tickets"][0][field] = []
    with pytest.raises(agy_spec_job.SpecJobError, match="non-empty list"):
        agy_spec_job.validate_manifest(value)


@pytest.mark.parametrize("field", ["id", "title", "objective"])
def test_required_strings_must_not_be_whitespace(field: str) -> None:
    value = manifest()
    value["tickets"][0][field] = "   "
    with pytest.raises(agy_spec_job.SpecJobError):
        agy_spec_job.validate_manifest(value)


def test_dependency_cycle_is_rejected() -> None:
    value = manifest()
    value["tickets"][0]["status"] = "READY"
    value["tickets"][0]["blocked_by"] = ["T-002"]
    with pytest.raises(agy_spec_job.SpecJobError, match="dependency cycle"):
        agy_spec_job.validate_manifest(value)


def test_resolved_job_is_planning_output_not_authority() -> None:
    output = agy_spec_job.resolved_job(manifest())
    assert output["job"]["integration_branch"] == "codex/job-001"
    assert output["remaining"] == ["T-002"]
    assert output["frontier"][0]["id"] == "T-002"


def test_declared_blocked_ticket_is_reported() -> None:
    value = manifest()
    value["tickets"][1]["status"] = "BLOCKED"
    output = agy_spec_job.resolved_job(value)
    assert output["blocked"] == [{"id": "T-002", "blocked_by": ["T-001"]}]
