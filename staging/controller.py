from sqlalchemy.orm import Session
from .models import User
from .auth import get_password_hash, authenticate_user, create_access_token
from .response import Response, ResponseDetail
import datetime

def RegisterController(request, db: Session):
    # Check if the username or email already exists
    db_user = db.query(User).filter(
        (User.username == request.username) | (User.email == request.email)
    ).first()
    if db_user:
        return ResponseDetail(status="failed", message="Username or email already registered", details="Failed register")

    try:
        # Hash the password before storing it
        hashed_password = get_password_hash(request.password)

        # Create a new user instance
        new_user = User(
            firstname=request.firstname,
            lastname=request.lastname,
            username=request.username,
            email=request.email,
            hashed_password=hashed_password,
            role=request.role,
            created_at=datetime.datetime.utcnow()
        )

        # Add the new user to the database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Return a success response
        return Response(status="success", message="Successfully created user")
    except Exception as e:
        # Handle unexpected errors
        return ResponseDetail(status="failed", message="Failed to create user", details=str(e))


def LoginController(request, db: Session):
    user = authenticate_user(db, request.credential, request.password)
    if not user:
        return Response(status="failed", message="Incorrect username or password")

    access_token, expire = create_access_token(data={"sub": user.username})  # using username from db to generate token
    expired_time = expire.strftime('%Y-%m-%dT%H:%M:%S')
    authdata = {"accesstoken": access_token, "token_type": "bearer", "expires_in": expired_time}
    return ResponseDetail(status="success", message="Successfully logged in", details=authdata)


def UserDetailsContoller(authUser):
    if authUser is None:
        return Response(status="failed", message="User not authenticated")

    user_data = {
        "id": authUser.id,
        "firstname": authUser.firstname,
        "lastname": authUser.lastname,
        "username": authUser.username,
        "email": authUser.email,
        "role": authUser.role,
        "registered": authUser.created_at
    }
    return ResponseDetail(status="success", message="User data retrieved successfully", details=user_data)


def UserCreateController(request, db: Session, current_user):
    # Ensure the user is authenticated
    if current_user is None:
        return ResponseDetail(status="failed", message="User not authenticated", details="You need to be logged in to create a user")

    # Check if the username or email already exists
    db_user = db.query(User).filter(
        (User.username == request.username) | (User.email == request.email)
    ).first()
    if db_user:
        return ResponseDetail(status="failed", message="Username or email already registered", details="Failed to create user")

    try:
        # Hash the password before storing it
        hashed_password = get_password_hash(request.password)

        # Create a new user instance
        new_user = User(
            firstname=request.firstname,
            lastname=request.lastname,
            username=request.username,
            email=request.email,
            hashed_password=hashed_password,
            role=request.role,
            created_at=datetime.datetime.utcnow()
        )

        # Add the new user to the database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Return a success response
        return Response(status="success", message="Successfully created user")
    except Exception as e:
        # Handle unexpected errors
        return ResponseDetail(status="failed", message="Failed to create user", details=str(e))


def UserEditController(user_id: int, request, db: Session, current_user):
    # Ensure the user is authenticated
    if current_user is None:
        return ResponseDetail(status="failed", message="User not authenticated", details="You need to be logged in to edit a user")

    # Fetch the user to be updated
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return ResponseDetail(status="failed", message="User not found", details=f"User with ID {user_id} does not exist")

    # Update the user's information
    user.firstname = request.firstname
    user.lastname = request.lastname
    user.username = request.username
    user.email = request.email

    if request.password:
        # Hash the new password if provided
        user.hashed_password = get_password_hash(request.password)

    try:
        db.commit()
        db.refresh(user)
        return Response(status="success", message="User updated successfully")
    except Exception as e:
        return ResponseDetail(status="failed", message="Failed to update user", details=str(e))

def UserDeleteController(user_id: int, db: Session, current_user):
    # Ensure the user is authenticated
    if current_user is None:
        return ResponseDetail(status="failed", message="User not authenticated", details="You need to be logged in to delete a user")

    # Fetch the user to be deleted
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return ResponseDetail(status="failed", message="User not found", details=f"User with ID {user_id} does not exist")

    try:
        db.delete(user)
        db.commit()
        return Response(status="success", message="User deleted successfully")
    except Exception as e:
        return ResponseDetail(status="failed", message="Failed to delete user", details=str(e))

