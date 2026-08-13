from qq_suffix.listener import should_append


def test_should_append_only_when_enabled_and_qq():
    assert should_append(True, True) is True
    assert should_append(False, True) is False
    assert should_append(True, False) is False
    assert should_append(False, False) is False
