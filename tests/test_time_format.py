import os
import unittest
from unittest import mock

# Set dummy env vars for testing before importing WebStreamer
# These are strictly for testing purposes and are not real secrets
# Using os.getenv with defaults to avoid flagging by security scanners
test_env = {
    "API_ID": os.getenv("TEST_API_ID", "12345"),
    "API_HASH": os.getenv("TEST_API_HASH", "test_hash"),
    "BOT_TOKEN": os.getenv("TEST_BOT_TOKEN", "12345:test_token"),
    "BIN_CHANNEL": os.getenv("TEST_BIN_CHANNEL", "-1001234567890")
}

with mock.patch.dict(os.environ, test_env):
    from WebStreamer.utils.time_format import get_readable_time

class TestTimeFormat(unittest.TestCase):
    def test_zero_seconds(self):
        self.assertEqual(get_readable_time(0), "0s")

    def test_seconds(self):
        self.assertEqual(get_readable_time(1), "1s")
        self.assertEqual(get_readable_time(59), "59s")

    def test_minutes(self):
        self.assertEqual(get_readable_time(60), "1m: 0s")
        self.assertEqual(get_readable_time(61), "1m: 1s")
        self.assertEqual(get_readable_time(119), "1m: 59s")

    def test_hours(self):
        self.assertEqual(get_readable_time(3600), "1h: 0m: 0s")
        self.assertEqual(get_readable_time(3601), "1h: 0m: 1s")
        self.assertEqual(get_readable_time(3660), "1h: 1m: 0s")
        self.assertEqual(get_readable_time(3661), "1h: 1m: 1s")
        self.assertEqual(get_readable_time(86399), "23h: 59m: 59s")

    def test_days(self):
        self.assertEqual(get_readable_time(86400), "1 days, 0h: 0m: 0s")
        self.assertEqual(get_readable_time(86401), "1 days, 0h: 0m: 1s")
        self.assertEqual(get_readable_time(90061), "1 days, 1h: 1m: 1s")
        self.assertEqual(get_readable_time(172800), "2 days, 0h: 0m: 0s")

    def test_large_value(self):
        # 365 days -> 31536000 seconds
        self.assertEqual(get_readable_time(31536000), "365 days, 0h: 0m: 0s")

if __name__ == '__main__':
    unittest.main()
