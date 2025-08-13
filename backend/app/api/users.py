from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import user as user_schema
from app.services import user_service
from ..db.database import get_db

router = APIRouter()

@router.post("/users/", response_model=user_schema.User, status_code=201)
def create_new_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    # First, check if a user with this email already exists
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        # If the user exists, raise a proper HTTP error
        raise HTTPException(status_code=400, detail="Email already registered")

    # If the user doesn't exist, create the new user
    return user_service.create_user(db=db, user=user)