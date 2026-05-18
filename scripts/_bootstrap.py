"""Bootstrap helpers for runner scripts."""

from __future__ import annotations

import sys
from pathlib import Path


def bootstrap() -> Path:
    """Ensure the src directory is importable and return the repo root."""
    repo_root = Path(__file__).resolve().parents[1]
    src_dir = repo_root / "src"
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))
    return repo_root
