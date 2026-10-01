import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

LEAN = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(LEAN / "scripts"))

import repo_scan  # noqa: E402


def make_repo(root: Path, files: dict[str, bytes]) -> Path:
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    for name, data in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True, capture_output=True)
    return root


def rules(repo, allow=(), max_bytes=1000, names=()):
    return {(p, r) for p, _, r in repo_scan.scan(repo, list(allow), max_bytes, list(names))}


class RepoScanTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_clean_repo(self):
        repo = make_repo(self.root, {"a.py": b"print('hi')\n"})
        self.assertEqual(rules(repo), set())
        self.assertEqual(repo_scan.main(["--repo", str(repo)]), 0)

    def test_forbidden_extension_and_allow_list(self):
        repo = make_repo(self.root, {"fixtures/x.PDF": b"%PDF", "docs/y.png": b"png"})
        self.assertEqual(rules(repo), {("fixtures/x.PDF", "forbidden-extension"), ("docs/y.png", "forbidden-extension")})
        self.assertEqual(rules(repo, allow=["docs/*.png", "fixtures/*"]), set())

    def test_too_large(self):
        repo = make_repo(self.root, {"big.txt": b"x" * 2000})
        self.assertEqual(rules(repo), {("big.txt", "too-large")})

    def test_secret_and_local_path_never_allow_listed(self):
        token = "gh" + "p_" + "A" * 36
        win = "C:" + "\\Users\\someone\\x"
        repo = make_repo(self.root, {"n.md": f"token {token}\nsee {win}\n/hom{"e"}/bob/x\n".encode()})
        found = repo_scan.scan(repo, ["*"], 1000, [])
        self.assertEqual({(r) for _, _, r in found}, {"secret", "local-path"})
        self.assertEqual([n for _, n, _ in found], [1, 2, 3])

    def test_private_key_header(self):
        header = "-----BEGIN " + "RSA PRIVATE KEY-----"
        repo = make_repo(self.root, {"k.txt": header.encode()})
        self.assertEqual(rules(repo), {("k.txt", "secret")})

    def test_private_names(self):
        repo = make_repo(self.root, {"d.md": b"we tested Back In Black today\n"})
        self.assertEqual(rules(repo, names=["Back In Black"]), {("d.md", "private-name")})
        self.assertEqual(rules(repo, names=["Other Song"]), set())

    def test_output_never_prints_matched_text(self):
        token = "gh" + "p_" + "B" * 36
        repo = make_repo(self.root, {"n.md": token.encode()})
        import contextlib
        import io

        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = repo_scan.main(["--repo", str(repo)])
        self.assertEqual(code, 1)
        self.assertNotIn(token, buffer.getvalue())
        self.assertIn("n.md:1: secret", buffer.getvalue())

    def test_scan_allow_file(self):
        repo = make_repo(self.root, {".scan-allow": b"# ok\nfixtures/public/*\n", "fixtures/public/a.png": b"p"})
        self.assertEqual(repo_scan.main(["--repo", str(repo)]), 0)

    def test_lean_files_in_this_checkout_are_clean(self):
        lean_repo = LEAN.parent
        own = [(p, r) for p, _, r in repo_scan.scan(lean_repo, [], 10_000_000, []) if p.startswith("lean/")]
        self.assertEqual(own, [])


if __name__ == "__main__":
    unittest.main()
