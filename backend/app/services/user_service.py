from sqlalchemy.orm import Session
from app.db import models
from app.schemas import user as user_schema
from app.core.security import get_password_hash
from sqlalchemy.orm import Session
from app.db import models
from app.schemas import user as user_schema
from app.core.security import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str):
    """Gets a user by their email address."""
    return db.query(models.User).filter(models.User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticates a user. Returns the user object if successful, otherwise None.
    """
    user = get_user_by_email(db=db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

# ... (keep the existing create_user function) ...
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