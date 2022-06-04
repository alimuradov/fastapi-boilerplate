from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    role: str

    class Config:
        orm_mode = True

class UserMe(UserBase):
    id: Optional[int] = None
    scope: List[str]
    position: str

    class Config:
        orm_mode = True

# Additional properties to return via API
class User(UserInDBBase):
    pass


class GetUser(BaseModel):
    user: UserMe
    
    class Config:
        orm_mode = True    

# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str