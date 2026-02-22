import os
import sys
import unittest
from importlib import reload

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

class TestFQDN(unittest.TestCase):
    def setUp(self):
        # Set dummy required vars
        os.environ["API_ID"] = "123"
        os.environ["API_HASH"] = "abc"
        os.environ["BOT_TOKEN"] = "token"
        os.environ["BIN_CHANNEL"] = "-100"
        os.environ["DATABASE_URL"] = "mongo"

    def test_fqdn_stripping(self):
        from WebStreamer import vars

        # Case 1: FQDN with https://
        os.environ["FQDN"] = "https://myapp.koyeb.app"
        reload(vars)
        self.assertEqual(vars.Var.FQDN, "myapp.koyeb.app")
        # URL should not have double scheme. Assuming HAS_SSL defaults to False in tests unless set.
        # If HAS_SSL is false -> http://myapp.koyeb.app...
        self.assertTrue(vars.Var.URL.startswith("http"))
        self.assertFalse(vars.Var.URL.startswith("https://https://"))

        # Case 2: FQDN with http://
        os.environ["FQDN"] = "http://myapp.koyeb.app"
        reload(vars)
        self.assertEqual(vars.Var.FQDN, "myapp.koyeb.app")

        # Case 3: FQDN with trailing slash
        os.environ["FQDN"] = "myapp.koyeb.app/"
        reload(vars)
        self.assertEqual(vars.Var.FQDN, "myapp.koyeb.app")

        # Case 4: Clean FQDN
        os.environ["FQDN"] = "myapp.koyeb.app"
        reload(vars)
        self.assertEqual(vars.Var.FQDN, "myapp.koyeb.app")

    def test_fqdn_default(self):
        from WebStreamer import vars
        # Case 5: No FQDN set
        if "FQDN" in os.environ:
            del os.environ["FQDN"]
        # Ensure BIND_ADDRESS is default (0.0.0.0)
        if "WEB_SERVER_BIND_ADDRESS" in os.environ:
             del os.environ["WEB_SERVER_BIND_ADDRESS"]

        reload(vars)
        self.assertEqual(vars.Var.FQDN, "localhost")


if __name__ == '__main__':
    unittest.main()
