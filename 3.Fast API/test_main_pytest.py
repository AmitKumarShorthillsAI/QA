import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from fastapi import HTTPException
from pydantic import ValidationError

from main import register, login, RegisterModel

# Reusable mock DB fixture
@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

# ---------- Registration Tests ----------

def test_register_valid_user(mock_db):
    mock_db.query().filter().first.return_value = None
    user = RegisterModel(username="TestUser1", password="Strong@123")
    response = register(user, db=mock_db)
    assert response == {"message": "User registered successfully!"}

def test_register_existing_user(mock_db):
    mock_db.query().filter().first.return_value = True
    user = RegisterModel(username="TestUser2", password="Strong@123")
    with pytest.raises(HTTPException) as exc:
        register(user, db=mock_db)
    assert exc.value.status_code == 400

def test_register_invalid_username():
    with pytest.raises(ValueError):
        RegisterModel(username="!!", password="Strong@123")

def test_register_short_username():
    with pytest.raises(ValueError):
        RegisterModel(username="ab", password="Strong@123")

def test_register_weak_password():
    with pytest.raises(ValueError):
        RegisterModel(username="TestUser3", password="123")

def test_register_password_no_uppercase():
    with pytest.raises(ValueError):
        RegisterModel(username="TestUser4", password="weak@123")

def test_register_password_no_special_char():
    with pytest.raises(ValueError):
        RegisterModel(username="TestUser5", password="Strong123")

def test_register_missing_password():
    with pytest.raises(ValidationError):
        RegisterModel(username="TestUser6")

def test_register_missing_username():
    with pytest.raises(ValidationError):
        RegisterModel(password="Strong@123")

# ---------- Login Tests ----------

def test_login_valid_user(mock_db):
    mock_db.query().filter().first.return_value = type('User', (), {
        "username": "TestUser7",
        "password": "Strong@123"
    })()
    response = login(username="TestUser7", password="Strong@123", db=mock_db)
    assert response == {"message": "Login successful!"}

def test_login_wrong_password(mock_db):
    mock_db.query().filter().first.return_value = type('User', (), {
        "username": "TestUser8",
        "password": "Strong@123"
    })()
    with pytest.raises(HTTPException) as exc:
        login(username="TestUser8", password="WrongPass", db=mock_db)
    assert exc.value.status_code == 401

def test_login_user_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    with pytest.raises(HTTPException) as exc:
        login(username="GhostUser", password="Strong@123", db=mock_db)
    assert exc.value.status_code == 404

def test_login_missing_username(mock_db):
    with pytest.raises(HTTPException) as exc:
        login(username=None, password="Strong@123", db=mock_db)
    assert exc.value.status_code == 400

def test_login_missing_password(mock_db):
    with pytest.raises(HTTPException) as exc:
        login(username="TestUser9", password=None, db=mock_db)
    assert exc.value.status_code == 400
