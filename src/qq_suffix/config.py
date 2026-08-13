import json
import os
import tempfile
from pathlib import Path

DEFAULT_SUFFIX = "音音"


def load_suffix(path: Path) -> str:
    if not path.exists():
        return DEFAULT_SUFFIX
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return DEFAULT_SUFFIX
    if not isinstance(data, dict):
        return DEFAULT_SUFFIX
    suffix = data.get("suffix")
    if isinstance(suffix, str) and suffix:
        return suffix
    return DEFAULT_SUFFIX


def save_suffix(path: Path, suffix: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps({"suffix": suffix}, ensure_ascii=False, indent=2)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp, path)
    except Exception:
        os.unlink(tmp)
        raise
