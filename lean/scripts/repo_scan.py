#!/usr/bin/env python3
"""Scan tracked files for things that must never be committed (CI gate).

Checks every git-tracked file for:
  forbidden-extension  .pdf .gp .gp3 .gp4 .gp5 .gpx .mxl .png .jpg .jpeg .gif .zip
                       (private fixture and artifact types) unless allow-listed
  too-large            larger than --max-bytes (default 1 MB) unless allow-listed
  local-path           an absolute local user path (Windows drive path under Users,
                       /home/<user>/, /Users/<user>/)
  secret               a credential-shaped token or private key header
  private-name         a line containing a name from --names-file (one literal per line;
                       e.g. private fixture names; the file itself is not committed)

Output is SANITISED: path, line number and rule only. Matched text is never printed.
Exit 0 clean, 1 findings, 64 usage. Allow-list: --allow GLOB (repeatable) or a
`.scan-allow` file in the repo root, one glob per line, `#` comments. Allow-listed paths
skip the extension and size rules only, never the secret, local-path or name rules.
"""

from __future__ import annotations

import argparse
import fnmatch
import re
import subprocess
import sys
from pathlib import Path

FORBIDDEN_EXT = {".pdf", ".gp", ".gp3", ".gp4", ".gp5", ".gpx", ".mxl", ".png", ".jpg", ".jpeg", ".gif", ".zip"}

# Patterns are assembled from parts so this file does not match its own rules.
SECRET = re.compile(
    "|".join(
        [
            "gh" + r"[pousr]_[A-Za-z0-9]{30,}",
            "github" + "_pat_" + r"[A-Za-z0-9_]{30,}",
            "sk" + "-ant-" + r"[A-Za-z0-9_-]{20,}",
            "AK" + "IA" + r"[0-9A-Z]{16}",
            "-----BEGIN " + r"(?:[A-Z]+ )?PRIVATE KEY-----",
        ]
    )
)
LOCAL_PATH = re.compile(
    r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s]+"
    r"|(?<![\w.])/home/[a-z_][\w-]*/"
    r"|(?<![\w.])/Users/[A-Za-z][\w.-]*/"
)


PLACEHOLDER_USERS = {"user", "username", "you", "name", "example", "me", "runner", "yourname", "your-name"}
USER_SEGMENT = re.compile(r"(?:[A-Za-z]:[\\/]+Users[\\/]+|/home/|/Users/)([^\\/\s]+)")


def _placeholder_user(match: "re.Match[str]") -> bool:
    """A path whose user segment is an obvious placeholder (user, you, <name>) is not a leak."""
    found = USER_SEGMENT.search(match.group(0))
    user = found.group(1).lower() if found else ""
    return user in PLACEHOLDER_USERS or user.startswith(("<", "{", "$", "%"))


def tracked_files(repo: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "-z"], check=False, capture_output=True
    )
    if result.returncode:
        raise SystemExit("NOT_A_GIT_REPOSITORY")
    return [p for p in result.stdout.decode("utf-8", "replace").split("\0") if p]


def load_allow(repo: Path, extra: list[str]) -> list[str]:
    patterns = list(extra)
    allow_file = repo / ".scan-allow"
    if allow_file.is_file():
        for line in allow_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(line)
    return patterns


def allowed(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pat) for pat in patterns)


def scan(repo: Path, allow: list[str], max_bytes: int, names: list[str]) -> list[tuple[str, int, str]]:
    findings: list[tuple[str, int, str]] = []
    for rel in tracked_files(repo):
        path = repo / rel
        if not path.is_file():
            continue
        skip_size_ext = allowed(rel, allow)
        if not skip_size_ext:
            if path.suffix.lower() in FORBIDDEN_EXT:
                findings.append((rel, 0, "forbidden-extension"))
            if path.stat().st_size > max_bytes:
                findings.append((rel, 0, "too-large"))
        data = path.read_bytes()
        if b"\0" in data:
            continue  # binary: only the extension and size rules apply
        text = data.decode("utf-8", "replace")
        for number, line in enumerate(text.splitlines(), 1):
            if SECRET.search(line):
                findings.append((rel, number, "secret"))
            if any(not _placeholder_user(m) for m in LOCAL_PATH.finditer(line)):
                findings.append((rel, number, "local-path"))
            if names and any(n in line for n in names):
                findings.append((rel, number, "private-name"))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--allow", action="append", default=[], help="glob exempt from extension/size rules")
    parser.add_argument("--max-bytes", type=int, default=1_000_000)
    parser.add_argument("--names-file", type=Path, help="private names, one literal per line (kept outside the repo)")
    args = parser.parse_args(argv)

    names: list[str] = []
    if args.names_file:
        if not args.names_file.is_file():
            print("NAMES_FILE_MISSING", file=sys.stderr)
            return 64
        names = [n.strip() for n in args.names_file.read_text(encoding="utf-8").splitlines() if len(n.strip()) >= 4]
    findings = scan(args.repo, load_allow(args.repo, args.allow), args.max_bytes, names)
    for rel, line, rule in findings:
        print(f"{rel}:{line or '-'}: {rule}")
    print(f"repo_scan: {len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
