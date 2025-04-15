import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Helper: register user safely
def register_user(username: str, password: str):
    return client.post("/register", json={"username": username, "password": password})

# ---- Test Cases ----

def test_register_valid_user():
    response = register_user("PyUser1", "Test@123")
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully!"}

def test_register_existing_user():
    register_user("PyUser2", "Test@123")
    response = register_user("PyUser2", "Test@123")
    assert response.status_code == 400

def test_register_invalid_username():
    response = register_user("!!", "Test@123")
    assert response.status_code == 422

def test_register_short_username():
    response = register_user("ab", "Test@123")
    assert response.status_code == 422

def test_register_weak_password():
    response = register_user("PyUser3", "123")
    assert response.status_code == 422

def test_register_missing_password():
    response = client.post("/register", json={"username": "PyUser4"})
    assert response.status_code == 422

def test_register_missing_username():
    response = client.post("/register", json={"password": "Test@123"})
    assert response.status_code == 422

def test_login_valid_credentials():
    register_user("PyUser5", "Test@123")
    response = client.get("/login", params={"username": "PyUser5", "password": "Test@123"})
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful!"}

def test_login_invalid_password():
    register_user("PyUser6", "Test@123")
    response = client.get("/login", params={"username": "PyUser6", "password": "Wrong123"})
    assert response.status_code == 401

def test_login_missing_username():
    response = client.get("/login", params={"password": "Test@123"})
    assert response.status_code == 400

def test_login_missing_password():
    response = client.get("/login", params={"username": "PyUser7"})
    assert response.status_code == 400

def test_login_nonexistent_user():
    response = client.get("/login", params={"username": "NoOne", "password": "Test@123"})
    assert response.status_code == 404

def test_logout():
    response = client.post("/logout")
    assert response.status_code == 200
    assert response.json() == {"message": "Logout successful!"}

def test_password_no_uppercase():
    response = register_user("PyUser8", "weak@123")
    assert response.status_code == 422

def test_password_no_special_char():
    response = register_user("PyUser9", "Strong123")
    assert response.status_code == 422
