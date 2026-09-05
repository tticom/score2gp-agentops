#!/usr/bin/env python3
"""Host controller for one assigned, recoverable agent cycle. Standard library only."""
from __future__ import annotations

import argparse
import ipaddress
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import signal
import subprocess
import sys
import uuid


RUNTIME = Path(__file__).resolve().parent
IDENTITIES = {
    "automation": ("tticom-automation", "tticomautomation@gmail.com"),
    "gov": ("tticomgov-code", "tticomgov-code@users.noreply.github.com"),
    "codex": ("tticom-codex", "tticom-codex@users.noreply.github.com"),
}
FORBIDDEN = {".git", "private", "raw", "generated", "work"}


class CycleError(RuntimeError):
    pass


def run(args, *, cwd=None, env=None, capture=True):
    result = subprocess.run([str(x) for x in args], cwd=cwd, env=env,
                            text=True, capture_output=capture)
    if result.returncode:
        # Do not print subprocess output: remote errors can contain credentials.
        raise CycleError(f"{args[0]} {args[1]} failed (exit {result.returncode})")
    return result.stdout.strip() if capture else ""


def git(repo, *args, env=None):
    return run(["git", "-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false",
                "-c", "credential.helper=", "-C", repo, *args], env=env)


def valid_host(host):
    if not isinstance(host, str) or not re.fullmatch(r"[a-z0-9]+(?:[.-][a-z0-9]+)*\.[a-z]{2,}", host):
        return False
    try:
        ipaddress.ip_address(host)
        return False
    except ValueError:
        return True


def valid_repository(url):
    return (isinstance(url, str) and re.fullmatch(
        r"https://github\.com/tticom/(?:score2gp(?:-[a-z0-9-]+)?|agy-skills)\.git", url
    ) and "private-fixtures" not in url)


def safe_path(path):
    parts = PurePosixPath(path).parts
    return (bool(parts) and not path.startswith("/") and "\\" not in path
            and not any(ord(c) < 32 for c in path)
            and all(p not in FORBIDDEN | {"..", "."} for p in parts)
            and ".agent-cycles" not in parts)


def validate_assignment(data):
    required = {"version", "task", "role", "mode", "repository", "branch", "base_sha",
                "allowed_paths", "validation", "egress_hosts", "prompt"}
    if not isinstance(data, dict) or not required <= data.keys():
        raise CycleError("assignment is missing required fields")
    if data["version"] != 1 or data["role"] not in IDENTITIES or data["mode"] not in {"author", "reviewer"}:
        raise CycleError("unsupported assignment version, role or mode")
    if not isinstance(data["task"], str) or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._-]*", data["task"]):
        raise CycleError("invalid task slug")
    if not valid_repository(data["repository"]) or data["repository"].endswith("/agy-skills.git"):
        raise CycleError("repository must be an approved GitHub HTTPS repository without credentials")
    branch = data["branch"]
    if not isinstance(branch, str) or branch in {"main", "master", "HEAD"} or "/" not in branch:
        raise CycleError("an explicit non-protected task branch is required")
    run(["git", "check-ref-format", "--branch", branch])
    if not isinstance(data["base_sha"], str) or not re.fullmatch(r"[0-9a-f]{40}", data["base_sha"]):
        raise CycleError("base_sha must pin the assigned branch head")
    paths = data["allowed_paths"]
    if not isinstance(paths, list) or any(not isinstance(p, str) or not safe_path(p) or "*" in p for p in paths):
        raise CycleError("allowed_paths must contain explicit safe files or directory prefixes")
    if data["mode"] == "author" and not paths:
        raise CycleError("author requires permitted paths")
    if data["mode"] == "reviewer" and (paths or type(data.get("pull_request")) is not int or data["pull_request"] < 1):
        raise CycleError("reviewer requires a PR number and no writable source paths")
    if not isinstance(data["validation"], list) or not data["validation"] or any(
        not isinstance(argv, list) or not argv or any(not isinstance(v, str) or not v or "\0" in v for v in argv)
        for argv in data["validation"]
    ):
        raise CycleError("validation must contain nonempty command argument arrays")
    if not isinstance(data["egress_hosts"], list) or not data["egress_hosts"] or any(
        not valid_host(h) for h in data["egress_hosts"]
    ):
        raise CycleError("egress_hosts requires exact DNS names, without wildcards or IP addresses")
    if not isinstance(data["prompt"], str) or not data["prompt"].strip():
        raise CycleError("a bounded worker prompt is required")
    contexts = data.get("context_repositories", [])
    if not isinstance(contexts, list):
        raise CycleError("context_repositories must be a list of pinned read-only repositories")
    seen = {data["repository"], "https://github.com/tticom/agy-skills.git"}
    for context in contexts:
        if (not isinstance(context, dict) or not valid_repository(context.get("repository"))
                or context["repository"] in seen or not isinstance(context.get("sha"), str)
                or not re.fullmatch(r"[0-9a-f]{40}", context["sha"])):
            raise CycleError("context repositories must be distinct approved repositories with exact SHAs")
        seen.add(context["repository"])
    return data


