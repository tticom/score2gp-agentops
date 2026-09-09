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
    (tmp_path / ".agy" / "prompts" / "implement.md").write_text(
        "{{CYCLE_ID}} {{TASK_ID}} {{TASK_TITLE}}\n{{ACCEPTANCE}}\n{{VALIDATION}}\n", encoding="utf-8"
    )
    record = agy_cycle.claim(root, "T-001", "test")
    text = agy_cycle.prompt(root, record["cycle_id"])
    assert record["cycle_id"] in text
    assert "T-001" in text
    assert "first" in text


def test_real_repo_flow_and_backlog_are_valid() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    flow, backlog, cycles = agy_cycle.load_config(repo_root)
    assert "states" in flow
    assert "tasks" in backlog
    # Ensure every command in flow maps to agy-cycle subcommands
    subcommands = {
        "claim", "next", "status", "prompt", "run", "implement",
        "transition", "reset", "repair", "attach-pr", "update-pr-head",
        "validate", "verify", "verify-pr", "verify-head", "open-pr",
        "review", "review-fix", "merge-check", "reconcile", "complete"
    }
    for state, defn in flow.get("states", {}).items():
        cmd = defn.get("command")
        if cmd != "none":
            assert cmd in subcommands, f"State '{state}' has unmapped command '{cmd}'"


def test_duplicate_key_in_yaml_raises_cycle_error(tmp_path: Path) -> None:
    yaml_file = tmp_path / "test.yaml"
    yaml_file.write_text(
        """
states:
  MERGE_READY:
    command: reconcile
  MERGE_READY:
    command: complete
""",
        encoding="utf-8",
    )
    with pytest.raises(agy_cycle.CycleError, match="duplicate key 'MERGE_READY'"):
        agy_cycle.read_yaml(yaml_file)


