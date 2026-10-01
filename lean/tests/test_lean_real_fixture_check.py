"""Tests for the local real-fixture check using a tiny fake product repository."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

LEAN = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(LEAN / "scripts"))

import real_fixture_check as rfc  # noqa: E402


def git(repo, *args):
    subprocess.run(
        ["git", "-C", str(repo), "-c", "user.email=t@example.invalid", "-c", "user.name=t", *args],
        check=True,
        capture_output=True,
    )


def make_product(root: Path, fixtures: int = 1) -> Path:
    product = root / "product"
    (product / "fixtures" / "private").mkdir(parents=True)
    (product / "fixtures" / "private" / ".gitkeep").write_text("", encoding="utf-8")
    for i in range(fixtures):
        (product / "fixtures" / "private" / f"s{i}.pdf").write_bytes(b"%PDF-private")
    (product / ".gitignore").write_text("fixtures/private/*.pdf\n", encoding="utf-8")
    git(product, "init", "-q")
    git(product, "add", ".gitignore", "fixtures/private/.gitkeep")
    git(product, "commit", "-q", "-m", "init")
    return product


def config(*steps, min_fixtures=1):
    return {"fixture_dir": "fixtures/private", "fixture_glob": "*.pdf", "min_fixtures": min_fixtures, "steps": list(steps)}


def cmd(name, code, kind="command", required=True):
    return {"name": name, "kind": kind, "required": required, "argv": ["{python}", "-c", code]}


class RealFixtureCheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.logs = self.root / "logs"
        self.logs.mkdir()

    def run_check(self, product, cfg, **kw):
        return rfc.run(product, cfg, sys.executable, self.logs, kw.get("fail_on_skips", False), kw.get("require_clean", False))

    def test_pass(self):
        product = make_product(self.root)
        out = self.run_check(product, config(cmd("ok", "print('SECRET' + '-PATH')")))
        self.assertEqual(out["result"], rfc.PASS)
        self.assertNotIn("SECRET-PATH", json.dumps(out), "raw output must never reach the summary")
        self.assertIn("SECRET-PATH", (self.logs / "ok.log").read_text(encoding="utf-8"))

    def test_failing_required_step_fails(self):
        product = make_product(self.root)
        out = self.run_check(product, config(cmd("bad", "import sys; sys.exit(3)")))
        self.assertEqual(out["result"], rfc.FAIL)
        self.assertEqual(out["steps"][0]["exit_code"], 3)

    def test_missing_fixtures_is_not_evaluated_never_pass(self):
        product = make_product(self.root, fixtures=0)
        out = self.run_check(product, config(cmd("ok", "pass")))
        self.assertEqual(out["result"], rfc.NOT_EVALUATED)
        self.assertEqual(rfc.EXIT[out["result"]], 2)

    def test_pytest_counts_and_skips(self):
        product = make_product(self.root)
        fake = "print('1 failed, 4 passed, 2 skipped in 0.1s')"
        step = cmd("t", fake, kind="pytest")
        out = self.run_check(product, config(step))
        self.assertEqual(out["steps"][0]["counts"], {"failed": 1, "passed": 4, "skipped": 2})
        self.assertEqual(out["result"], rfc.PASS)  # exit code 0 here; count parsing is separate
        skip_only = cmd("t", "print('5 passed, 2 skipped in 0.1s')", kind="pytest")
        self.assertEqual(self.run_check(product, config(skip_only), fail_on_skips=True)["result"], rfc.FAIL)
        self.assertEqual(self.run_check(product, config(skip_only))["result"], rfc.PASS)

    def test_pytest_without_summary_or_zero_passed_is_not_evaluated(self):
        product = make_product(self.root)
        self.assertEqual(self.run_check(product, config(cmd("t", "print('hello')", kind="pytest")))["result"], rfc.NOT_EVALUATED)
        zero = cmd("t", "print('2 skipped in 0.1s')", kind="pytest")
        self.assertEqual(self.run_check(product, config(zero))["result"], rfc.NOT_EVALUATED)

    def test_tracked_private_file_fails_invariant(self):
        product = make_product(self.root)
        step = {"name": "inv", "kind": "tracked-files", "paths": ["fixtures/private"], "allowed": ["fixtures/private/.gitkeep"], "required": True}
        self.assertEqual(self.run_check(product, config(step))["result"], rfc.PASS)
        git(product, "add", "-f", "fixtures/private/s0.pdf")
        out = self.run_check(product, config(step))
        self.assertEqual(out["result"], rfc.FAIL)
        self.assertEqual(out["steps"][0]["tracked_unexpected"], 1)

    def test_unstartable_required_step_is_not_evaluated(self):
        product = make_product(self.root)
        step = {"name": "x", "kind": "command", "required": True, "argv": ["definitely-not-a-program-xyz"]}
        self.assertEqual(self.run_check(product, config(step))["result"], rfc.NOT_EVALUATED)

    def test_optional_step_failure_does_not_fail(self):
        product = make_product(self.root)
        out = self.run_check(product, config(cmd("ok", "pass"), cmd("opt", "import sys; sys.exit(1)", required=False)))
        self.assertEqual(out["result"], rfc.PASS)

    def test_require_clean(self):
        product = make_product(self.root)
        (product / ".gitignore").write_text("changed\n", encoding="utf-8")
        out = self.run_check(product, config(cmd("ok", "pass")), require_clean=True)
        self.assertEqual(out["result"], rfc.FAIL)

    def test_cli_refuses_log_dir_inside_product_and_non_repo(self):
        product = make_product(self.root)
        self.assertEqual(rfc.main(["--product", str(product), "--log-dir", str(product / "logs")]), 64)
        self.assertEqual(rfc.main(["--product", str(self.root)]), 64)

    def test_cli_end_to_end_exit_codes(self):
        product = make_product(self.root)
        cfg = self.root / "c.json"
        cfg.write_text(json.dumps(config(cmd("ok", "pass"))), encoding="utf-8")
        self.assertEqual(rfc.main(["--product", str(product), "--config", str(cfg), "--log-dir", str(self.logs), "--python", sys.executable]), 0)
        cfg.write_text(json.dumps(config(cmd("bad", "raise SystemExit(1)"))), encoding="utf-8")
        self.assertEqual(rfc.main(["--product", str(product), "--config", str(cfg), "--log-dir", str(self.logs), "--python", sys.executable]), 1)

    def test_parse_pytest_counts(self):
        self.assertEqual(rfc.parse_pytest_counts("x\n=== 3 passed, 1 warning in 1s ==="), {"passed": 3})
        self.assertEqual(rfc.parse_pytest_counts("2 errors in 1s"), {"errors": 2})
        self.assertEqual(rfc.parse_pytest_counts("nothing"), {})


if __name__ == "__main__":
    unittest.main()
