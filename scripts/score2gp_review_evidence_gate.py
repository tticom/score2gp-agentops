#!/usr/bin/env python3
"""Validate strike-adjusted reviewer-created evidence before approval."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


class ReviewEvidenceError(ValueError):
    pass


ATTESTATION = (
    "I personally ran every listed probe against the pinned review head "
    "and recorded observed output without inference."
)


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ReviewEvidenceError(f"{field} must be non-empty text")
    return value.strip()


def active_strikes(scorecard: dict[str, Any], reviewer: str) -> int:
    reviewer_entry = (scorecard.get("reviewers") or {}).get(reviewer) or {}
    strikes = reviewer_entry.get("active_strikes", 0)
    if not isinstance(strikes, int) or strikes < 0:
        raise ReviewEvidenceError(f"invalid active_strikes for {reviewer}")
    return strikes


def validate_approval_packet(
    packet: dict[str, Any], *, expected_head: str, strikes: int, high_risk: bool
) -> tuple[int, int]:
    if packet.get("verdict") != "APPROVE":
        raise ReviewEvidenceError("packet verdict must be APPROVE")
    if not re.fullmatch(r"[0-9a-f]{40}", expected_head):
        raise ReviewEvidenceError("expected_head must be a full commit SHA")
    if packet.get("review_head") != expected_head:
        raise ReviewEvidenceError("review_head does not match the pinned PR head")
    _text(packet.get("baseline_failure_expectation"), "baseline_failure_expectation")
    claims = packet.get("claims")
    if not isinstance(claims, list) or not claims:
        raise ReviewEvidenceError("claims must be a non-empty list")
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            raise ReviewEvidenceError(f"claims[{index}] must be an object")
        for field in (
            "claim",
            "production_path",
            "evidence_path",
            "false_success_mutation",
            "failure_oracle",
            "disproof_attempt",
        ):
            _text(claim.get(field), f"claims[{index}].{field}")
        probe_names = claim.get("probe_names")
        if not isinstance(probe_names, list) or not probe_names:
            raise ReviewEvidenceError(
                f"claims[{index}].probe_names must identify executed probes"
            )
        for probe_name in probe_names:
            _text(probe_name, f"claims[{index}].probe_names")
        if claim.get("status") != "verified":
            raise ReviewEvidenceError(f"claims[{index}].status must be verified")

    probes = packet.get("probes")
    if not isinstance(probes, list):
        raise ReviewEvidenceError("probes must be a list")
    required = (3 if high_risk else 2) + min(strikes, 2)
    if len(probes) < required:
        raise ReviewEvidenceError(
            f"need at least {required} reviewer-created probes; found {len(probes)}"
        )
    commands: set[str] = set()
    mutations: set[str] = set()
    probe_names: set[str] = set()
    probe_types: set[str] = set()
    production_count = 0
    for index, probe in enumerate(probes):
        if not isinstance(probe, dict):
            raise ReviewEvidenceError(f"probes[{index}] must be an object")
        if probe.get("reviewer_created") is not True:
            raise ReviewEvidenceError(f"probes[{index}] is not reviewer-created")
        if probe.get("author_test_only") is not False:
            raise ReviewEvidenceError(f"probes[{index}] is author-test-only")
        if probe.get("result") not in {"killed", "exposed"}:
            raise ReviewEvidenceError(f"probes[{index}] did not kill or expose a mutation")
        if probe.get("head_sha") != expected_head:
            raise ReviewEvidenceError(f"probes[{index}].head_sha is not the pinned head")
        if probe.get("exit_code") not in range(0, 256):
            raise ReviewEvidenceError(f"probes[{index}].exit_code must be recorded")
        probe_type = probe.get("probe_type")
        if probe_type not in {"mutation", "boundary", "artifact"}:
            raise ReviewEvidenceError(
                f"probes[{index}].probe_type must be mutation, boundary, or artifact"
            )
        digest = _text(probe.get("output_sha256"), f"probes[{index}].output_sha256")
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ReviewEvidenceError(
                f"probes[{index}].output_sha256 must be a lowercase SHA-256"
            )
        for field in (
            "name",
            "command",
            "input",
            "false_success_mutation",
            "observed_output",
            "invariant",
        ):
            _text(probe.get(field), f"probes[{index}].{field}")
        command = probe["command"].strip()
        mutation = probe["false_success_mutation"].strip()
        name = probe["name"].strip()
        if command in commands or mutation in mutations:
            raise ReviewEvidenceError("probe commands and mutations must be unique")
        if name in probe_names:
            raise ReviewEvidenceError("probe names must be unique")
        commands.add(command)
        mutations.add(mutation)
        probe_names.add(name)
        probe_types.add(probe_type)
        production_count += probe.get("production_path") is True

    for index, claim in enumerate(claims):
        missing = set(claim["probe_names"]) - probe_names
        if missing:
            raise ReviewEvidenceError(
                f"claims[{index}] references unknown probes: {sorted(missing)}"
            )

    required_types = {"mutation", "artifact"}
    if not required_types.issubset(probe_types):
        raise ReviewEvidenceError(
            "approval requires both mutation and final-artifact probes"
        )

    required_production = 2 if high_risk else 1
    if production_count < required_production:
        raise ReviewEvidenceError(
            f"need {required_production} production-path probes; found {production_count}"
        )
    risks = packet.get("residual_risks")
    if not isinstance(risks, list) or not risks:
        raise ReviewEvidenceError("residual_risks must be a non-empty list")
    banned = {"none", "no risk", "no risks", "zero", "n/a"}
    if any(_text(risk, "residual_risk").lower().rstrip(".") in banned for risk in risks):
        raise ReviewEvidenceError("zero-risk claims are forbidden")
    if packet.get("integrity_attestation") != ATTESTATION:
        raise ReviewEvidenceError("integrity_attestation is missing or not exact")
    return required, len(probes) * 2


def read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ReviewEvidenceError(f"cannot read JSON evidence: {error}") from error
    if not isinstance(payload, dict):
        raise ReviewEvidenceError("JSON root must be an object")
    return payload