def clone_branch(remote, branch, base, destination, env):
    # --no-local also avoids hardlinks when exercising this against local test remotes.
    run(["git", "clone", "--no-local", "--single-branch", "--branch", branch,
         "--", remote, destination], env=env)
    if git(destination, "rev-parse", "HEAD", env=env) != base:
        raise CycleError("assigned branch moved; retain clone and resolve a fresh assignment")


def sanitize_git_config(repo, remote, env):
    """Never execute worker-supplied filters, hooks or credential helpers on the host."""
    metadata = repo / ".git"
    if metadata.is_symlink() or not metadata.is_dir():
        raise CycleError("cycle Git metadata was replaced")
    if any(p.is_symlink() or (p.is_file() and p.stat().st_nlink != 1) for p in metadata.rglob("*")):
        raise CycleError("symlinks or hardlinks in Git metadata are not permitted")
    if any((metadata / p).exists() for p in ("objects/info/alternates", "info/grafts", "shallow")):
        raise CycleError("external or rewritten Git object histories are not permitted")
    (metadata / "config").write_text("[core]\n\trepositoryformatversion = 0\n\tbare = false\n\tfilemode = true\n")
    git(repo, "remote", "add", "origin", remote, env=env)


def check_paths(paths, allowed):
    for path in paths:
        if not safe_path(path) or not any(path == p or (p.endswith("/") and path.startswith(p)) for p in allowed):
            raise CycleError(f"out-of-scope path; clone retained: {path!r}")


