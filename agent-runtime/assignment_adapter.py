#!/usr/bin/env python3
"""Convert the governed go/got assignment into the disposable-cycle envelope."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys

class AdapterError(RuntimeError):
    pass

def diagnostic(result: subprocess.CompletedProcess) -> str:
    detail = result.stderr.strip() or result.stdout.strip() or "no diagnostic output"
    return re.sub(
        r"(?i)(token|password|secret|authorization|credential)\s*[=:]\s*[^\s]+",
        r"\1=[REDACTED]",
        detail,
    )[:500]

def role_dispatch_environment(role: str) -> dict[str, str]:
    env = os.environ.copy()
    project = env.get("SCORE2GP_GCP_PROJECT_ID", "")
    secret = env.get("SCORE2GP_GITHUB_SECRET_NAME", f"score2gp-github-{role}-token")
    if not project:
        raise AdapterError("SCORE2GP_GCP_PROJECT_ID is required before governance dispatch")
    result = subprocess.run(
        ["gcloud", "secrets", "versions", "access", "latest",
         f"--secret={secret}", f"--project={project}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise AdapterError(
            f"GitHub secret lookup failed (exit {result.returncode}): {diagnostic(result)}"
        )
    token = result.stdout.strip()
    if not token or "\n" in token or "\r" in token:
        raise AdapterError("GitHub secret lookup returned an invalid token")
    env["GH_TOKEN"] = token
    return env

def command_json(command: list[str], cwd: Path, env: dict[str, str]) -> dict:
    result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True)
    if result.returncode:
        raise AdapterError(
            f"governance dispatch failed (exit {result.returncode}): {diagnostic(result)}"
        )
    try:
        value = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise AdapterError("governance dispatch returned invalid JSON") from exc
    if not isinstance(value, dict) or value.get("state") in {"FAIL_CLOSED", "BLOCKED"} or value.get("ok") is False:
        raise AdapterError("governance dispatch did not return a runnable assignment")
    return value

def task_by_id(authority: dict, task_id: str) -> dict:
    candidates = ([authority["task"]] if isinstance(authority.get("task"), dict) else [])
    if isinstance(authority.get("task_registry"), dict):
        if task_id in authority["task_registry"]:
            return authority["task_registry"][task_id]
        candidates += list(authority["task_registry"].values())
    candidates += [item for item in authority.get("tasks", []) + authority.get("completed_tasks", []) if isinstance(item, dict)]
    proposal = authority.get("next_task_proposal")
    if isinstance(proposal, dict):
        candidates.append(proposal)
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

def remote_branch_head(repository: str, branch: str) -> str | None:
    result = subprocess.run(
        ["git", "ls-remote", repository, f"refs/heads/{branch}"],
        capture_output=True, text=True, check=False,
    )
    fields = result.stdout.split()
    if result.returncode:
        raise AdapterError(f"cannot inspect assigned branch: {diagnostic(result)}")
    if not fields:
        return None
    if len(fields) != 2 or len(fields[0]) != 40:
        raise AdapterError("assigned branch does not have an exact remote head")
    return fields[0]

def git_checked(product: Path, args: list[str], env: dict[str, str]) -> str:
    result = subprocess.run(
        ["git", "-C", str(product), *args],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise AdapterError(f"product git {' '.join(args)} failed: {diagnostic(result)}")
    return result.stdout.strip()

def ensure_task_branch(
    repository: str,
    branch: str,
    product: Path,
    env: dict[str, str],
) -> str:
    current = remote_branch_head(repository, branch)
    if current is not None:
        return current
    # The task repository may differ from the product checkout (for example,
    # governance tasks run in AgentOps while the product checkout is score2gp).
    # Resolve the branch base from the repository that will receive the ref.
    base = remote_branch_head(repository, "main")
    if base is None:
        raise AdapterError("task repository main does not have an exact remote head")
    slug = repository.removeprefix("https://github.com/").removesuffix(".git")
    result = subprocess.run(
        ["gh", "api", f"repos/{slug}/git/refs", "-f", f"ref=refs/heads/{branch}", "-f", f"sha={base}"],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        current = remote_branch_head(repository, branch)
        if current == base:
            return current
        raise AdapterError(f"task branch creation failed: {diagnostic(result)}")
    current = remote_branch_head(repository, branch)
    if current != base:
        raise AdapterError("created task branch did not read back at product origin/main")
    return current

def convert(
    assignment: dict,
    authority: dict,
    role: str,
    hosts: list[str],
    product: Path | None = None,
    env: dict[str, str] | None = None,
) -> dict:
    work, worker = assignment.get("work"), assignment.get("worker")
    if not isinstance(work, dict) or not isinstance(worker, dict):
        raise AdapterError("governance assignment has no bounded work/worker sections")
    task = task_by_id(authority, str(assignment.get("authority", {}).get("task_id", "")))
    repository = work.get("repository")
    if not isinstance(repository, str):
        raise AdapterError("assignment repository is missing")
    if not repository.startswith("https://"):
        repository = f"https://github.com/{repository}.git"
    branch, head = work.get("branch"), work.get("expected_head_sha")
    if not isinstance(branch, str):
        raise AdapterError("governance assignment is missing its branch")
    if head is None and work.get("pull_request") is None:
        head = remote_branch_head(repository, branch)
        if head is None:
            if product is None or env is None:
                raise AdapterError("assigned branch does not have an exact remote head")
            head = ensure_task_branch(repository, branch, product, env)
    if not isinstance(head, str) or len(head) != 40:
        raise AdapterError("governance assignment does not pin an exact branch head")
    # A pull request is normal for an implementation cycle. Governance promotion
    # is a bounded author action even when its source PR is already merged;
    # only the reviewer role requires a read-only source mount.
    mode = "reviewer" if worker.get("role") == "reviewer" else "author"
    prompt = work.get("prompt") or task.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        raise AdapterError("task has no bounded prompt")
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
    dispatch_env = role_dispatch_environment(args.role)
    assignment = command_json([sys.executable, str(agentops / "scripts" / ("score2gp_go_bootstrap.py" if args.role == "automation" else "score2gp_got_bootstrap.py")), "--agentops", str(agentops), "--product", str(product), "--json"], agentops, dispatch_env)
    try:
        authority = json.loads((agentops / "projects/score2gp/ORCHESTRATION_STATE.json").read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise AdapterError("cannot read orchestration authority") from exc
    converted = convert(
        assignment,
        authority,
        args.role,
        parse_hosts(os.environ.get("SCORE2GP_EGRESS_HOSTS", "")),
        product=product,
        env=dispatch_env,
    )
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
