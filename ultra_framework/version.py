"""version module"""
from pathlib import Path

__version__ = Path("VERSION").read_text(encoding="utf-8")

