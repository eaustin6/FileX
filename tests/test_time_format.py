import pytest
from WebStreamer.utils.time_format import get_readable_time

@pytest.mark.parametrize("seconds, expected", [
    (0, ""),
    (1, "1s"),
    (59, "59s"),
    (60, "1m: 0s"),
    (61, "1m: 1s"),
    (3599, "59m: 59s"),
    (3600, "1h: 0m: 0s"),
    (3661, "1h: 1m: 1s"),
    (86399, "23h: 59m: 59s"),
    (86400, "1 days, 0h: 0m: 0s"),
    (90061, "1 days, 1h: 1m: 1s"),
    (172800, "2 days, 0h: 0m: 0s"),
])
def test_get_readable_time(seconds, expected):
    """Test get_readable_time with various inputs."""
    assert get_readable_time(seconds) == expected
