from qq_suffix.window import is_qq_process


def test_is_qq_process_matches_case_insensitively():
    assert is_qq_process("QQ.exe") is True
    assert is_qq_process("qq.exe") is True
    assert is_qq_process("Qq.Exe") is True


def test_is_qq_process_returns_false_for_others():
    assert is_qq_process("chrome.exe") is False
    assert is_qq_process("") is False
