import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path

DEFAULT_SUFFIX = "音音"
DEFAULT_NEWLINE = True


@dataclass
class Config:
    suffix: str = DEFAULT_SUFFIX
    newline: bool = DEFAULT_NEWLINE


def load_config(path: Path) -> Config:
    if not path.exists():
        return Config()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return Config()
    if not isinstance(data, dict):
        return Config()
    suffix = data.get("suffix")
    newline = data.get("newline", DEFAULT_NEWLINE)
    return Config(
        suffix=suffix if isinstance(suffix, str) and suffix else DEFAULT_SUFFIX,
        newline=newline if isinstance(newline, bool) else DEFAULT_NEWLINE,
    )


def save_config(path: Path, suffix: str, newline: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(
        {"suffix": suffix, "newline": newline},
        ensure_ascii=False,
        indent=2,
    )
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp, path)
    except Exception:
        os.unlink(tmp)
        raise