def test_unmet_dependencies_cannot_be_claimed(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    (root / "plan" / "backlog.yaml").write_text(
        """
tasks:
  - id: T-001
    title: first
    status: READY
    ordinality: 1
    cardinality: 1
    depends_on: []
  - id: T-002
    title: second
    status: READY
    ordinality: 2
    cardinality: 1
    depends_on: [T-001]
""",
        encoding="utf-8",
    )
    with pytest.raises(agy_cycle.CycleError, match="unmet dependencies"):
        agy_cycle.claim(root, "T-002", "worker")


def test_resource_group_mutual_exclusion(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    (root / "plan" / "backlog.yaml").write_text(
        """
tasks:
  - id: T-001
    title: first
    status: READY
    ordinality: 1
    cardinality: 1
    resource_group: database
    depends_on: []
  - id: T-002
    title: second
    status: READY
    ordinality: 2
    cardinality: 1
    resource_group: database
    depends_on: []
""",
        encoding="utf-8",
    )
    rec1 = agy_cycle.claim(root, "T-001", "worker-1")
    assert rec1["state"] == "CLAIMED"
    with pytest.raises(agy_cycle.CycleError, match="resource group 'database' is currently locked"):
        agy_cycle.claim(root, "T-002", "worker-2")

    # Resetting rec1 releases the resource_group lock
    agy_cycle.reset(root, rec1["cycle_id"], "READY", "worker-1")
    rec2 = agy_cycle.claim(root, "T-002", "worker-2")
    assert rec2["state"] == "CLAIMED"


def test_self_review_is_strictly_forbidden(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    (root / ".agy" / "flow.yaml").write_text(
        Path(__file__).resolve().parent.parent.joinpath(".agy", "flow.yaml").read_text(encoding="utf-8")
    )
    rec = agy_cycle.claim(root, "T-001", "author-1")
    cid = rec["cycle_id"]
    agy_cycle.transition(root, cid, "IMPLEMENTING", "author-1")
    agy_cycle.transition(root, cid, "VALIDATING", "author-1")
    agy_cycle.attach_pr(root, cid, "https://github.com/org/repo/pull/1", "author-1")
    agy_cycle.transition(root, cid, "REVIEW_REQUIRED", "author-1")

    # Author attempting self-review must fail
    with pytest.raises(agy_cycle.CycleError, match="self-review is forbidden"):
        agy_cycle.review(root, cid, "APPROVED", "author-1")

    # Independent reviewer succeeds
    res = agy_cycle.review(root, cid, "APPROVED", "reviewer-2")
    assert res["state"] == "APPROVED"


def test_multi_round_review_fix_lifecycle(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import json
    import unittest.mock as mock

    root = make_root(tmp_path)
    (root / ".agy" / "flow.yaml").write_text(
        Path(__file__).resolve().parent.parent.joinpath(".agy", "flow.yaml").read_text(encoding="utf-8")
    )
    rec = agy_cycle.claim(root, "T-001", "worker")
    cid = rec["cycle_id"]

    # Round 1: Implementation -> Validation -> PR Open
    agy_cycle.transition(root, cid, "IMPLEMENTING", "worker")
    agy_cycle.transition(root, cid, "VALIDATING", "worker")
    head1 = "1111111111111111111111111111111111111111"
    agy_cycle.attach_pr(root, cid, "https://github.com/org/repo/pull/1", "worker", head_sha=head1)
    agy_cycle.transition(root, cid, "REVIEW_REQUIRED", "worker")

    # Reviewer requests changes
    agy_cycle.review(root, cid, "CHANGES_REQUESTED", "reviewer")
    status = agy_cycle.load_cycle(root / ".agy" / "cycles", cid)[1]
    assert status["state"] == "CHANGES_REQUESTED"

    # Author addresses feedback and transitions back to VALIDATING
    agy_cycle.transition(root, cid, "IMPLEMENTING", "worker")
    agy_cycle.transition(root, cid, "VALIDATING", "worker")

    # Author can transition back to PR_OPEN without deadlock
    agy_cycle.transition(root, cid, "PR_OPEN", "worker")

    # Remote PR advances with review-fix commit
    head2 = "2222222222222222222222222222222222222222"
    live_pr = {
        "number": 1,
        "url": "https://github.com/org/repo/pull/1",
        "state": "OPEN",
        "mergedAt": None,
        "headRefOid": head2,
    }
    with mock.patch("subprocess.run") as m_run:
        m_run.return_value = mock.Mock(returncode=0, stdout=json.dumps(live_pr), stderr="")
        updated = agy_cycle.update_pr_head(root, cid, head2, "worker")
        assert updated["pr_head_sha"] == head2

    # Transition to REVIEW_REQUIRED for second review
    agy_cycle.transition(root, cid, "REVIEW_REQUIRED", "worker")
    agy_cycle.review(root, cid, "APPROVED", "reviewer")

    # Merge check
    with mock.patch("subprocess.run") as m_run:
        m_run.return_value = mock.Mock(returncode=0, stdout=json.dumps(live_pr), stderr="")
        agy_cycle.merge_check(root, cid, "worker")
    status = agy_cycle.load_cycle(root / ".agy" / "cycles", cid)[1]
    assert status["state"] == "MERGE_READY"

    # Merge on remote and reconcile (first call transitions to MERGED)
    live_pr["mergedAt"] = "2026-09-09T21:00:00Z"
    with mock.patch("subprocess.run") as m_run:
        m_run.return_value = mock.Mock(returncode=0, stdout=json.dumps(live_pr), stderr="")
        rec1 = agy_cycle.reconcile(root, cid, "worker")
        assert rec1["state"] == "MERGED"

        # Second call transitions to RECONCILED (idempotent state progression)
        rec2 = agy_cycle.reconcile(root, cid, "worker")
        assert rec2["state"] == "RECONCILED"

        # Third call remains RECONCILED
        rec3 = agy_cycle.reconcile(root, cid, "worker")
        assert rec3["state"] == "RECONCILED"

    # Complete cycle and release task lock
    completed = agy_cycle.complete_cycle(root, cid, "worker")
    assert completed["state"] == "COMPLETE"
    assert not (root / ".agy" / "cycles" / "T-001.claim").exists()
