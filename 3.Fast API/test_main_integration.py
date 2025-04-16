import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from main import app, Base, get_db

# ------------------------
# Setup: Use SQLite in-memory DB for isolation
# ------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.sqlite3"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the app's get_db dependency for test DB
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

class TestFastAPIAuthIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=engine)

    def setUp(self):
        # Optional: can truncate users table before each test for isolation
        db = TestingSessionLocal()
        db.execute(text("DELETE FROM users")) # text is used mark the raw SQL string explicitly as SQL text expression
        db.commit()
        db.close()

    # 1. Valid Registration
    def test_register_valid_user(self):
        res = client.post("/register", json={"username": "TestUser1", "password": "Strong@123"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {"message": "User registered successfully!"})

    # 2. Register existing user
    def test_register_existing_user(self):
        client.post("/register", json={"username": "TestUser2", "password": "Strong@123"})
        res = client.post("/register", json={"username": "TestUser2", "password": "Strong@123"})
        self.assertEqual(res.status_code, 400)

    # 3–7: Invalid registrations
    def test_register_invalid_username(self):
        res = client.post("/register", json={"username": "!!", "password": "Strong@123"})
        self.assertEqual(res.status_code, 422)

    def test_register_short_username(self):
        res = client.post("/register", json={"username": "ab", "password": "Strong@123"})
        self.assertEqual(res.status_code, 422)

    def test_register_weak_password(self):
        res = client.post("/register", json={"username": "TestUser3", "password": "123"})
        self.assertEqual(res.status_code, 422)

    def test_register_password_no_uppercase(self):
        res = client.post("/register", json={"username": "TestUser4", "password": "weak@123"})
        self.assertEqual(res.status_code, 422)

    def test_register_password_no_special_char(self):
        res = client.post("/register", json={"username": "TestUser5", "password": "Strong123"})
        self.assertEqual(res.status_code, 422)

    # 8–9: Missing fields
    def test_register_missing_password(self):
        res = client.post("/register", json={"username": "TestUser6"})
        self.assertEqual(res.status_code, 422)

    def test_register_missing_username(self):
        res = client.post("/register", json={"password": "Strong@123"})
        self.assertEqual(res.status_code, 422)

    # 10. Valid Login
    def test_login_valid_credentials(self):
        client.post("/register", json={"username": "TestUser7", "password": "Strong@123"})
        res = client.get("/login", params={"username": "TestUser7", "password": "Strong@123"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {"message": "Login successful!"})

    # 11–13: Invalid logins
    def test_login_invalid_password(self):
        client.post("/register", json={"username": "TestUser8", "password": "Strong@123"})
        res = client.get("/login", params={"username": "TestUser8", "password": "WrongPass"})
        self.assertEqual(res.status_code, 401)

    def test_login_nonexistent_user(self):
        res = client.get("/login", params={"username": "GhostUser", "password": "Strong@123"})
        self.assertEqual(res.status_code, 404)

    def test_login_missing_username(self):
        res = client.get("/login", params={"password": "Strong@123"})
        self.assertEqual(res.status_code, 400)

    def test_login_missing_password(self):
        res = client.get("/login", params={"username": "TestUser9"})
        self.assertEqual(res.status_code, 400)

    # 14. Logout test
    def test_logout(self):
        res = client.post("/logout")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {"message": "Logout successful!"})


if __name__ == "__main__":
    unittest.main()
