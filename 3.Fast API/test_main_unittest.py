import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from fastapi import HTTPException
from pydantic import ValidationError

from main import register, login, RegisterModel

class TestFastAPIAuthUnit(unittest.TestCase):

    def setUp(self):
        # Set up mock database session
        self.mock_db = MagicMock(spec=Session)

    def test_register_valid_user(self):
        self.mock_db.query().filter().first.return_value = None
        user = RegisterModel(username="TestUser1", password="Strong@123")
        response = register(user, db=self.mock_db)
        self.assertEqual(response, {"message": "User registered successfully!"})

    def test_register_existing_user(self):
        self.mock_db.query().filter().first.return_value = True
        user = RegisterModel(username="TestUser2", password="Strong@123")
        with self.assertRaises(HTTPException) as context:
            register(user, db=self.mock_db)
        self.assertEqual(context.exception.status_code, 400)

    def test_register_invalid_username(self):
        with self.assertRaises(ValueError):
            RegisterModel(username="!!", password="Strong@123")

    def test_register_short_username(self):
        with self.assertRaises(ValueError):
            RegisterModel(username="ab", password="Strong@123")

    def test_register_weak_password(self):
        with self.assertRaises(ValueError):
            RegisterModel(username="TestUser3", password="123")

    def test_register_password_no_uppercase(self):
        with self.assertRaises(ValueError):
            RegisterModel(username="TestUser4", password="weak@123")

    def test_register_password_no_special_char(self):
        with self.assertRaises(ValueError):
            RegisterModel(username="TestUser5", password="Strong123")

    def test_register_missing_password(self):
        with self.assertRaises(ValidationError):
            RegisterModel(username="TestUser6")

    def test_register_missing_username(self):
        with self.assertRaises(ValidationError):
            RegisterModel(password="Strong@123")


    def test_login_valid_user(self):
        # Fake user object from DB
        self.mock_db.query().filter().first.return_value = type('User', (), {
            "username": "TestUser7",
            "password": "Strong@123"
        })()
        response = login(username="TestUser7", password="Strong@123", db=self.mock_db)
        self.assertEqual(response, {"message": "Login successful!"})

    def test_login_wrong_password(self):
        self.mock_db.query().filter().first.return_value = type('User', (), {
            "username": "TestUser8",
            "password": "Strong@123"
        })()
        with self.assertRaises(HTTPException) as context:
            login(username="TestUser8", password="WrongPass", db=self.mock_db)
        self.assertEqual(context.exception.status_code, 401)

    def test_login_user_not_found(self):
        self.mock_db.query().filter().first.return_value = None
        with self.assertRaises(HTTPException) as context:
            login(username="GhostUser", password="Strong@123", db=self.mock_db)
        self.assertEqual(context.exception.status_code, 404)

    def test_login_missing_username(self):
        with self.assertRaises(HTTPException) as context:
            login(username=None, password="Strong@123", db=self.mock_db)
        self.assertEqual(context.exception.status_code, 400)

    def test_login_missing_password(self):
        with self.assertRaises(HTTPException) as context:
            login(username="TestUser9", password=None, db=self.mock_db)
        self.assertEqual(context.exception.status_code, 400)

if __name__ == "__main__":
    unittest.main()
