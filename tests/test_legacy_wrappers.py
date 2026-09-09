import subprocess
import sys
import os
from types import SimpleNamespace

import pytest

from scripts import score2gp_go_bootstrap, score2gp_got_bootstrap

def setup_clean_repo(tmp_path):
    repo_path = tmp_path / "repo"
    repo_path.mkdir()
    subprocess.run(["git", "init", "--initial-branch=main"], cwd=repo_path, check=True)
    subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "--allow-empty", "-m", "init"], cwd=repo_path, check=True)

    origin_path = tmp_path / "origin"
    origin_path.mkdir()
    subprocess.run(["git", "init", "--bare"], cwd=origin_path, check=True)
    subprocess.run(["git", "remote", "add", "origin", str(origin_path)], cwd=repo_path, check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=repo_path, check=True)
    return repo_path

def test_go_wrapper_missing_authority_fails(tmp_path):
    repo_path = setup_clean_repo(tmp_path)
    result = subprocess.run(
        [sys.executable, os.path.abspath("scripts/score2gp_go_bootstrap.py"), "--agentops", str(repo_path), "--product", str(repo_path)],
        capture_output=True, text=True
    )
    assert result.returncode != 0
    assert "Missing authority" in result.stderr

def test_got_wrapper_missing_authority_fails(tmp_path):
    repo_path = setup_clean_repo(tmp_path)
    result = subprocess.run(
        [sys.executable, os.path.abspath("scripts/score2gp_got_bootstrap.py"), "--agentops", str(repo_path), "--product", str(repo_path)],
        capture_output=True, text=True
    )
    assert result.returncode != 0
    assert "Missing authority" in result.stderr

def test_json_flag_output(tmp_path):
    repo_path = setup_clean_repo(tmp_path)
    result = subprocess.run(
        [sys.executable, os.path.abspath("scripts/score2gp_go_bootstrap.py"), "--agentops", str(repo_path), "--product", str(repo_path), "--json"],
        capture_output=True, text=True
    )
    assert result.returncode != 0
    assert "FAIL_CLOSED" in result.stdout

def test_legacy_bootstrap_compatibility_warning(tmp_path):
    repo_path = setup_clean_repo(tmp_path)
    result = subprocess.run(
        [sys.executable, os.path.abspath("scripts/score2gp_bootstrap.py"), "--agentops", str(repo_path), "--product", str(repo_path)],
        capture_output=True, text=True
    )
    assert result.returncode != 0
    assert "WARNING: score2gp_bootstrap.py is retired" in result.stderr
    assert "Missing authority" in result.stderr

def test_go_wrapper_dirty_repo_fails(tmp_path):
    repo_path = setup_clean_repo(tmp_path)
    (repo_path / "dirty.txt").write_text("dirty")
    subprocess.run(["git", "add", "dirty.txt"], cwd=repo_path, check=True)

    result = subprocess.run(
        [sys.executable, os.path.abspath("scripts/score2gp_go_bootstrap.py"), "--agentops", str(repo_path), "--product", str(repo_path)],
        capture_output=True, text=True
    )
    assert result.returncode != 0
    assert "is dirty" in result.stderr

def test_got_wrapper_dirty_repo_fails(tmp_path):
    repo_path = setup_clean_repo(tmp_path)
    (repo_path / "dirty.txt").write_text("dirty")
    subprocess.run(["git", "add", "dirty.txt"], cwd=repo_path, check=True)

    result = subprocess.run(
        [sys.executable, os.path.abspath("scripts/score2gp_got_bootstrap.py"), "--agentops", str(repo_path), "--product", str(repo_path)],
        capture_output=True, text=True
    )
    assert result.returncode != 0
    assert "is dirty" in result.stderr


@pytest.mark.parametrize("module", [score2gp_go_bootstrap, score2gp_got_bootstrap])
def test_bootstrap_switches_to_and_fast_forwards_main(monkeypatch, tmp_path, module):
    calls = []

    def run(command, **kwargs):
        calls.append(command)
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(module.subprocess, "run", run)
    module.sync_main(tmp_path, "agentops")

    assert calls == [
        ["git", "status", "--porcelain"],
        ["git", "fetch", "origin", "main"],
        ["git", "switch", "main"],
        ["git", "merge", "--ff-only", "origin/main"],
    ]


def test_terminal_task_does_not_snapshot_historical_pr() -> None:
    assert score2gp_go_bootstrap.should_snapshot_task_pr("COMPLETED") is False
    assert score2gp_go_bootstrap.should_snapshot_task_pr("PROMOTED") is True
    assert score2gp_got_bootstrap.should_snapshot_task_pr("MERGED", False) is False
    assert score2gp_got_bootstrap.should_snapshot_task_pr("MERGED", True) is True
