from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel # for data validation
from typing import Optional # for optional fields like email and phone

app = FastAPI()

# Dummy user store
users_db = {}

# Pydantic models
class RegisterModel(BaseModel):
    username: str
    password: str

class LoginModel(BaseModel):
    username: str
    password: str

@app.get("/")
def read_root():
    return {"Message": "This is a simple FastAPI application for user registration and login."}\

@app.post("/register")
def register(user: RegisterModel):
    if user.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    users_db[user.username] = user.password
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: LoginModel):
    if users_db.get(user.username) != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    return {"message": "Login successful"}

@app.post("/logout")
def logout():
    return {"message": "Logout successful"}