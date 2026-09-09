#!/usr/bin/env python3
"""Small deterministic controller for one-task AGY implementation cycles.

This module owns lifecycle mechanics only. It never asks an AI to select a
task, infer state, or promote work. AGY is an interactive worker invoked by a
separate adapter after ``next`` returns the bounded command.
"""

from __future__ import annotations

import argparse
import json
import os
import pty
import select
import shlex
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]


TERMINAL = {"COMPLETE", "CANCELLED"}


class CycleError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise CycleError("agy-cycle requires PyYAML; install it in the controller environment")
    try:
        class DuplicateCheckingLoader(yaml.SafeLoader):
            pass

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[str, Any]:
            mapping: dict[str, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                if key in mapping:
                    raise CycleError(f"duplicate key '{key}' found in {path}")
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        DuplicateCheckingLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping
        )
        value = yaml.load(path.read_text(encoding="utf-8"), Loader=DuplicateCheckingLoader)
    except CycleError:
        raise
    except (OSError, yaml.YAMLError) as exc:
        raise CycleError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CycleError(f"{path} must contain a mapping")
    return value


def write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def paths(root: Path) -> tuple[Path, Path, Path]:
    return root / ".agy" / "flow.yaml", root / "plan" / "backlog.yaml", root / ".agy" / "cycles"


def load_config(root: Path) -> tuple[dict[str, Any], dict[str, Any], Path]:
    flow_path, backlog_path, cycles = paths(root)
    flow = read_yaml(flow_path)
    backlog = read_yaml(backlog_path)
    validate_flow(flow)
    validate_backlog(backlog)
    return flow, backlog, cycles


def validate_flow(flow: dict[str, Any]) -> None:
    states = flow.get("states")
    if not isinstance(states, dict) or not states:
        raise CycleError("flow.yaml must define states")
    limits = flow.get("limits", {})
    if limits.get("max_prs_per_cycle", 1) != 1:
        raise CycleError("max_prs_per_cycle must be exactly 1")
    for state, definition in states.items():
        if not isinstance(definition, dict) or "command" not in definition:
            raise CycleError(f"state {state} must define command")
        targets = definition.get("next")
        if targets is None:
            targets = []
        elif isinstance(targets, str):
            targets = [targets]
        if not isinstance(targets, list) or any(target not in states for target in targets):
            raise CycleError(f"state {state} points to unknown state")


def validate_backlog(backlog: dict[str, Any]) -> None:
    tasks = backlog.get("tasks")
    if not isinstance(tasks, list):
        raise CycleError("backlog.yaml must define a tasks list")
    ids: set[str] = set()
    for task in tasks:
        if not isinstance(task, dict):
            raise CycleError("every backlog task must be a mapping")
        required = {"id", "title", "status", "ordinality", "cardinality", "depends_on"}
        missing = required - task.keys()
        if missing:
            raise CycleError(f"task is missing: {', '.join(sorted(missing))}")
        task_id = str(task["id"])
        if task_id in ids:
            raise CycleError(f"duplicate task id: {task_id}")
        ids.add(task_id)
        if int(task["cardinality"]) != 1:
            raise CycleError(f"task {task_id} must fit one cycle (cardinality: 1)")
    for task in tasks:
        for dependency in task["depends_on"]:
            if dependency not in ids:
                raise CycleError(f"task {task['id']} depends on unknown task {dependency}")


def task_map(backlog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(task["id"]): task for task in backlog["tasks"]}


def completed_task_ids(cycles: Path) -> set[str]:
    result: set[str] = set()
    if not cycles.exists():
        return result
    for path in cycles.glob("*.json"):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if value.get("state") == "COMPLETE":
            result.add(str(value.get("task_id")))
    return result


def eligible_tasks(backlog: dict[str, Any], cycles: Path) -> list[dict[str, Any]]:
    tasks = task_map(backlog)
    completed = completed_task_ids(cycles)
    active = {
        str(json.loads(path.read_text(encoding="utf-8")).get("task_id"))
        for path in cycles.glob("*.json")
        if path.is_file()
    } if cycles.exists() else set()
    result = []
    for task in backlog["tasks"]:
        if task["status"] != "READY" or task["id"] in active or task["id"] in completed:
            continue
        if dependencies_satisfied(task, tasks, completed):
            result.append(task)
    return sorted(result, key=lambda item: (str(item.get("sprint", "")), int(item["ordinality"]), -int(item.get("priority", 0))))


