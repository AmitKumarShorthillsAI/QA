from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, field_validator
import re # Importing regex for password validation

app = FastAPI()

# Dummy user database
users_db = {}

# Pydantic model for registration
class RegisterModel(BaseModel):
    username: str
    password: str

    @field_validator('username') # Using field_validator for validation
    @classmethod
    def validate_username(cls, value):
        if not value.isalnum():
            raise ValueError("Username must be alphanumeric only.")
        if len(value) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        return value

    @field_validator('password')
    @classmethod
    def validate_password(cls, value): # Here value is the 'password' in the decorator
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise ValueError("Password must include at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise ValueError("Password must include at least one lowercase letter.")
        if not re.search(r'\d', value):
            raise ValueError("Password must include at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError("Password must include at least one special character.")
        return value

@app.get("/")
def read_root():
    return {"Message": "This is a simple FastAPI app for user registration and login."}

@app.post("/register")
# Using the RegisterModel for registration, user is the instance of RegisterModel
def register(user: RegisterModel):
    if user.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists."
        )
    users_db[user.username] = user.password
    return {"message": "User registered successfully!"}

@app.get("/login")
def login(username: str = Query(...), password: str = Query(...)): # Using Query to get username and password from query parameters
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required."
        )

    stored_password = users_db.get(username)
    if not stored_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Username does not exist."
        )
    if stored_password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password."
        )

    return {"message": "Login successful!"}

@app.post("/logout")
def logout():
    return {"message": "Logout successful!"}
