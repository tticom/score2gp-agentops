import unittest
from scripts.pr_body import summarize_report, redact_sensitive_data
import scripts.pr_body
from unittest.mock import patch
import subprocess
import io
import sys

class TestPrBody(unittest.TestCase):
    def test_summarize_report_emits_only_status_counts(self):
        raw_text = """PASS: Cookie: session_id=super-secret
FAIL: Authorization: Bearer token-value
WARNING: /private/Lesson-5.pdf
# heading containing private@example.test
"""

        sanitized = summarize_report(raw_text)

        self.assertIn("PASS: 1 reported", sanitized)
        self.assertIn("FAIL: 1 reported", sanitized)
        self.assertIn("WARNING: 1 reported", sanitized)

        self.assertNotIn("super-secret", sanitized)
        self.assertNotIn("token-value", sanitized)
        self.assertNotIn("/private/", sanitized)
        self.assertNotIn("private@example.test", sanitized)
        self.assertNotIn("Cookie:", sanitized)
        self.assertNotIn("Authorization:", sanitized)

    @patch("scripts.pr_body.run_cmd")
    @patch("scripts.pr_body.subprocess.run")
    def test_audit_failure_omits_raw_output(self, mock_run, mock_run_cmd):
        # Mock git commands to not fail
        mock_run_cmd.return_value = "file.txt"
        
        mock_run.side_effect = lambda cmd, **kwargs: subprocess.CompletedProcess(
            args=cmd, 
            returncode=1 if "scripts/artifact_audit.py" in cmd else 0, 
            stdout="Fake audit stdout with /private/Lesson-5.pdf and token=secret123",
            stderr="Fake audit stderr"
        )
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            with patch('sys.argv', ['pr_body.py']):
                scripts.pr_body.main()
        finally:
            sys.stdout = sys.__stdout__
            
        body = captured_output.getvalue()
        
        self.assertNotIn("Fake audit stdout", body)
        self.assertNotIn("/private/", body)
        self.assertNotIn("secret123", body)
        self.assertIn("Raw audit output is intentionally omitted; inspect it only in the local workspace.", body)


    @patch("scripts.pr_body.run_cmd")
    @patch("scripts.pr_body.subprocess.run")
    @patch("scripts.pr_body.os.path.exists")
    @patch("builtins.open")
    def test_oserror_omits_raw_exception(self, mock_open, mock_exists, mock_run, mock_run_cmd):
        mock_run_cmd.return_value = "file.txt"
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        mock_exists.return_value = True
        mock_open.side_effect = OSError("Secret permission denied: /private/keys")
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            with patch('sys.argv', ['pr_body.py']):
                scripts.pr_body.main()
        finally:
            sys.stdout = sys.__stdout__
            
        body = captured_output.getvalue()
        
        self.assertNotIn("Secret permission denied", body)
        self.assertNotIn("/private/keys", body)
        self.assertIn("Error reading verification report: I/O error occurred.", body)


    def test_summarize_report_avoids_false_positives(self):
        raw_text = """COMPASS: this should not count
FAILING: this should count as FAIL? No, FAIL: or FAIL 
# heading
"""
        sanitized = scripts.pr_body.summarize_report(raw_text)
        self.assertNotIn("PASS", sanitized)
        self.assertNotIn("FAIL", sanitized)


    def test_summarize_report_parses_real_report_format(self):
        raw_text = """# Score2GP Verification Report

**Overall Status**: 🔴 FAIL
**Timestamp**: 2026-08-19 05:59:19

| Verification Step | Status | Exit Code | Time |
| :--- | :--- | :--- | :--- |
| Run pytest | 🟢 PASS | 0 | 51.81s |
| Export schemas | 🟢 PASS | 0 | 0.33s |
| Validate IR on tiny_score | 🟢 PASS | 0 | 0.26s |
| Artifact audit | 🟢 PASS | 0 | 0.04s |
| Git PR range check diff | 🔴 FAIL | 2 | 0.01s |
| Random step | 🟡 WARNING | 0 | 0.01s |

## Step Details
- **Status**: PASS
"""
        sanitized = scripts.pr_body.summarize_report(raw_text)
        self.assertIn("PASS: 4 reported", sanitized)
        self.assertIn("FAIL: 1 reported", sanitized)
        self.assertIn("WARNING: 1 reported", sanitized)

if __name__ == "__main__":
    unittest.main()
