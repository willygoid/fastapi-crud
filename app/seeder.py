# seed_data.py
from sqlalchemy.orm import Session
from .models import Role

# Define your roles
DEFAULT_ROLES = ["superadmin", "admin", "analyst", "user"]

def seed_roles(db: Session):
    """
    Seeds default roles into the database if they don't exist.
    """
    for role_name in DEFAULT_ROLES:
        role = db.query(Role).filter_by(name=role_name).first()
        if not role:
            new_role = Role(name=role_name)
            db.add(new_role)
            db.commit()