def checkpoint(repo, remote, branch, base, allowed, receipt, name, email, env):
    env = {k: v for k, v in env.items() if not k.startswith("GIT_") or k in {"GIT_ASKPASS", "GIT_TERMINAL_PROMPT", "GIT_CONFIG_GLOBAL", "GIT_CONFIG_NOSYSTEM"}}
    env.update(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1",
               GIT_NO_REPLACE_OBJECTS="1",
               GIT_AUTHOR_NAME=name, GIT_AUTHOR_EMAIL=email,
               GIT_COMMITTER_NAME=name, GIT_COMMITTER_EMAIL=email)
    sanitize_git_config(repo, remote, env)
    if git(repo, "symbolic-ref", "--short", "HEAD", env=env) != branch:
        raise CycleError("worker switched branches; clone retained")
    git(repo, "merge-base", "--is-ancestor", base, "HEAD", env=env)
    # Check every new commit, including files added and subsequently deleted.
    commits = git(repo, "rev-list", f"{base}..HEAD", env=env).splitlines()
    for commit in commits:
        changed = git(repo, "diff-tree", "--root", "-m", "--no-commit-id", "--name-only", "--no-renames", "-r", "-z", commit, env=env)
        check_paths(filter(None, changed.split("\0")), allowed)
    changed = git(repo, "diff", "HEAD", "--name-only", "--no-renames", "-z", env=env)
    untracked = git(repo, "ls-files", "--others", "--exclude-standard", "-z", env=env)
    check_paths(filter(None, (changed + "\0" + untracked).split("\0")), allowed)
    # Do not silently dispose of ignored work. Known runtime caches are disposable.
    ignored = git(repo, "ls-files", "--others", "--ignored", "--exclude-standard", "-z", env=env)
    for path in filter(None, ignored.split("\0")):
        if not any(p in {"__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache"} for p in PurePosixPath(path).parts):
            raise CycleError(f"ignored output requires recovery before disposal: {path!r}")
    current = git(repo, "ls-remote", "--exit-code", remote, f"refs/heads/{branch}", env=env).split()[0]
    if current != base:
        raise CycleError("remote branch moved during cycle; clone retained")
    git(repo, "add", "--all", "--", ".", env=env)
    # Commit-message evidence travels with the branch without creating governance
    # files in a product repository or granting an extra writable source path.
    git(repo, "commit", "--allow-empty", "-m", f"checkpoint: cycle {receipt['cycle_id']}",
        "-m", json.dumps(receipt, indent=2), env=env)
    head = git(repo, "rev-parse", "HEAD", env=env)
    # No force or lease: a concurrent divergent push must be rejected by Git.
    git(repo, "push", "--porcelain", remote, f"HEAD:refs/heads/{branch}", env=env)
    published = git(repo, "ls-remote", "--exit-code", remote, f"refs/heads/{branch}", env=env).split()[0]
    if published != head or git(repo, "status", "--porcelain", env=env):
        raise CycleError("remote checkpoint or clean worktree verification failed")
    return head


def common_container(name, image, uid, gid):
    return ["docker", "run", "--rm", "--name", name, "--user", f"{uid}:{gid}",
            "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges:true",
            "--pids-limit", "512", "--memory", "4g", "--cpus", "2", "--init",
            "--tmpfs", f"/tmp:rw,noexec,nosuid,nodev,size=256m,uid={uid},gid={gid},mode=1777",
            "--tmpfs", f"/test-tmp:rw,exec,nosuid,nodev,size=256m,uid={uid},gid={gid},mode=1777",
            "--tmpfs", f"/home/agent:rw,exec,nosuid,nodev,size=512m,uid={uid},gid={gid},mode=700"]


def bind(source, target, readonly=True):
    if any(c in str(source) for c in ",\n\r"):
        raise CycleError("mount path contains unsupported characters")
    return ["--mount", f"type=bind,src={source},dst={target}" + (",readonly" if readonly else "")]


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n")


