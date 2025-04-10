# QA
This repo is for practicing software testing in QA.


# FastAPI Documentation
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
It is built on top of Starlette for the web parts and Pydantic for the data parts.
FastAPI is easy to use and allows you to create APIs quickly with automatic interactive documentation.

⬤ Installation
    To install FastAPI, you can use pip. It's recommended to create a virtual environment first. 

    1. Create a virtual environment 
        python -m venv venv

    2. Activate the virtual environment
        On Windows:
        venv\Scripts\activate

        On macOS and Linux:
        source venv/bin/activate

    3. Install FastAPI and an ASGI server (like uvicorn)
        pip install fastapi uvicorn

    4. Install Pydantic for data validation
        pip install pydantic
⬤ Setup
1. Create a new Python file (e.g., main.py) and copy the code provided above.

2. Save the file.

3. Make sure you have the necessary imports at the top of your file:
    from fastapi import FastAPI, HTTPException, status
    from pydantic import BaseModel
    from typing import Optional

4. Define your FastAPI app and the necessary routes.
5. Define your Pydantic models for data validation.
6. Use the FastAPI app instance to define your routes.
7. Use Pydantic models to validate incoming data.

⬤ Running the Application
1. Make sure your virtual environment is activated.
2. Run the FastAPI application using uvicorn:
    uvicorn main:app --reload
    
The --reload flag enables auto-reload, so the server will restart upon code changes.