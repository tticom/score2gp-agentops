#!/usr/bin/env python3
"""Convert the governed go/got assignment into the disposable-cycle envelope."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys

class AdapterError(RuntimeError):
    pass

def command_json(command: list[str], cwd: Path, env: dict[str, str]) -> dict:
    result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True)
    if result.returncode:
        raise AdapterError(f"governance dispatch failed (exit {result.returncode})")
    try:
        value = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise AdapterError("governance dispatch returned invalid JSON") from exc
    if not isinstance(value, dict) or value.get("state") in {"FAIL_CLOSED", "BLOCKED"} or value.get("ok") is False:
        raise AdapterError("governance dispatch did not return a runnable assignment")
    return value

def task_by_id(authority: dict, task_id: str) -> dict:
    candidates = ([authority["task"]] if isinstance(authority.get("task"), dict) else [])
    candidates += [item for item in authority.get("tasks", []) + authority.get("completed_tasks", []) if isinstance(item, dict)]
    for task in candidates:
        if str(task.get("id")) == task_id:
            return task
    raise AdapterError(f"task {task_id!r} is absent from orchestration authority")

def validation_commands(task: dict) -> list[list[str]]:
    result = []
    for command in task.get("validation_commands", []):
        if isinstance(command, list) and all(isinstance(value, str) for value in command):
            result.append(command)
        elif isinstance(command, str):
            result.append(shlex.split(command))
        else:
            raise AdapterError("task validation_commands contains a non-command")
    if not result:
        raise AdapterError("task has no validation_commands; runtime refuses an unvalidated cycle")
    return result

def parse_hosts(value: str) -> list[str]:
    hosts = value.split()
    if not hosts:
        raise AdapterError("SCORE2GP_EGRESS_HOSTS must name the required HTTPS services")
    return hosts

def convert(assignment: dict, authority: dict, role: str, hosts: list[str]) -> dict:
    work, worker = assignment.get("work"), assignment.get("worker")
    if not isinstance(work, dict) or not isinstance(worker, dict):
        raise AdapterError("governance assignment has no bounded work/worker sections")
    task = task_by_id(authority, str(assignment.get("authority", {}).get("task_id", "")))
    branch, head = work.get("branch"), work.get("expected_head_sha")
    if not isinstance(branch, str) or not isinstance(head, str) or len(head) != 40:
        raise AdapterError("governance assignment does not pin an exact branch head")
    # A pull request is normal for an implementation cycle. The governed worker
    # role, not PR existence, determines whether the source mount is writable.
    mode = "reviewer" if worker.get("role") in {"reviewer", "governance"} else "author"
    prompt = work.get("prompt") or task.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        raise AdapterError("task has no bounded prompt")
    repository = work.get("repository")
    if not isinstance(repository, str):
        raise AdapterError("assignment repository is missing")
    if not repository.startswith("https://"):
        repository = f"https://github.com/{repository}.git"
    return {"version": 1, "task": str(task["id"]), "role": role, "mode": mode,
            "repository": repository, "branch": branch, "base_sha": head,
            "pull_request": work.get("pull_request"),
            "allowed_paths": [] if mode == "reviewer" else work.get("allowed_paths", task.get("allowed_paths", [])),
            "validation": validation_commands(task), "egress_hosts": hosts, "prompt": prompt,
            "authority": assignment.get("authority", {}), "context_repositories": []}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--role", choices=("automation", "gov", "codex"), required=True)
    parser.add_argument("--agentops", type=Path, required=True)
    parser.add_argument("--product", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    agentops, product = args.agentops.resolve(), args.product.resolve()
    env = os.environ.copy(); env["SCORE2GP_AGENT_ROLE"] = args.role
    assignment = command_json([sys.executable, str(agentops / "scripts" / ("score2gp_go_bootstrap.py" if args.role == "automation" else "score2gp_got_bootstrap.py")), "--agentops", str(agentops), "--product", str(product), "--json"], agentops, env)
    try:
        authority = json.loads((agentops / "projects/score2gp/ORCHESTRATION_STATE.json").read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise AdapterError("cannot read orchestration authority") from exc
    converted = convert(assignment, authority, args.role, parse_hosts(os.environ.get("SCORE2GP_EGRESS_HOSTS", "")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as exc:
        raise AdapterError("refusing to overwrite an existing assignment") from exc
    with os.fdopen(descriptor, "w") as stream:
        json.dump(converted, stream, indent=2); stream.write("\n")
    print(args.output); return 0

if __name__ == "__main__":
    try: raise SystemExit(main())
    except AdapterError as exc:
        print(f"error: {exc}", file=sys.stderr); raise SystemExit(64)
