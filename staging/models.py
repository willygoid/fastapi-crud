from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, field_validator, constr, EmailStr
import re
from enum import Enum
from typing import Optional


Base = declarative_base()

#Role Enumeration
class RoleEnum(str, Enum):
    superadmin = "superadmin"
    admin = "admin"
    analyst = "analyst"
    user = "user"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50))
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    role = Column(String(12), nullable=False)

# Field user Register to accept request
class UserCreate(BaseModel):
    firstname: constr(min_length=1)
    lastname: str
    username: constr(min_length=3)
    email: EmailStr
    password: constr(min_length=8)
    role: RoleEnum

    #required field
    @field_validator('firstname', 'username', 'email', 'password', 'role', mode='before')
    def check_not_empty(cls, value, field_info):
        if not value.strip():
            raise ValueError(f"{field_info.field_name} cannot be empty")
        return value

    #Validate userrname
    @field_validator('username')
    def validate_username(cls, value):
        if not re.match(r'^[a-zA-Z0-9_]+$', value):  # Ensures username is alphanumeric with underscores
            raise ValueError('Username must be alphanumeric and can include underscores only')
        return value

# Field user login to accept request
class UserLogin(BaseModel):
    credential: str
    password: str

#for print API Response
class SuccessResponse(BaseModel):
    status: str
    message: str

class ErrorResponse(BaseModel):
    status: str
    message: str
    details: Optional[str] = None

class SuccessLoginResponse(BaseModel):
    status: str
    message: str
    access_token: str
    token_type: str
    expires_in: str

class UserResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True