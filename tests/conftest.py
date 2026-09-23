"""Keep real executable test doubles off hardened noexec temporary mounts."""
import os
from pathlib import Path
import tempfile

import pytest


def is_noexec(path) -> bool:
    """Return whether ``path`` is on a noexec mount; Windows has no such flag."""
    statvfs = getattr(os, "statvfs", None)
    if statvfs is None:
        return False
    return bool(statvfs(path).f_flag & os.ST_NOEXEC)


def pytest_configure(config):
    if config.option.basetemp:
        # An explicit test location is the caller's responsibility.
        return
    if not is_noexec(tempfile.gettempdir()):
        return
    root = Path(config.rootpath) / "work" / "test-tmp"
    root.mkdir(parents=True, exist_ok=True)
    if is_noexec(root):
        raise pytest.UsageError("Runtime tests require an executable --basetemp or TMPDIR location")
    config.option.basetemp = tempfile.mkdtemp(prefix="pytest-", dir=root)
