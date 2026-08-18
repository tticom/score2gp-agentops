import unittest
from scripts.pr_body import summarize_report

class TestPrBody(unittest.TestCase):
    def test_summarize_report(self):
        raw_text = """# Verification Report /some/secret/path/to/hide.txt
Some raw log output: /private/path/to/my_secret_file.pdf
PASS: Test 1 /home/tticom/workspace/repo/file.py:12
FAIL: Test 2 /opt/app/bin/start
WARNING: Something might be wrong /var/log/syslog
More raw logs with stderr output...
"""
        sanitized = summarize_report(raw_text)
        self.assertIn("Sanitized Verification Report", sanitized)
        self.assertIn("# Verification Report [REDACTED]", sanitized)
        self.assertIn("PASS: Test 1 [REDACTED]:12", sanitized)
        self.assertIn("FAIL: Test 2 [REDACTED]", sanitized)
        self.assertIn("WARNING: Something might be wrong [REDACTED]", sanitized)
        self.assertNotIn("/private/path", sanitized)
        self.assertNotIn("/some/secret/path", sanitized)
        self.assertNotIn("/home/tticom", sanitized)
        self.assertNotIn("/opt/app", sanitized)
        self.assertNotIn("/var/log", sanitized)
        self.assertNotIn("stderr output", sanitized)
