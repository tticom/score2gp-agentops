from __future__ import annotations

import threading
from pathlib import Path

import pytest

from scripts import agy_cycle


def make_root(tmp_path: Path) -> Path:
    (tmp_path / ".agy").mkdir()
    (tmp_path / "plan").mkdir()
    (tmp_path / ".agy" / "flow.yaml").write_text(
        """
version: 1
states:
  READY: {command: claim, next: CLAIMED}
  CLAIMED: {command: implement, next: IMPLEMENTING}
  IMPLEMENTING: {command: verify, next: VERIFYING}
  VERIFYING: {command: open-pr, next: PR_OPEN, on_failure: FAILED}
  PR_OPEN: {command: check, next: CHECKING}
  CHECKING: {command: merge-check, next: MERGE_READY, on_failure: FAILED}
  MERGE_READY: {command: complete, next: COMPLETE}
  COMPLETE: {command: none}
  BLOCKED: {command: repair}
  FAILED: {command: repair}
limits: {max_prs_per_cycle: 1}
""",
        encoding="utf-8",
    )
    (tmp_path / "plan" / "backlog.yaml").write_text(
        """
tasks:
  - id: T-001
    title: first
    status: READY
    sprint: S-1
    ordinality: 1
    cardinality: 1
    priority: 1
    depends_on: []
  - id: T-002
    title: second
    status: READY
    sprint: S-1
    ordinality: 2
    cardinality: 1
    priority: 1
    depends_on: []
""",
        encoding="utf-8",
    )
    return tmp_path


def test_claim_is_atomic_for_concurrent_instances(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    results: list[dict] = []
    errors: list[str] = []

    def run(owner: str) -> None:
        try:
            results.append(agy_cycle.claim(root, "T-001", owner))
        except agy_cycle.CycleError as exc:
            errors.append(str(exc))

    threads = [threading.Thread(target=run, args=(f"worker-{index}",)) for index in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert len(results) == 1
    assert len(errors) == 1
    assert "already claimed" in errors[0]


def test_next_is_derived_from_flow_and_transition_is_bounded(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    record = agy_cycle.claim(root, "T-001", "test")
    assert agy_cycle.next_action(root, record["cycle_id"])["command"] == "implement"
    agy_cycle.transition(root, record["cycle_id"], "IMPLEMENTING", "test")
    assert agy_cycle.next_action(root, record["cycle_id"])["command"] == "verify"
    with pytest.raises(agy_cycle.CycleError, match="invalid transition"):
        agy_cycle.transition(root, record["cycle_id"], "COMPLETE", "test")


def test_manual_reset_is_available_without_ai_state_reconstruction(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    record = agy_cycle.claim(root, "T-001", "test")
    reset = agy_cycle.reset(root, record["cycle_id"], "READY", "human")
    assert reset["state"] == "READY"
    assert reset["history"][-1]["manual"] is True
    assert not (root / ".agy" / "cycles" / f"{record['cycle_id']}.json").exists()


def test_one_pr_limit_is_enforced(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    record = agy_cycle.claim(root, "T-001", "test")
    agy_cycle.transition(root, record["cycle_id"], "IMPLEMENTING", "test")
    agy_cycle.transition(root, record["cycle_id"], "VERIFYING", "test")
    agy_cycle.transition(root, record["cycle_id"], "PR_OPEN", "test")
    agy_cycle.attach_pr(root, record["cycle_id"], "https://example.test/pr/1", "test")
    with pytest.raises(agy_cycle.CycleError, match="one permitted PR"):
        agy_cycle.attach_pr(root, record["cycle_id"], "https://example.test/pr/2", "test")


def test_prompt_is_bounded_by_the_task_record(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    (root / ".agy" / "prompts").mkdir()
    (root / ".agy" / "prompts" / "implement.md").write_text(
        "{{CYCLE_ID}} {{TASK_ID}} {{TASK_TITLE}}\n{{ACCEPTANCE}}\n{{VALIDATION}}\n", encoding="utf-8"
    )
    record = agy_cycle.claim(root, "T-001", "test")
    text = agy_cycle.prompt(root, record["cycle_id"])
    assert record["cycle_id"] in text
    assert "T-001" in text
    assert "first" in text
