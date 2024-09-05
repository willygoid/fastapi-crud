from pydantic import BaseModel, constr, EmailStr, field_validator
import re
from .models import RoleEnum

# Input Field user Register
class RegisterField(BaseModel):
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

class LoginField(BaseModel):
    credential: str
    password: str