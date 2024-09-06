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
            username=str(request.username).lower(),
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
        return ResponseDetail(status="failed", message="Failed to create user"+str(e), details=str(e))


def LoginController(request, db: Session):
    user = authenticate_user(db, request.credential, request.password)
    if not user:
        return Response(status="failed", message="Incorrect username or password")

    access_token, expire = create_access_token(data={"sub": user.username})  # using username from db to generate token
    expired_time = expire.strftime('%Y-%m-%dT%H:%M:%S')
    authdata = {"accesstoken": access_token, "token_type": "bearer", "expires_in": expired_time}
    return ResponseDetail(status="success", message="Successfully logged in", details=authdata)


def AuthUserController(authUser): #details info of authenticated user
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


def UserListController(db: Session, auth_user):
    if auth_user is None:
        return Response(status="failed", message="User not authenticated")

    try:
        users = db.query(User).all()
        if not users:
            return Response(status="failed", message="No users found")

        return ResponseDetail(status="success", message="Users fetched successfully", details=[user.to_dict() for user in users])
    except Exception as e:
        return Response(status="failed", message="An unexpected error occurred: "+str(e))

def UserCreateController(request, db: Session, auth_user):
    # Ensure the user is authenticated
    if auth_user is None:
        return ResponseDetail(status="failed", message="User not authenticated", details="You need to be logged in to create a user")

    # Check if the authenticated user has the required role
    if auth_user.role not in ['superadmin', 'admin']:
        return ResponseDetail(status="failed", message="Insufficient permissions", details="Youre not allowed to do this action")

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
            username=str(request.username).lower(),
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


def UserEditController(username: str, request, db: Session, auth_user):
    # Ensure the user is authenticated
    if auth_user is None:
        return ResponseDetail(status="failed", message="User not authenticated", details="You need to be logged in to edit a user")

    # Fetch the user to be updated
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return ResponseDetail(status="failed", message="User not found", details=f"User with ID {username} does not exist")

    # Update the user's information
    user.firstname = request.firstname
    user.lastname = request.lastname

    # Change email if provided
    if request.email:
        CheckEmail = db.query(User).filter(User.email == request.email).first()
        if CheckEmail and CheckEmail.username != username:
            return ResponseDetail(status="failed", message="Email already taken", details="Choose another email to continue")
        user.email = request.email

    if request.password:
        # Hash the new password if provided
        user.hashed_password = get_password_hash(request.password)

    if request.role:
        if auth_user.role not in ['superadmin', 'admin']:
            return ResponseDetail(status="failed", message="Insufficient permissions", details="Youre not allowed to do this action")
        else:
            user.role = request.role

    try:
        db.commit()
        db.refresh(user)
        return Response(status="success", message="User updated successfully")
    except Exception as e:
        return ResponseDetail(status="failed", message="Failed to update user", details=str(e))


def UserDeleteController(username: str, db: Session, auth_user):
    # Ensure the user is authenticated
    if auth_user is None:
        return ResponseDetail(status="failed", message="User not authenticated", details="You need to be logged in to delete a user")

    # Fetch the user to be deleted
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return ResponseDetail(status="failed", message="User not found", details=f"User with ID {username} does not exist")

    try:
        db.delete(user)
        db.commit()
        return Response(status="success", message="User deleted successfully")
    except Exception as e:
        return ResponseDetail(status="failed", message="Failed to delete user", details=str(e))


def UserDetailsController(username: str, db: Session, auth_user):
    if auth_user is None:
        return Response(status="failed", message="User not authenticated")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return Response(status="failed", message="User not found")
    try:
        user_data = {
            "firstname": user.firstname,
            "lastname": user.lastname,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "registered": user.created_at
        }
        return ResponseDetail(status="success", message="User data retrieved successfully", details=user_data)
    except Exception as e:
        return ResponseDetail(status="failed", message="Failed to fetch user", details=str(e))
