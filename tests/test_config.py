from qq_suffix.config import DEFAULT_SUFFIX, load_suffix, save_suffix


def test_load_suffix_returns_default_when_missing(tmp_path):
    assert load_suffix(tmp_path / "config.json") == DEFAULT_SUFFIX


def test_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "config.json"
    save_suffix(path, "你好")
    assert load_suffix(path) == "你好"


def test_load_suffix_returns_default_on_invalid_json(tmp_path):
    path = tmp_path / "config.json"
    path.write_text("{not json", encoding="utf-8")
    assert load_suffix(path) == DEFAULT_SUFFIX


def test_load_suffix_returns_default_on_empty_string(tmp_path):
    path = tmp_path / "config.json"
    save_suffix(path, "")
    assert load_suffix(path) == DEFAULT_SUFFIX
