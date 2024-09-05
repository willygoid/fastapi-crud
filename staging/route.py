from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .connection import get_db
from .models import *
from .auth import authenticate_user, create_access_token, get_password_hash, get_current_user
from .response import *
from .field import *
import datetime

router = APIRouter()


@router.post("/register", responses={200: {"response": Response}, 400: {"response": ResponseDetail}})
def register_user(request: RegisterField, db: Session = Depends(get_db)):
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
            created_at= datetime.datetime.utcnow()
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


@router.post("/login", responses={200: {"response": ResponseDetail}, 400: {"response": Response}})
def login_for_access_token(request: LoginField, db: Session = Depends(get_db)):
    user = authenticate_user(db, request.credential, request.password)
    if not user:
        return Response(status="failed", message="Incorrect username or password")
    access_token, expire = create_access_token(data={"sub": user.username}) #pakaiusername dari db untuk generate token
    expired_time = expire.strftime('%Y-%m-%dT%H:%M:%S')
    authdata = {"accesstoken": access_token, "token_type": "bearer", "expires_in": expired_time}
    return ResponseDetail(status="success", message="Successfully logged in", details=authdata)

#Protected Route with Header
@router.get("/user", responses={200: {"response": ResponseDetail}, 400: {"response": Response}})
def protected_route(authUser: Optional[ResponseDetail] = Depends(get_current_user)):
    if authUser is None:
        return Response(status="failed", message="User not authenticated")

    user_data = {"id": authUser.id, "firstname": authUser.firstname, "lastname": authUser.lastname, "username": authUser.username, "email": authUser.email, "role": authUser.role, "registered": authUser.created_at}
    return ResponseDetail(status="success", message="User data retrieved successfully", details=user_data)




