"""Tests for the lean pre-push hook and its installer, against real git repos."""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

LEAN = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(LEAN / "scripts"))

import install_hooks  # noqa: E402

SH = shutil.which("sh")


def git(cwd, *args, env=None, check=True):
    return subprocess.run(
        ["git", "-C", str(cwd), *args],
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


def commit(repo: Path, name: str, text: str = "x"):
    (repo / name).write_text(text, encoding="utf-8")
    git(repo, "add", name)
    git(repo, "-c", "user.email=t@example.invalid", "-c", "user.name=t", "commit", "-q", "-m", name)


class Fixture:
    """A bare 'remote', a clone with the hook installed, and a second clone."""

    def __init__(self, root: Path):
        self.remote = root / "remote.git"
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(self.remote)], check=True)
        self.work = root / "work"
        subprocess.run(["git", "clone", "-q", str(self.remote), str(self.work)], check=True, capture_output=True)
        git(self.work, "checkout", "-q", "-b", "main")
        commit(self.work, "a.txt")
        # Seed the remote before the hook is installed.
        git(self.work, "push", "-q", "origin", "main")
        self.assert_ok(install_hooks.main(["--repo", str(self.work)]))

    @staticmethod
    def assert_ok(code):
        assert code == 0, code

    def push(self, *args, env=None):
        full = dict(os.environ, **(env or {}))
        return git(self.work, "push", *args, env=full, check=False)


@unittest.skipUnless(SH, "needs a POSIX sh (Git for Windows ships one)")
class PrePushHookTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.fx = Fixture(Path(self.tmp.name))

    def test_push_to_main_is_blocked(self):
        commit(self.fx.work, "b.txt")
        result = self.fx.push("origin", "main")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("protected branch 'main'", result.stderr)
        head = git(self.fx.remote, "rev-parse", "main").stdout.strip()
        self.assertNotEqual(head, git(self.fx.work, "rev-parse", "HEAD").stdout.strip())

    def test_push_head_to_remote_main_from_task_branch_is_blocked(self):
        git(self.fx.work, "checkout", "-q", "-b", "task/x")
        commit(self.fx.work, "b.txt")
        result = self.fx.push("origin", "HEAD:main")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("protected branch 'main'", result.stderr)

    def test_delete_main_is_blocked(self):
        result = self.fx.push("origin", "--delete", "main")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("delete protected branch", result.stderr)

    def test_task_branch_push_is_allowed(self):
        git(self.fx.work, "checkout", "-q", "-b", "task/x")
        commit(self.fx.work, "b.txt")
        result = self.fx.push("origin", "task/x")
        self.assertEqual(result.returncode, 0, result.stderr)
        git(self.fx.remote, "rev-parse", "task/x")

    def test_force_push_is_blocked_and_override_allows(self):
        git(self.fx.work, "checkout", "-q", "-b", "task/x")
        commit(self.fx.work, "b.txt", "1")
        self.assertEqual(self.fx.push("origin", "task/x").returncode, 0)
        git(self.fx.work, "reset", "-q", "--hard", "HEAD~1")
        commit(self.fx.work, "b.txt", "2")
        blocked = self.fx.push("--force", "origin", "task/x")
        self.assertNotEqual(blocked.returncode, 0)
        self.assertIn("non-fast-forward", blocked.stderr)
        allowed = self.fx.push("--force", "origin", "task/x", env={"LEAN_ALLOW_FORCE": "1"})
        self.assertEqual(allowed.returncode, 0, allowed.stderr)

    def test_maintainer_override_for_protected_push(self):
        commit(self.fx.work, "b.txt")
        result = self.fx.push("origin", "main", env={"LEAN_ALLOW_PROTECTED_PUSH": "1"})
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_no_verify_bypasses_the_hook(self):
        # Documented limitation: this is convention plus hook, not server enforcement.
        commit(self.fx.work, "b.txt")
        result = self.fx.push("--no-verify", "origin", "main")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_custom_protected_list(self):
        git(self.fx.work, "checkout", "-q", "-b", "release")
        commit(self.fx.work, "b.txt")
        result = self.fx.push("origin", "release", env={"LEAN_PROTECTED_BRANCHES": "release"})
        self.assertNotEqual(result.returncode, 0)


class InstallerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        self.hook = Path(install_hooks.hooks_dir(self.repo)) / "pre-push"

    def test_install_check_uninstall(self):
        self.assertEqual(install_hooks.main(["--repo", str(self.repo), "--check"]), 1)
        self.assertEqual(install_hooks.main(["--repo", str(self.repo)]), 0)
        self.assertTrue(self.hook.is_file())
        self.assertNotIn(b"\r", self.hook.read_bytes())
        self.assertEqual(install_hooks.main(["--repo", str(self.repo), "--check"]), 0)
        self.assertEqual(install_hooks.main(["--repo", str(self.repo)]), 0)  # idempotent
        self.assertEqual(install_hooks.main(["--repo", str(self.repo), "--uninstall"]), 0)
        self.assertFalse(self.hook.exists())

    def test_refuses_to_overwrite_foreign_hook_unless_forced(self):
        self.hook.parent.mkdir(parents=True, exist_ok=True)
        self.hook.write_text("#!/bin/sh\necho mine\n", encoding="utf-8")
        self.assertEqual(install_hooks.main(["--repo", str(self.repo)]), 1)
        self.assertIn("mine", self.hook.read_text(encoding="utf-8"))
        self.assertEqual(install_hooks.main(["--repo", str(self.repo), "--force"]), 0)
        self.assertTrue(self.hook.with_name("pre-push.bak").is_file())
        # Uninstall restores the previous hook.
        self.assertEqual(install_hooks.main(["--repo", str(self.repo), "--uninstall"]), 0)
        self.assertIn("mine", self.hook.read_text(encoding="utf-8"))

    def test_uninstall_leaves_a_foreign_hook(self):
        self.hook.parent.mkdir(parents=True, exist_ok=True)
        self.hook.write_text("#!/bin/sh\necho mine\n", encoding="utf-8")
        self.assertEqual(install_hooks.main(["--repo", str(self.repo), "--uninstall"]), 1)
        self.assertTrue(self.hook.exists())

    def test_core_hookspath_is_reported_not_silently_ignored(self):
        git(self.repo, "config", "core.hooksPath", "elsewhere")
        self.assertEqual(install_hooks.main(["--repo", str(self.repo)]), 1)
        self.assertEqual(install_hooks.main(["--repo", str(self.repo), "--check"]), 1)

    def test_not_a_repository(self):
        with tempfile.TemporaryDirectory() as plain:
            with self.assertRaises(SystemExit):
                install_hooks.main(["--repo", plain])

    def test_linked_worktree_shares_the_hook(self):
        commit(self.repo, "a.txt")
        git(self.repo, "worktree", "add", "-q", str(self.repo.parent / (self.repo.name + "-wt")), "-b", "w")
        self.addCleanup(shutil.rmtree, str(self.repo.parent / (self.repo.name + "-wt")), True)
        self.assertEqual(install_hooks.main(["--repo", str(self.repo)]), 0)
        wt = self.repo.parent / (self.repo.name + "-wt")
        self.assertEqual(install_hooks.main(["--repo", str(wt), "--check"]), 0)


if __name__ == "__main__":
    unittest.main()
