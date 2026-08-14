from qq_suffix.config import DEFAULT_NEWLINE, DEFAULT_SUFFIX, load_config, save_config


def test_load_config_returns_defaults_when_missing(tmp_path):
    config = load_config(tmp_path / "config.json")
    assert config.suffix == DEFAULT_SUFFIX
    assert config.newline == DEFAULT_NEWLINE


def test_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "config.json"
    save_config(path, "你好", False)
    config = load_config(path)
    assert config.suffix == "你好"
    assert config.newline is False


def test_load_config_returns_defaults_on_invalid_json(tmp_path):
    path = tmp_path / "config.json"
    path.write_text("{not json", encoding="utf-8")
    config = load_config(path)
    assert config.suffix == DEFAULT_SUFFIX
    assert config.newline == DEFAULT_NEWLINE


def test_load_config_returns_default_on_empty_suffix(tmp_path):
    path = tmp_path / "config.json"
    save_config(path, "", True)
    config = load_config(path)
    assert config.suffix == DEFAULT_SUFFIX
    assert config.newline is True


def test_load_config_returns_defaults_on_non_object_json(tmp_path):
    path = tmp_path / "config.json"
    path.write_text("[1, 2]", encoding="utf-8")
    config = load_config(path)
    assert config.suffix == DEFAULT_SUFFIX
    assert config.newline == DEFAULT_NEWLINE


def test_load_config_falls_back_newline_on_non_bool(tmp_path):
    path = tmp_path / "config.json"
    path.write_text('{"suffix": "x", "newline": "yes"}', encoding="utf-8")
    config = load_config(path)
    assert config.suffix == "x"
    assert config.newline == DEFAULT_NEWLINE
