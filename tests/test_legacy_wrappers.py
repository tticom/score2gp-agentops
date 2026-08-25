import subprocess
import sys

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
