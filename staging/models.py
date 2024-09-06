from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum
import datetime

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
    role = Column(String(12), nullable=False, default=RoleEnum.user)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat()  # Format datetime as ISO string
        }