def dependencies_satisfied(task: dict[str, Any], tasks: dict[str, dict[str, Any]], completed: set[str]) -> bool:
    return all(dependency in completed or tasks[dependency].get("status") == "DONE" for dependency in task["depends_on"])


def claim(root: Path, task_id: str | None, owner: str) -> dict[str, Any]:
    _, backlog, cycles = load_config(root)
    cycles.mkdir(parents=True, exist_ok=True)
    tasks = task_map(backlog)
    if task_id and task_id not in tasks:
        raise CycleError(f"unknown task: {task_id}")
    candidates = [tasks[task_id]] if task_id else eligible_tasks(backlog, cycles)
    if not candidates:
        raise CycleError("no eligible READY task")
    task = candidates[0]
    if task["status"] != "READY":
        raise CycleError(f"task {task['id']} is not READY")
    if not dependencies_satisfied(task, tasks, completed_task_ids(cycles)):
        raise CycleError(f"task {task['id']} has unmet dependencies")
    resource_group = task.get("resource_group")
    if resource_group:
        for cpath in cycles.glob("*.json"):
            if not cpath.is_file():
                continue
            try:
                cdata = json.loads(cpath.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if cdata.get("state") not in TERMINAL:
                c_task = tasks.get(str(cdata.get("task_id")), {})
                if c_task.get("resource_group") == resource_group:
                    raise CycleError(
                        f"resource group '{resource_group}' is currently locked by active cycle {cdata.get('cycle_id')}"
                    )
        group_lock = cycles / f"{resource_group}.group_claim"
        try:
            fd = os.open(group_lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(f"{task['id']} {owner} {utc_now()}\n")
        except FileExistsError as exc:
            raise CycleError(f"resource group '{resource_group}' is already claimed") from exc
    lock = cycles / f"{task['id']}.claim"
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(f"{owner} {utc_now()}\n")
    except FileExistsError as exc:
        if resource_group:
            (cycles / f"{resource_group}.group_claim").unlink(missing_ok=True)
        raise CycleError(f"task {task['id']} is already claimed") from exc
    cycle_id = f"CYCLE-{uuid.uuid4().hex[:10].upper()}"
    record = {
        "cycle_id": cycle_id,
        "task_id": task["id"],
        "owner": owner,
        "state": "CLAIMED",
        "prs": [],
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "history": [{"state": "CLAIMED", "at": utc_now(), "by": owner}],
    }
    write_json_atomic(cycles / f"{cycle_id}.json", record)
    return record


def load_cycle(cycles: Path, cycle_id: str) -> tuple[Path, dict[str, Any]]:
    path = cycles / f"{cycle_id}.json"
    if not path.exists():
        raise CycleError(f"cycle not found: {cycle_id}")
    try:
        return path, json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CycleError(f"invalid cycle record: {path}") from exc


def transition(root: Path, cycle_id: str, requested: str, actor: str) -> dict[str, Any]:
    flow, _, cycles = load_config(root)
    path, record = load_cycle(cycles, cycle_id)
    current = str(record["state"])
    if current in TERMINAL:
        raise CycleError(f"cycle {cycle_id} is terminal: {current}")
    definition = flow["states"].get(current)
    targets = definition.get("next", []) if definition else []
    if isinstance(targets, str):
        targets = [targets]
    if not definition or requested not in targets:
        raise CycleError(f"invalid transition {current} -> {requested}")
    record["state"] = requested
    record["updated_at"] = utc_now()
    record.setdefault("history", []).append({"state": requested, "at": utc_now(), "by": actor})
    write_json_atomic(path, record)
    return record


def reset(root: Path, cycle_id: str, state: str, actor: str) -> dict[str, Any]:
    _, backlog, cycles = load_config(root)
    path, record = load_cycle(cycles, cycle_id)
    if state not in {"READY", "BLOCKED", "FAILED"}:
        raise CycleError("reset state must be READY, BLOCKED, or FAILED")
    record["state"] = state
    record["updated_at"] = utc_now()
    record.setdefault("history", []).append({"state": state, "at": utc_now(), "by": actor, "manual": True})
    if state == "READY":
        archive = cycles / "archive"
        archive.mkdir(parents=True, exist_ok=True)
        os.replace(path, archive / path.name)
        (cycles / f"{record['task_id']}.claim").unlink(missing_ok=True)
        tasks = task_map(backlog)
        task = tasks.get(str(record.get("task_id")), {})
        rg = task.get("resource_group")
        if rg:
            (cycles / f"{rg}.group_claim").unlink(missing_ok=True)
        return record
    write_json_atomic(path, record)
    return record


def attach_pr(root: Path, cycle_id: str, url: str, actor: str, head_sha: str | None = None) -> dict[str, Any]:
    """Record the sole PR for a cycle after the controller creates it."""
    load_config(root)
    cycles = paths(root)[2]
    path, record = load_cycle(cycles, cycle_id)
    if record.get("state") not in {"VALIDATING", "PR_OPEN"}:
        raise CycleError("a PR can only be attached while the cycle is VALIDATING or PR_OPEN")
    if record.get("prs"):
        raise CycleError("cycle already has its one permitted PR")
    if not url.strip():
        raise CycleError("PR URL must not be empty")
    if head_sha is not None and (len(head_sha) != 40 or any(char not in "0123456789abcdef" for char in head_sha)):
        raise CycleError("PR head SHA must be a 40-character lowercase hex SHA")
    record["prs"] = [url]
    record["pr_head_sha"] = head_sha
    record["state"] = "PR_OPEN"
    record["updated_at"] = utc_now()
    record.setdefault("history", []).append({"state": "PR_ATTACHED", "at": utc_now(), "by": actor, "url": url})
    write_json_atomic(path, record)
    return record


def validate_cycle(root: Path, cycle_id: str, worktree: Path | None = None) -> dict[str, Any]:
    """Run the task's declared commands and store a machine-readable receipt."""
    _, backlog, cycles = load_config(root)
    path, record = load_cycle(cycles, cycle_id)
    task = task_map(backlog)[record["task_id"]]
    cwd = (worktree or root).resolve()
    results = []
    for command in task.get("validation", []):
        argv = shlex.split(command) if isinstance(command, str) else command
        if not isinstance(argv, list) or not argv or any(not isinstance(value, str) for value in argv):
            raise CycleError("validation commands must be strings or argument arrays")
        result = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, check=False)
        results.append({"argv": argv, "exit_code": result.returncode, "stdout": result.stdout[-4000:], "stderr": result.stderr[-4000:]})
    record["validation"] = results
    record["updated_at"] = utc_now()
    if any(result["exit_code"] != 0 for result in results):
        record["state"] = "FAILED"
    write_json_atomic(path, record)
    if record["state"] == "FAILED":
        raise CycleError("validation failed; receipt written to cycle record")
    return record


def verify_pr(root: Path, cycle_id: str, actor: str) -> dict[str, Any]:
    """Read the live PR and reject a changed or missing exact head."""
    load_config(root)
    cycles = paths(root)[2]
    path, record = load_cycle(cycles, cycle_id)
    urls = record.get("prs", [])
    if len(urls) != 1:
        raise CycleError("cycle must have exactly one PR before head verification")
    result = subprocess.run(
        ["gh", "pr", "view", urls[0], "--json", "number,url,state,mergedAt,headRefOid"],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise CycleError(f"PR lookup failed: {result.stderr.strip()[-500:]}")
    try:
        live = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise CycleError("gh returned invalid PR JSON") from exc
    expected = record.get("pr_head_sha")
    actual = live.get("headRefOid")
    if expected and actual != expected:
        raise CycleError(f"remote PR head changed: expected {expected}, got {actual}")
    record["live_pr"] = live
    record["updated_at"] = utc_now()
    record.setdefault("history", []).append({"state": "PR_VERIFIED", "at": utc_now(), "by": actor, "head_sha": actual})
    write_json_atomic(path, record)
    return record


def open_pr(root: Path, cycle_id: str, repository: str, actor: str, worktree: Path | None = None) -> dict[str, Any]:
    """Create or find the single PR for the cycle and pin its exact head."""
    _, backlog, cycles = load_config(root)
    path, record = load_cycle(cycles, cycle_id)
    cwd = (worktree or root).resolve()
    branch_result = subprocess.run(["git", "-C", str(cwd), "branch", "--show-current"], capture_output=True, text=True, check=False)
    branch = branch_result.stdout.strip()
    if branch_result.returncode or not branch or branch in {"main", "master"}:
        raise CycleError("open-pr requires a named non-protected branch")
    head_result = subprocess.run(["git", "-C", str(cwd), "rev-parse", "HEAD"], capture_output=True, text=True, check=False)
    if head_result.returncode:
        raise CycleError("cannot resolve local branch head")
    head_sha = head_result.stdout.strip()

    if record.get("prs"):
        record["pr_head_sha"] = head_sha
        record["state"] = "PR_OPEN"
        record["updated_at"] = utc_now()
        record.setdefault("history", []).append({
            "state": "PR_HEAD_UPDATED",
            "at": utc_now(),
            "by": actor,
            "head_sha": head_sha,
        })
        write_json_atomic(path, record)
        return verify_pr(root, cycle_id, actor)

    task = task_map(backlog)[record["task_id"]]
    body = "\n".join([
        f"## AGY Cycle {cycle_id}",
        "",
        f"Task: `{task['id']}` — {task['title']}",
        f"Exact local head: `{head_sha}`",
        "",
        "This PR was created by the deterministic AGY Cycle controller.",
    ])
    created = subprocess.run(
        ["gh", "pr", "create", "--repo", repository, "--base", "main", "--head", branch,
         "--title", f"{task['id']}: {task['title']}", "--body", body],
        capture_output=True, text=True, check=False,
    )
    if created.returncode:
        raise CycleError(f"PR creation failed: {created.stderr.strip()[-500:]}")
    url = created.stdout.strip().splitlines()[-1] if created.stdout.strip() else ""
    if not url.startswith("https://github.com/"):
        raise CycleError("gh pr create did not return a GitHub PR URL")
    record = attach_pr(root, cycle_id, url, actor, head_sha)
    return verify_pr(root, cycle_id, actor) if record.get("pr_head_sha") else record


def update_pr_head(root: Path, cycle_id: str, head_sha: str, actor: str) -> dict[str, Any]:
    """Explicitly update the recorded PR head SHA and verify against GitHub."""
    load_config(root)
    cycles = paths(root)[2]
    path, record = load_cycle(cycles, cycle_id)
    if not record.get("prs"):
        raise CycleError("cycle has no attached PR to update")
    if len(head_sha) != 40 or any(char not in "0123456789abcdef" for char in head_sha):
        raise CycleError("PR head SHA must be a 40-character lowercase hex SHA")
    record["pr_head_sha"] = head_sha
    record["updated_at"] = utc_now()
    record.setdefault("history", []).append({
        "state": "PR_HEAD_UPDATED",
        "at": utc_now(),
        "by": actor,
        "head_sha": head_sha,
    })
    write_json_atomic(path, record)
    return verify_pr(root, cycle_id, actor)


def review(root: Path, cycle_id: str, verdict: str, reviewer: str) -> dict[str, Any]:
    """Record a review verdict while strictly preventing self-review."""
    load_config(root)
    cycles = paths(root)[2]
    path, record = load_cycle(cycles, cycle_id)
    if record.get("state") != "REVIEW_REQUIRED":
        raise CycleError(f"cycle must be in REVIEW_REQUIRED to record a review (current: {record.get('state')})")
    if reviewer == record.get("owner"):
        raise CycleError(f"self-review is forbidden: reviewer '{reviewer}' cannot review cycle owned by '{record.get('owner')}'")
    if verdict not in {"APPROVED", "CHANGES_REQUESTED"}:
        raise CycleError("review verdict must be APPROVED or CHANGES_REQUESTED")
    return transition(root, cycle_id, verdict, reviewer)


def merge_check(root: Path, cycle_id: str, actor: str) -> dict[str, Any]:
    """Verify approved status and remote PR state before merge readiness."""
    load_config(root)
    cycles = paths(root)[2]
    path, record = load_cycle(cycles, cycle_id)
    if record.get("state") != "APPROVED":
        raise CycleError(f"cycle must be in APPROVED to run merge-check (current: {record.get('state')})")
    record = verify_pr(root, cycle_id, actor)
    return transition(root, cycle_id, "MERGE_READY", actor)


def reconcile(root: Path, cycle_id: str, actor: str) -> dict[str, Any]:
    """Record merged/reconciled facts without starting a successor task."""
    record = verify_pr(root, cycle_id, actor)
    live = record.get("live_pr", {})
    if not live.get("mergedAt"):
        raise CycleError("PR is not merged; reconciliation cannot complete")
    path = paths(root)[2] / f"{cycle_id}.json"
    if record.get("state") == "MERGE_READY":
        record["state"] = "MERGED"
    elif record.get("state") == "MERGED":
        record["state"] = "RECONCILED"
    record["updated_at"] = utc_now()
    if not any(item.get("state") == "RECONCILED" for item in record.get("history", [])):
        record.setdefault("history", []).append({"state": record["state"], "at": utc_now(), "by": actor})
    write_json_atomic(path, record)
    return record


def complete_cycle(root: Path, cycle_id: str, actor: str) -> dict[str, Any]:
    """Transition a reconciled cycle to COMPLETE and release locks."""
    _, backlog, cycles = load_config(root)
    path, record = load_cycle(cycles, cycle_id)
    if record.get("state") not in {"RECONCILED", "MERGE_READY"}:
        raise CycleError(f"cycle must be in RECONCILED or MERGE_READY to complete (current: {record.get('state')})")
    record = transition(root, cycle_id, "COMPLETE", actor)
    tasks = task_map(backlog)
    (cycles / f"{record['task_id']}.claim").unlink(missing_ok=True)
    task = tasks.get(str(record.get("task_id")), {})
    rg = task.get("resource_group")
    if rg:
        (cycles / f"{rg}.group_claim").unlink(missing_ok=True)
    return record


def next_action(root: Path, cycle_id: str) -> dict[str, Any]:
    flow, backlog, cycles = load_config(root)
    _, record = load_cycle(cycles, cycle_id)
    state = str(record["state"])
    definition = flow["states"].get(state)
    if not definition:
        raise CycleError(f"unknown cycle state: {state}")
    task = task_map(backlog)[record["task_id"]]
    return {"cycle_id": cycle_id, "task_id": task["id"], "state": state, "command": definition["command"], "task": task}


def prompt(root: Path, cycle_id: str) -> str:
    result = next_action(root, cycle_id)
    task = result["task"]
    template_path = root / ".agy" / "prompts" / "implement.md"
    template = template_path.read_text(encoding="utf-8")
    return template.replace("{{CYCLE_ID}}", result["cycle_id"]).replace("{{TASK_ID}}", task["id"]).replace(
        "{{TASK_TITLE}}", task["title"]
    ).replace("{{ACCEPTANCE}}", "\n".join(f"- {item}" for item in task.get("acceptance", []))).replace(
        "{{VALIDATION}}", "\n".join(f"- {item}" for item in task.get("validation", []))
    )


def run_interactive(root: Path, cycle_id: str, agy_bin: str) -> int:
    """Run AGY in a real PTY and inject exactly the generated task prompt."""
    command = shlex.split(agy_bin)
    if not command:
        raise CycleError("AGY command must not be empty")
    task_prompt = prompt(root, cycle_id).encode("utf-8") + b"\n"
    pid, master = pty.fork()
    if pid == 0:  # pragma: no cover - child process is the external CLI
        os.execvp(command[0], command)
    os.write(master, task_prompt)
    inputs = [master]
    if sys.stdin.isatty():
        inputs.append(sys.stdin)
    while inputs:
        readable, _, _ = select.select(inputs, [], [])
        for stream in readable:
            if stream == master:
                try:
                    data = os.read(master, 4096)
                except OSError:
                    data = b""
                if not data:
                    inputs.remove(master)
                else:
                    os.write(sys.stdout.fileno(), data)
            else:
                data = os.read(sys.stdin.fileno(), 4096)
                if not data:
                    inputs.remove(sys.stdin)
                else:
                    os.write(master, data)
    _, status = os.waitpid(pid, 0)
    return os.waitstatus_to_exitcode(status)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agy-cycle")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--owner", default=os.environ.get("AGY_CYCLE_OWNER", "local"))
    sub = parser.add_subparsers(dest="command", required=True)
    claim_parser = sub.add_parser("claim")
    claim_parser.add_argument("task_id", nargs="?")
    for name in ("next", "status"):
        command = sub.add_parser(name)
        command.add_argument("cycle_id")
    prompt_parser = sub.add_parser("prompt")
    prompt_parser.add_argument("cycle_id")
    for r_name in ("run", "implement"):
        run_parser = sub.add_parser(r_name)
        run_parser.add_argument("cycle_id")
        run_parser.add_argument("--agy-bin", default=os.environ.get("AGY_CLI", "agy"))
    transition_parser = sub.add_parser("transition")
    transition_parser.add_argument("cycle_id")
    transition_parser.add_argument("state")
    for res_name in ("reset", "repair"):
        reset_parser = sub.add_parser(res_name)
        reset_parser.add_argument("cycle_id")
        reset_parser.add_argument("state", nargs="?", default="READY")
    pr_parser = sub.add_parser("attach-pr")
    pr_parser.add_argument("cycle_id")
    pr_parser.add_argument("url")
    pr_parser.add_argument("--head-sha")
    u_head_parser = sub.add_parser("update-pr-head")
    u_head_parser.add_argument("cycle_id")
    u_head_parser.add_argument("--head-sha", required=True)
    for v_name in ("validate", "verify"):
        validate_parser = sub.add_parser(v_name)
        validate_parser.add_argument("cycle_id")
        validate_parser.add_argument("--worktree", type=Path)
    for vp_name in ("verify-pr", "verify-head"):
        verify_parser = sub.add_parser(vp_name)
        verify_parser.add_argument("cycle_id")
    open_parser = sub.add_parser("open-pr")
    open_parser.add_argument("cycle_id")
    open_parser.add_argument("--repository", required=True)
    open_parser.add_argument("--worktree", type=Path)
    review_parser = sub.add_parser("review")
    review_parser.add_argument("cycle_id")
    review_parser.add_argument("verdict", choices=("APPROVED", "CHANGES_REQUESTED"))
    review_parser.add_argument("--reviewer", default=os.environ.get("AGY_CYCLE_REVIEWER", "reviewer"))
    rf_parser = sub.add_parser("review-fix")
    rf_parser.add_argument("cycle_id")
    mc_parser = sub.add_parser("merge-check")
    mc_parser.add_argument("cycle_id")
    reconcile_parser = sub.add_parser("reconcile")
    reconcile_parser.add_argument("cycle_id")
    comp_parser = sub.add_parser("complete")
    comp_parser.add_argument("cycle_id")
    args = parser.parse_args(argv)
    try:
        if args.command == "claim":
            result = claim(args.root, args.task_id, args.owner)
        elif args.command == "next":
            result = next_action(args.root, args.cycle_id)
        elif args.command == "status":
            _, result = load_cycle(paths(args.root)[2], args.cycle_id)
        elif args.command == "prompt":
            print(prompt(args.root, args.cycle_id), end="")
            return 0
        elif args.command in {"run", "implement"}:
            return run_interactive(args.root, args.cycle_id, args.agy_bin)
        elif args.command == "transition":
            result = transition(args.root, args.cycle_id, args.state, args.owner)
        elif args.command == "attach-pr":
            result = attach_pr(args.root, args.cycle_id, args.url, args.owner, args.head_sha)
        elif args.command == "update-pr-head":
            result = update_pr_head(args.root, args.cycle_id, args.head_sha, args.owner)
        elif args.command in {"validate", "verify"}:
            result = validate_cycle(args.root, args.cycle_id, args.worktree)
        elif args.command in {"verify-pr", "verify-head"}:
            result = verify_pr(args.root, args.cycle_id, args.owner)
        elif args.command == "open-pr":
            result = open_pr(args.root, args.cycle_id, args.repository, args.owner, args.worktree)
        elif args.command == "review":
            result = review(args.root, args.cycle_id, args.verdict, args.reviewer)
        elif args.command == "review-fix":
            result = transition(args.root, args.cycle_id, "IMPLEMENTING", args.owner)
        elif args.command == "merge-check":
            result = merge_check(args.root, args.cycle_id, args.owner)
        elif args.command == "reconcile":
            result = reconcile(args.root, args.cycle_id, args.owner)
        elif args.command == "complete":
            result = complete_cycle(args.root, args.cycle_id, args.owner)
        else:
            result = reset(args.root, args.cycle_id, args.state, args.owner)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except CycleError as exc:
        print(f"agy-cycle: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
