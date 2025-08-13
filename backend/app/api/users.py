from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import user as user_schema
from app.services import user_service
from app.db.database import get_db

router = APIRouter()

@router.post("/users/", response_model=user_schema.User, status_code=201)
def create_new_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    # You can add logic here to check if a user with that email already exists
    # For now, we will just create the user.
    db_user = user_service.create_user(db=db, user=user)
    if not db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return db_user