import os
import unittest
from importlib import reload

class TestAllowedUsers(unittest.TestCase):
    def test_allowed_users_parsing(self):
        # Setup env
        os.environ["ALLOWED_USERS"] = "user1, @user2, user1,  user3 "
        # Mock other required vars to avoid exit
        os.environ["API_ID"] = "123"
        os.environ["API_HASH"] = "abc"
        os.environ["BOT_TOKEN"] = "token"
        os.environ["BIN_CHANNEL"] = "-100"

        from WebStreamer import vars
        reload(vars)

        # Verify membership
        self.assertIn("user1", vars.Var.ALLOWED_USERS)
        self.assertIn("user2", vars.Var.ALLOWED_USERS)
        self.assertIn("user3", vars.Var.ALLOWED_USERS)

        # Check that it strips characters correctly
        self.assertNotIn("@user2", vars.Var.ALLOWED_USERS) # It should be stripped to user2

    def test_allowed_users_empty(self):
        os.environ["ALLOWED_USERS"] = ""
        os.environ["API_ID"] = "123"
        os.environ["API_HASH"] = "abc"
        os.environ["BOT_TOKEN"] = "token"
        os.environ["BIN_CHANNEL"] = "-100"

        from WebStreamer import vars
        reload(vars)

        # Should be empty
        self.assertEqual(len(vars.Var.ALLOWED_USERS), 0)

if __name__ == '__main__':
    unittest.main()
