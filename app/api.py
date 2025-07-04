import os
from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.auth import hash_password, verify_password

from pydantic import BaseModel, EmailStr

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
router = APIRouter()


# User registration page
@router.get("/register", response_class=HTMLResponse)
async def show_register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


# User registration posting
@router.post("/register")
async def register_user(
    request: Request,
    username: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        # Create a already_registered.html to return for existing
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "msg": "Email already registered"},
            status_code=400,
        )

    hashed_pw = hash_password(password)
    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_pw,
    )

    db.add(new_user)
    db.commit()

    return templates.TemplateResponse(
        "login.html", {"request": request, "msg": "Registration successful"}
    )


# User login
@router.get("/login", response_class=HTMLResponse)
async def display_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# User's see the watchlist page after logging in
@router.post("/login", response_class=HTMLResponse)
async def handle_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    # display the user's watchlist page
    # allow users to add company names to watchlist

    user = db.query(User).filter(User.username == username).first()

    # Invalid login
    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "msg": "Invalid username or password"},
            status_code=400,
        )

    # Valid login
    return templates.TemplateResponse(
        "display_watchlist.html", {"request": request, "user": user}
    )
