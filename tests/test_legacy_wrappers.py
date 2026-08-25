import subprocess
import sys
import os

def test_go_wrapper_missing_authority_fails():
    result = subprocess.run(
        [sys.executable, "scripts/score2gp_go_bootstrap.py", "--agentops", "/tmp/nonexistent"],
        capture_output=True, text=True
    )
    assert result.returncode != 0
    assert "Missing authority" in result.stderr or "Failed to sync" in result.stderr

def test_got_wrapper_missing_authority_fails():
    result = subprocess.run(
        [sys.executable, "scripts/score2gp_got_bootstrap.py", "--agentops", "/tmp/nonexistent"],
        capture_output=True, text=True
    )
    assert result.returncode != 0
    assert "Missing authority" in result.stderr or "Failed to sync" in result.stderr

def test_json_flag_output():
    result = subprocess.run(
        [sys.executable, "scripts/score2gp_go_bootstrap.py", "--agentops", "/tmp/nonexistent", "--json"],
        capture_output=True, text=True
    )
    assert result.returncode != 0
    assert "FAIL_CLOSED" in result.stdout

def test_legacy_bootstrap_compatibility_warning():
    result = subprocess.run(
        [sys.executable, "scripts/score2gp_bootstrap.py", "--agentops", "/tmp/nonexistent"],
        capture_output=True, text=True
    )
    assert result.returncode != 0
    assert "WARNING: score2gp_bootstrap.py is retired" in result.stderr

def test_go_wrapper_dirty_repo_fails(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "--allow-empty", "-m", "init"], cwd=tmp_path, check=True)
    (tmp_path / "dirty.txt").write_text("dirty")
    subprocess.run(["git", "add", "dirty.txt"], cwd=tmp_path, check=True)
    
    result = subprocess.run(
        [sys.executable, os.path.abspath("scripts/score2gp_go_bootstrap.py"), "--agentops", str(tmp_path)],
        capture_output=True, text=True
    )
    assert result.returncode != 0
    assert "is dirty" in result.stderr
