import unittest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app, get_db, User

class TestAuthAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

        # Base user for reusability
        self.existing_user = {"username": "ExistingUser", "password": "Strong@123"}
        self.client.post("/register", json=self.existing_user)

    def tearDown(self):
        # Called after each test method
        # Optional cleanup code can go here if needed
        # Get a DB session and remove all users that start with "TestUser"
        db: Session = next(get_db())
        db.query(User).filter(User.username.like("TestUser%")).delete(synchronize_session=False)
        db.commit()
        db.close()

    # 1. Valid registration
    def test_register_valid_user(self):
        response = self.client.post("/register", json={"username": "User1", "password": "Strong@123"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "User registered successfully!")

    # 2. Duplicate username
    def test_register_existing_user(self):
        response = self.client.post("/register", json=self.existing_user)
        self.assertEqual(response.status_code, 400)

    # 3. Invalid username (symbols)
    def test_register_invalid_username(self):
        response = self.client.post("/register", json={"username": "!!", "password": "Strong@123"})
        self.assertEqual(response.status_code, 422)

    # 4. Short username
    def test_register_short_username(self):
        response = self.client.post("/register", json={"username": "ab", "password": "Strong@123"})
        self.assertEqual(response.status_code, 422)

    # 5. Weak password (too short)
    def test_register_weak_password(self):
        response = self.client.post("/register", json={"username": "TestUser2", "password": "123"})
        self.assertEqual(response.status_code, 422)

    # 6. Missing password field
    def test_register_missing_password(self):
        response = self.client.post("/register", json={"username": "TestUser3"})
        self.assertEqual(response.status_code, 422)

    # 7. Missing username field
    def test_register_missing_username(self):
        response = self.client.post("/register", json={"password": "Strong@123"})
        self.assertEqual(response.status_code, 422)

    # 8. Valid login
    def test_login_valid_credentials(self):
        self.client.post("/register", json={"username": "TestUser4", "password": "Strong@123"})
        response = self.client.get("/login", params={"username": "TestUser4", "password": "Strong@123"})
        self.assertEqual(response.status_code, 200)

    # 9. Wrong password
    def test_login_invalid_password(self):
        self.client.post("/register", json={"username": "TestUser5", "password": "Strong@123"})
        response = self.client.get("/login", params={"username": "TestUser5", "password": "Wrong123"})
        self.assertEqual(response.status_code, 401)

    # 10. Missing username in login
    def test_login_missing_username(self):
        response = self.client.get("/login", params={"password": "Strong@123"})
        self.assertEqual(response.status_code, 400)

    # 11. Missing password in login
    def test_login_missing_password(self):
        response = self.client.get("/login", params={"username": "TestUser6"})
        self.assertEqual(response.status_code, 400)

    # 12. Non-existent user login
    def test_login_nonexistent_user(self):
        response = self.client.get("/login", params={"username": "GhostUser", "password": "Strong@123"})
        self.assertEqual(response.status_code, 404)

    # 13. Logout
    def test_logout(self):
        response = self.client.post("/logout")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Logout successful!")

    # 14. Password without uppercase
    def test_password_no_uppercase(self):
        response = self.client.post("/register", json={"username": "TestUser7", "password": "weak@123"})
        self.assertEqual(response.status_code, 422)

    # 15. Password without special character
    def test_password_no_special_char(self):
        response = self.client.post("/register", json={"username": "TestUser8", "password": "Strong123"})
        self.assertEqual(response.status_code, 422)

if __name__ == "__main__":
    unittest.main()
