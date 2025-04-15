# Importing FastAPI framework and HTTPException for handling HTTP errors
from fastapi import FastAPI, HTTPException, status, Request, Depends
# Importing MySQL connector for database connection
import mysql.connector

# Importing Pydantic BaseModel for request validation and field_validator for custom validation
from pydantic import BaseModel, field_validator

# Importing Optional for optional parameters
from typing import Optional

# Importing SQLAlchemy components for database interaction
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Importing regex module for password validation
import re

# Importing os module for environment variable management
import os
from dotenv import load_dotenv

# --------------------------------- FastAPI App --------------------------------------------
# Creating a FastAPI instance
app = FastAPI()

# --------------------------------- SQLAlchemy Setup ---------------------------------------
# Load environment variables
load_dotenv()

# Read values
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# Database connection URL (<your_password> -> MySQL root password)
DATABASE_URL = f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Creating a SQLAlchemy engine to connect to the database
engine = create_engine(DATABASE_URL)

# Creating a session factory for database sessions
SessionLocal = sessionmaker(bind=engine)

# Declaring the base class for ORM models
Base = declarative_base()

# ---------------------------------- DB Model -----------------------------------------------
# Defining the User table schema using SQLAlchemy ORM
class User(Base):
    __tablename__ = "users"  # Table name in the database
    id = Column(Integer, primary_key=True, index=True)  # Primary key column
    username = Column(String(50), unique=True, nullable=False)  # Username column (unique and required)
    password = Column(String(255), nullable=False)  # Password column (required)

# Create the table in the database if it does not already exist
Base.metadata.create_all(bind=engine)

# --------------------------------- Pydantic Models -------------------------------------------
# Pydantic model for user registration request validation
class RegisterModel(BaseModel):
    username: str  # Username field
    password: str  # Password field

    # Custom validator for username
    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        # Ensure username is alphanumeric and at least 3 characters long
        if len(v) < 3 or not v.isalnum():
            raise ValueError("Username must be alphanumeric and at least 3 characters long.")
        return v

    # Custom validator for password
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        # Ensure password meets complexity requirements
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters.")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must include at least one uppercase letter.")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must include at least one lowercase letter.")
        if not re.search(r"\d", v):
            raise ValueError("Password must include at least one number.")
        if not re.search(r"[^\w\s]", v):
            raise ValueError("Password must include at least one special character.")
        return v

# Pydantic model for user login request validation
class LoginModel(BaseModel):
    username: str  # Username field
    password: str  # Password field

# ----------------------------------- Dependency -------------------------------------------------
# Dependency function to get a database session
def get_db():
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Yield the session for use in routes
    finally:
        db.close()  # Close the session after use

# ----------------------------------- Routes --------------------------------------------------------
# Home route to test the API
@app.get("/")
def home():
    return {"message": "FastAPI with MySQL - User Auth System"}

# Route for user registration
@app.post("/register")
def register(user: RegisterModel, db: Session = Depends(get_db)):
    # Check if the username already exists in the database
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Create a new user and save to the database
    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully!"}

# Route for user login
@app.get("/login")
def login(username: Optional[str] = None, password: Optional[str] = None, db: Session = Depends(get_db)):
    print(f"Username: {username}, Password: {password}")  # Debugging line
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required.")

    # Check if the username exists in the database
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Username does not exist.")
    
    # Validate the password
    if user.password != password:
        raise HTTPException(status_code=401, detail="Invalid password.")
    
    return {"message": "Login successful!"}

# Route for user logout
@app.post("/logout")
def logout():
    return {"message": "Logout successful!"}