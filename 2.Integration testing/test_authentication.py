import unittest
from auth_service import AuthService

class TestAuthenticationIntegration(unittest.TestCase):
    def setUp(self):
        """Set up authentication service before each test."""
        self.auth_service = AuthService()

    def test_valid_credentials(self):
        """Testing with correct username and password."""
        self.assertEqual(self.auth_service.authenticate("admin", "password123"), "Access Granted")

    def test_invalid_credentials(self):
        """Testing with incorrect password."""
        self.assertEqual(self.auth_service.authenticate("admin", "wrongpass"), "Access Denied")

    def test_non_existent_user(self):
        """Testing with a username that doesn't exist."""
        self.assertEqual(self.auth_service.authenticate("unknown_user", "securepass"), "Access Denied")

if __name__ == "__main__":
    unittest.main()
