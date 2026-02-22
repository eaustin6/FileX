import unittest
from unittest.mock import patch
import sys
import os

# Mock environment variables before importing anything that might use them
os.environ["API_ID"] = "12345"
os.environ["API_HASH"] = "abcdef123456"
os.environ["BOT_TOKEN"] = "123456789:abcdefghijklmnopqrstuvwxyz"
os.environ["BIN_CHANNEL"] = "-1001234567890"

# Add current dir to sys.path
sys.path.append(os.getcwd())

# We need to import WebStreamer to make sure modules are loaded
# But permissions.py imports Var which reads env vars.
# We mocked env vars above, so it should be fine.

from WebStreamer.utils.permissions import is_user_locked, is_user_banned

class TestPermissions(unittest.TestCase):

    @patch('WebStreamer.utils.permissions.Var')
    @patch('WebStreamer.utils.permissions.authorized_users', new_callable=set)
    def test_lock_mode_off(self, mock_authorized_users, mock_var):
        mock_var.LOCK_MODE = False
        mock_var.ALLOWED_USERS = []

        # Lock mode off -> always allowed (returns False for is_locked)
        self.assertFalse(is_user_locked(12345, "user"))

    @patch('WebStreamer.utils.permissions.Var')
    @patch('WebStreamer.utils.permissions.authorized_users', new_callable=set)
    def test_lock_mode_on_not_authorized(self, mock_authorized_users, mock_var):
        mock_var.LOCK_MODE = True
        mock_var.ALLOWED_USERS = []
        # Not in authorized_users

        self.assertTrue(is_user_locked(12345, "user"))

    @patch('WebStreamer.utils.permissions.Var')
    @patch('WebStreamer.utils.permissions.authorized_users', new_callable=set)
    def test_lock_mode_on_authorized(self, mock_authorized_users, mock_var):
        mock_var.LOCK_MODE = True
        mock_var.ALLOWED_USERS = []
        mock_authorized_users.add(12345)

        self.assertFalse(is_user_locked(12345, "user"))

    @patch('WebStreamer.utils.permissions.Var')
    @patch('WebStreamer.utils.permissions.authorized_users', new_callable=set)
    def test_lock_mode_on_in_allowed_users(self, mock_authorized_users, mock_var):
        mock_var.LOCK_MODE = True
        mock_var.ALLOWED_USERS = ["12345"]

        self.assertFalse(is_user_locked(12345, "user"))

        mock_var.ALLOWED_USERS = ["user"]
        self.assertFalse(is_user_locked(67890, "user"))

    @patch('WebStreamer.utils.permissions.Var')
    def test_banned_no_allowed_users(self, mock_var):
        mock_var.ALLOWED_USERS = []

        # No allowed users set -> everyone allowed (returns False for is_banned)
        self.assertFalse(is_user_banned(12345, "user"))

    @patch('WebStreamer.utils.permissions.Var')
    def test_banned_with_allowed_users(self, mock_var):
        mock_var.ALLOWED_USERS = ["12345", "admin"]

        # User in ID list -> not banned
        self.assertFalse(is_user_banned(12345, "user"))

        # User in Username list -> not banned
        self.assertFalse(is_user_banned(67890, "admin"))

        # User NOT in list -> banned
        self.assertTrue(is_user_banned(99999, "guest"))

    @patch('WebStreamer.utils.permissions.Var')
    def test_banned_with_none_username(self, mock_var):
        mock_var.ALLOWED_USERS = ["12345"]

        # User not in list, no username -> banned
        self.assertTrue(is_user_banned(99999, None))

        # User in list by ID, no username -> not banned
        self.assertFalse(is_user_banned(12345, None))

if __name__ == '__main__':
    unittest.main()
