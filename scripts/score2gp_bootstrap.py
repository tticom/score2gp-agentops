#!/usr/bin/env python3
"""Compatibility wrapper for retired score2gp_bootstrap.py"""
import sys
import subprocess
import argparse

def main():
    print("WARNING: score2gp_bootstrap.py is retired. Redirecting to score2gp_got_bootstrap.py.", file=sys.stderr)
    cmd = [sys.executable, "scripts/score2gp_got_bootstrap.py"] + sys.argv[1:]
    res = subprocess.run(cmd)
    sys.exit(res.returncode)

if __name__ == "__main__":
    main()
