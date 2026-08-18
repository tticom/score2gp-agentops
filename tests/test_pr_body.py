import unittest
from scripts.pr_body import summarize_report

class TestPrBody(unittest.TestCase):
    def test_summarize_report(self):
        raw_text = """# Verification Report
Some raw log output: /private/path/to/my_secret_file.pdf
PASS: Test 1
FAIL: Test 2
WARNING: Something might be wrong
More raw logs with stderr output...
"""
        sanitized = summarize_report(raw_text)
        self.assertIn("Sanitized Verification Report", sanitized)
        self.assertIn("PASS: Test 1", sanitized)
        self.assertIn("FAIL: Test 2", sanitized)
        self.assertIn("WARNING: Something might be wrong", sanitized)
        self.assertNotIn("/private/path", sanitized)
        self.assertNotIn("stderr output", sanitized)
