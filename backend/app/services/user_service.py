from sqlalchemy.orm import Session
from app.db import models
from app.schemas import user as user_schema
from app.core.security import get_password_hash

def create_user(db: Session, user: user_schema.UserCreate):
    """
    Creates a new user in the database.
    """
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password # We need to add this column to our model
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user