def execute(data, engine, extra):
    uid, gid = os.getuid(), os.getgid()
    if uid == 0:
        raise CycleError("run the controller as the distribution's non-root owner")
    if data["role"] != os.environ.get("SCORE2GP_AGENT_ROLE", data["role"]):
        raise CycleError("assignment role differs from instance role")
    login, email = IDENTITIES[data["role"]]
    image_tag = os.environ.get("SCORE2GP_CODEX_IMAGE" if engine == "codex" else "SCORE2GP_AGENT_IMAGE",
                               f"score2gp-{'codex' if engine == 'codex' else 'agent'}:local")
    image = run(["docker", "image", "inspect", "--format", "{{.Id}}", image_tag])
    root = Path(os.environ.get("SCORE2GP_CYCLE_ROOT", str(Path.home() / ".local/state/score2gp/cycles")))
    cycle_id = f"{data['role']}-{uuid.uuid4().hex}"
    folder = root / cycle_id
    folder.mkdir(parents=True, mode=0o700)
    folder.chmod(0o700)
    repo = folder / "repo"
    repo_target = "/workspace/" + data["repository"].rsplit("/", 1)[1].removesuffix(".git")
    secret = folder / "github-token"
    network, proxy_name, worker_name = (f"score2gp-{cycle_id}-{suffix}" for suffix in ("net", "proxy", "worker"))
    receipt = {"cycle_id": cycle_id, "assignment": data, "image_id": image,
               "status": "retained", "validation": []}
    write_json(folder / "receipt.json", receipt)
    print(f"cycle: {cycle_id}\nrecovery: {folder}", flush=True)
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0")
    try:
        project = os.environ.get("SCORE2GP_GCP_PROJECT_ID", "")
        secret_name = os.environ.get("SCORE2GP_GITHUB_SECRET_NAME", f"score2gp-github-{data['role']}-token")
        if not project:
            raise CycleError("SCORE2GP_GCP_PROJECT_ID is required")
        token = run(["gcloud", "secrets", "versions", "access", "latest", f"--secret={secret_name}", f"--project={project}"])
        if not token or "\n" in token or "\r" in token:
            raise CycleError("invalid GitHub secret")
        secret.write_text(token)
        secret.chmod(0o600)
        askpass = folder / "askpass.sh"
        askpass.write_text('#!/bin/sh\ncase "$1" in *Username*) printf "%s\\n" x-access-token ;; *) cat "$SCORE2GP_TOKEN_FILE" ;; esac\n')
        askpass.chmod(0o700)
        env.update(GH_TOKEN=token, GIT_ASKPASS=str(askpass), SCORE2GP_TOKEN_FILE=str(secret))
        if run(["gh", "api", "user", "--jq", ".login"], env=env) != login:
            raise CycleError("GitHub secret does not belong to the assigned role")
        if data["mode"] == "reviewer":
            slug = data["repository"].removeprefix("https://github.com/").removesuffix(".git")
            pr = json.loads(run(["gh", "api", f"repos/{slug}/pulls/{data['pull_request']}"], env=env))
            if (pr["head"]["sha"] != data["base_sha"] or pr["head"]["ref"] != data["branch"]
                    or pr["user"]["login"] == login or pr["state"] != "open"
                    or pr["head"]["repo"]["full_name"] != slug):
                raise CycleError("review must target another author's open PR at the assigned repository, branch and head")
        clone_branch(data["repository"], data["branch"], data["base_sha"], repo, env)
        git(repo, "config", "user.name", login, env=env)
        git(repo, "config", "user.email", email, env=env)
        context_mounts = []
        for context in data.get("context_repositories", []):
            name = context["repository"].rsplit("/", 1)[1].removesuffix(".git")
            destination = folder / "context" / name
            destination.mkdir(parents=True)
            git(destination, "init", env=env)
            git(destination, "fetch", "--depth=1", context["repository"], context["sha"], env=env)
            git(destination, "checkout", "--detach", "FETCH_HEAD", env=env)
            if git(destination, "rev-parse", "HEAD", env=env) != context["sha"]:
                raise CycleError("context repository did not resolve to its assigned SHA")
            context_mounts += bind(destination, f"/workspace/{name}")
        write_json(folder / "assignment.json", data)
        passwd = folder / "passwd"
        passwd.write_text(f"root:x:0:0:root:/root:/usr/sbin/nologin\nagent:x:{uid}:{gid}:agent:/home/agent:/usr/sbin/nologin\n")
        group = folder / "group"
        group.write_text(f"root:x:0:\nagent:x:{gid}:\n")
        run(["docker", "network", "create", "--internal", network])
        proxy = common_container(proxy_name, image, uid, gid)
        proxy += ["--detach", "--network", "bridge", "--entrypoint", "python"]
        proxy += bind(RUNTIME / "egress_proxy.py", "/egress_proxy.py")
        proxy += bind(folder / "assignment.json", "/assignment.json")
        run(proxy + [image, "/egress_proxy.py", "/assignment.json"])
        run(["docker", "network", "connect", "--alias", "egress", network, proxy_name])
        run(["docker", "exec", proxy_name, "python", "-c",
             "import socket,time\nfor attempt in range(50):\n try:\n  socket.create_connection(('127.0.0.1',3128),1).close(); break\n except OSError: time.sleep(.1)\nelse: raise SystemExit(1)"])
        worker_argv = common_container(worker_name, image, uid, gid)
        interactive_auth = os.environ.get("SCORE2GP_INTERACTIVE_AUTH") == "1" and sys.stdin.isatty()
        if interactive_auth:
            worker_argv[2:2] = ["--interactive", "--tty"]
        worker_argv += ["--network", network, "--workdir", repo_target, "--entrypoint", "python"]
        worker_argv += bind(repo, repo_target, data["mode"] == "reviewer") + context_mounts
        worker_argv += bind(passwd, "/etc/passwd") + bind(group, "/etc/group")
        worker_argv += bind(secret, "/run/secrets/github-token")
        worker_argv += bind(folder / "assignment.json", "/assignment.json")
        worker_argv += bind(RUNTIME / "worker.py", "/worker.py")
        for key, value in {
            "HOME": "/home/agent", "USER": "agent", "LOGNAME": "agent", "CODEX_HOME": "/home/agent/.codex",
            "SCORE2GP_AGENT_ROLE": data["role"], "SCORE2GP_CYCLE_ID": cycle_id,
            "SCORE2GP_TASK": data["task"], "PYTHONPATH": f"{repo_target}/src:{repo_target}",
            "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": "/test-tmp", "PYTEST_ADDOPTS": "-p no:cacheprovider",
            "HTTP_PROXY": "http://egress:3128", "HTTPS_PROXY": "http://egress:3128",
            "http_proxy": "http://egress:3128", "https_proxy": "http://egress:3128", "NO_PROXY": "", "no_proxy": "",
            "GIT_AUTHOR_NAME": login, "GIT_AUTHOR_EMAIL": email,
            "GIT_COMMITTER_NAME": login, "GIT_COMMITTER_EMAIL": email,
        }.items():
            worker_argv += ["--env", f"{key}={value}"]
        # Only agent authentication/config state persists; source and packages do not.
        auth_root = Path.home() / ".local/share/score2gp" / data["role"] / "auth"
        for dirname in ([".codex"] if engine == "codex" else [".config", ".gemini"]):
            auth = auth_root / dirname
            auth.mkdir(parents=True, exist_ok=True, mode=0o700)
            if auth.is_symlink() or auth.stat().st_uid != uid:
                raise CycleError("authentication state has unexpected ownership or is a symlink")
            worker_argv += bind(auth, f"/home/agent/{dirname}", False)
        skills = Path(os.environ.get("AGY_SKILLS_DIR", str(Path.home() / "work/score2gp-workspace/agy-skills"))).resolve()
        if not skills.is_dir():
            raise CycleError("AGY_SKILLS_DIR must name the installed skills checkout")
        receipt["skills_sha"] = git(skills, "rev-parse", "HEAD", env=env)
        if git(skills, "status", "--porcelain", env=env):
            raise CycleError("skills checkout must be clean")
        skills_snapshot = folder / "skills"
        run(["git", "clone", "--no-local", "--no-checkout", "--", skills, skills_snapshot], env=env)
        git(skills_snapshot, "checkout", "--detach", receipt["skills_sha"], env=env)
        worker_argv += bind(skills_snapshot, "/workspace/agy-skills")
        # Interactive WSL launches may complete first-run AGY auth; unattended
        # cycles remain noninteractive and fail closed if auth is missing.
        agent_stdin = None if interactive_auth else subprocess.DEVNULL
        agent = subprocess.run(worker_argv + [image, "/worker.py", engine, *extra], stdin=agent_stdin)
        receipt["agent_exit_code"] = agent.returncode
        if agent.returncode != 0:
            raise CycleError(f"agent exited {agent.returncode}; clone retained without automatic checkpoint")
        # Validate offline in new containers, without the token, auth or skills mounts.
        for index, argv in enumerate(data["validation"]):
            validation = common_container(worker_name, image, uid, gid)
            validation += ["--network", "none", "--workdir", repo_target, "--entrypoint", argv[0]]
            validation += bind(repo, repo_target, data["mode"] == "reviewer") + context_mounts
            validation += bind(passwd, "/etc/passwd") + bind(group, "/etc/group")
            validation += ["--env", "HOME=/home/agent", "--env", f"PYTHONPATH={repo_target}/src:{repo_target}",
                           "--env", "PYTHONDONTWRITEBYTECODE=1", "--env", "PYTEST_ADDOPTS=-p no:cacheprovider", "--env", "TMPDIR=/test-tmp"]
            with (folder / f"validation-{index}.log").open("w") as output:
                result = subprocess.run(validation + [image, *argv[1:]], stdout=output, stderr=subprocess.STDOUT)
            receipt["validation"].append({"argv": argv, "exit_code": result.returncode})
        if data["mode"] == "author":
            receipt["status"] = "checkpoint"
            checkpoint_receipt = {"cycle_id": cycle_id, "task": data["task"], "base_sha": data["base_sha"],
                                  "image_id": image, "skills_sha": receipt["skills_sha"],
                                  "validation": receipt["validation"],
                                  "context_repositories": data.get("context_repositories", [])}
            receipt["published_head"] = checkpoint(repo, data["repository"], data["branch"], data["base_sha"],
                                                   data["allowed_paths"], checkpoint_receipt, login, email, env)
        else:
            slug = data["repository"].removeprefix("https://github.com/").removesuffix(".git")
            current = json.loads(run(["gh", "api", f"repos/{slug}/pulls/{data['pull_request']}"], env=env))
            if current["head"]["sha"] != data["base_sha"] or current["state"] != "open":
                raise CycleError("PR changed during review; clone retained")
            reviews = json.loads(run(["gh", "api", "--paginate", "--slurp", f"repos/{slug}/pulls/{data['pull_request']}/reviews"], env=env))
            found = [review for page in reviews for review in page if review["user"]["login"] == login
                     and review["commit_id"] == data["base_sha"] and review["state"] in {"COMMENTED", "APPROVED", "CHANGES_REQUESTED"}
                     and f"<!-- score2gp-cycle:{cycle_id} -->" in (review.get("body") or "")]
            if not found:
                raise CycleError("no published exact-head review receipt; clone retained")
            receipt["review_url"] = found[-1]["html_url"]
        if any(v["exit_code"] != 0 for v in receipt["validation"]):
            raise CycleError("validation failed; checkpoint published, clone retained")
        receipt["status"] = "complete"
        # This unique clone was created by this invocation; remote work is verified above.
        shutil.rmtree(repo)
        if (folder / "context").exists():
            shutil.rmtree(folder / "context")
        shutil.rmtree(skills_snapshot)
        print("cycle complete: remote evidence verified; disposable clone removed", flush=True)
        return 0
    except (CycleError, KeyboardInterrupt) as exc:
        receipt["status"] = "retained"
        receipt["reason"] = str(exc) or "interrupted"
        print(f"cycle retained: {receipt['reason']}\nrecovery: {folder}", file=sys.stderr)
        return 1
    finally:
        # Supervise Docker instead of exec: ordinary exit and SIGINT/SIGTERM reach cleanup.
        for name in (worker_name, proxy_name):
            subprocess.run(["docker", "rm", "--force", name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["docker", "network", "rm", network], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        secret.unlink(missing_ok=True)
        write_json(folder / "receipt.json", receipt)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", choices=("agy", "codex"), required=True)
    parser.add_argument("--assignment", default=os.environ.get("SCORE2GP_CYCLE_ASSIGNMENT"))
    args, extra = parser.parse_known_args()
    if not args.assignment:
        parser.error("set SCORE2GP_CYCLE_ASSIGNMENT to an approved cycle assignment")
    def interrupted(signum, frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, interrupted)
    try:
        data = validate_assignment(json.loads(Path(args.assignment).read_text()))
        return execute(data, args.engine, extra)
    except (CycleError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 64


if __name__ == "__main__":
    sys.exit(main())
