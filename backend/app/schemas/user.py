from pydantic import BaseModel, EmailStr
import uuid
from typing import Optional

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    username: str

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

# Properties to return to client
class User(UserBase):
    user_id: uuid.UUID

    class Config:
        orm_mode = True # This allows the model to be created from an ORM object