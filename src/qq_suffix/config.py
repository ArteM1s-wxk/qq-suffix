import json
from pathlib import Path

DEFAULT_SUFFIX = "音音"


def load_suffix(path: Path) -> str:
    if not path.exists():
        return DEFAULT_SUFFIX
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return DEFAULT_SUFFIX
    suffix = data.get("suffix")
    if isinstance(suffix, str) and suffix:
        return suffix
    return DEFAULT_SUFFIX


def save_suffix(path: Path, suffix: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"suffix": suffix}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
