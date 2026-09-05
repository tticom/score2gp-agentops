"""Keep real executable test doubles off hardened noexec temporary mounts."""
import os
from pathlib import Path
import tempfile

import pytest


def pytest_configure(config):
    if config.option.basetemp:
        # An explicit test location is the caller's responsibility.
        return
    if not os.statvfs(tempfile.gettempdir()).f_flag & os.ST_NOEXEC:
        return
    root = Path(config.rootpath) / "work" / "test-tmp"
    root.mkdir(parents=True, exist_ok=True)
    if os.statvfs(root).f_flag & os.ST_NOEXEC:
        raise pytest.UsageError("Runtime tests require an executable --basetemp or TMPDIR location")
    config.option.basetemp = tempfile.mkdtemp(prefix="pytest-", dir=root)
