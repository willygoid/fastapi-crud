from sqlalchemy.orm import Session
from .connection import engine, get_db
from .models import Base, User, RoleEnum
from .auth import get_password_hash


def create_tables():
    # Create tables in the database
    Base.metadata.create_all(bind=engine)

def seed_data(db: Session):
    # Check if there are any existing users to avoid duplicate seeding
    if db.query(User).count() == 0:
        # List of user data to be seeded
        users = [
            User(
                firstname="Super Admin",
                lastname="",
                username="superadmin",
                email="superadmin@example.com",
                hashed_password=get_password_hash("superadmin123"),
                role=RoleEnum.superadmin
            ),
            User(
                firstname="Admin User",
                lastname="",
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                role=RoleEnum.admin
            ),
            User(
                firstname="Analyst User",
                lastname="",
                username="analyst",
                email="analyst@example.com",
                hashed_password=get_password_hash("analyst123"),
                role=RoleEnum.analyst
            ),
            User(
                firstname="Regular User",
                lastname="",
                username="user",
                email="user@example.com",
                hashed_password=get_password_hash("user1234"),
                role=RoleEnum.user
            )
        ]

        # Add all users to the session and commit
        db.bulk_save_objects(users)
        db.commit()
        print("Database seeded with initial data.")
    else:
        print("Database already contains data. Skipping seeding.")


def seeder():
    # Create tables if they do not exist
    create_tables()

    # Use the get_db function to obtain a session
    with next(get_db()) as db:
        seed_data(db)


