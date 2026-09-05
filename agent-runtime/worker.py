#!/usr/bin/env python3
"""Container-only agent entrypoint. The host owns validation and checkpointing."""
import json
import os
from pathlib import Path
import subprocess
import sys


def main():
    data = json.loads(Path("/assignment.json").read_text())
    os.environ["GH_TOKEN"] = Path("/run/secrets/github-token").read_text().strip()
    os.environ["GIT_ASKPASS"] = "/usr/local/bin/github-askpass.sh"
    os.environ["GIT_TERMINAL_PROMPT"] = "0"
    prompt = data["prompt"] + (
        f"\nCycle {os.environ['SCORE2GP_CYCLE_ID']}: remain on {data['branch']}. "
        "The host controller owns final validation, commit and push. Do not push or switch branches. "
        "Use the supplied bounded assignment; do not select another task."
    )
    if data["mode"] == "reviewer":
        prompt += ("\nSource is read-only. Publish your formal review on the assigned PR at the assigned head, "
                   f"including <!-- score2gp-cycle:{os.environ['SCORE2GP_CYCLE_ID']} --> in its body.")
    engine, *extra = sys.argv[1:]
    if engine == "agy":
        for plugin in ("engineering", "productivity"):
            result = subprocess.run(["agy", "plugin", "install", f"/workspace/agy-skills/plugins/{plugin}"])
            if result.returncode:
                return result.returncode
        command = ["agy", "--dangerously-skip-permissions", *extra, "--print", prompt]
    else:
        command = ["codex", "exec", "--ephemeral", "--dangerously-bypass-approvals-and-sandbox", "--add-dir", "/workspace/agy-skills", *extra, prompt]
    return subprocess.run(command).returncode


if __name__ == "__main__":
    sys.exit(main())
