"""The guidance must only name lean/ paths that exist, so promotion does not break it."""

import re
import unittest
from pathlib import Path

LEAN = Path(__file__).resolve().parent.parent
ROOT = LEAN.parent


class GuidancePathsTest(unittest.TestCase):
    def test_lean_paths_named_in_guidance_exist(self):
        for doc in ("CLAUDE.md", "AGENTS.md", "README.md", "TASKS.md"):
            text = (LEAN / doc).read_text(encoding="utf-8")
            for match in re.findall(r"`(lean/[A-Za-z0-9_./-]+)`", text):
                path = ROOT / match.rstrip("/.")
                self.assertTrue(path.exists(), f"{doc} names missing path {match}")

    def test_cutover_names_existing_lean_files(self):
        text = (ROOT / "MIGRATION.md").read_text(encoding="utf-8")
        for match in re.findall(r"`(lean/[A-Za-z0-9_./-]+)`", text):
            if match.startswith("lean/skills"):
                continue  # lives in the skills repository
            self.assertTrue((ROOT / match.rstrip("/.")).exists(), f"MIGRATION.md names missing path {match}")


if __name__ == "__main__":
    unittest.main()
