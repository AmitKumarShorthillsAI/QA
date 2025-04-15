import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestFastAPIAuth(unittest.TestCase):

    def test_register_valid_user(self):
        response = client.post("/register", json={"username": "TestUser1", "password": "Strong@123"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "User registered successfully!"})

    def test_register_existing_user(self):
        client.post("/register", json={"username": "TestUser2", "password": "Strong@123"})
        response = client.post("/register", json={"username": "TestUser2", "password": "Strong@123"})
        self.assertEqual(response.status_code, 400)

    def test_register_invalid_username(self):
        response = client.post("/register", json={"username": "!!", "password": "Strong@123"})
        self.assertEqual(response.status_code, 422)

    def test_register_short_username(self):
        response = client.post("/register", json={"username": "ab", "password": "Strong@123"})
        self.assertEqual(response.status_code, 422)

    def test_register_weak_password(self):
        response = client.post("/register", json={"username": "TestUser3", "password": "123"})
        self.assertEqual(response.status_code, 422)

    def test_register_missing_password(self):
        response = client.post("/register", json={"username": "TestUser4"})
        self.assertEqual(response.status_code, 422)

    def test_register_missing_username(self):
        response = client.post("/register", json={"password": "Strong@123"})
        self.assertEqual(response.status_code, 422)

    def test_login_valid_credentials(self):
        client.post("/register", json={"username": "TestUser5", "password": "Strong@123"})
        response = client.get("/login", params={"username": "TestUser5", "password": "Strong@123"})
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_password(self):
        client.post("/register", json={"username": "TestUser6", "password": "Strong@123"})
        response = client.get("/login", params={"username": "TestUser6", "password": "Wrong123"})
        self.assertEqual(response.status_code, 401)

    def test_login_missing_username(self):
        response = client.get("/login", params={"password": "Strong@123"})
        self.assertEqual(response.status_code, 400)

    def test_login_missing_password(self):
        response = client.get("/login", params={"username": "TestUser7"})
        self.assertEqual(response.status_code, 400)

    def test_login_nonexistent_user(self):
        response = client.get("/login", params={"username": "GhostUser", "password": "Strong@123"})
        self.assertEqual(response.status_code, 404)

    def test_logout(self):
        response = client.post("/logout")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Logout successful!"})

    def test_password_no_uppercase(self):
        response = client.post("/register", json={"username": "TestUser8", "password": "weak@123"})
        self.assertEqual(response.status_code, 422)

    def test_password_no_special_char(self):
        response = client.post("/register", json={"username": "TestUser9", "password": "Strong123"})
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
