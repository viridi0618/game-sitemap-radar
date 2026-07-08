from pathlib import Path

_src_pkg = Path(__file__).resolve().parents[1] / "src" / "radar"
__path__ = [str(_src_pkg)]

