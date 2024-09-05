from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .models import User, UserCreate, SuccessResponse, ErrorResponse, UserResponse, UserLogin
from .connection import get_db
from .security import authenticate_user, create_access_token, get_password_hash, get_current_user
from .response import FailedLoginResponse, SuccessLoginResponse


router = APIRouter()


@router.post("/register", responses={200: {"model": SuccessResponse}, 400: {"model": ErrorResponse}})
def register_user(request: UserCreate, db: Session = Depends(get_db)):
    # Check if the username or email already exists
    db_user = db.query(User).filter(
        (User.username == request.username) | (User.email == request.email)
    ).first()
    if db_user:
        return ErrorResponse(status="failed", message="Username or email already registered")

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
        )

        # Add the new user to the database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Return a success response
        return SuccessResponse(status="success", message="Successfully created user")
    except Exception as e:
        # Handle unexpected errors
        return ErrorResponse(status="failed", message="Failed to create user", details=str(e))


@router.post("/login", responses={200: {"model": SuccessLoginResponse}, 400: {"model": ErrorResponse}})
def login_for_access_token(request: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, request.credential, request.password)
    if not user:
        return FailedLoginResponse(status="failed", message="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username}) #pakaiusername dari db untuk generate token
    return SuccessLoginResponse(status="success", message="Successfully logged in", access_token=access_token, token_type="bearer", expires_in="2m")

#Protected Route with Header
@router.get("/user", response_model=UserResponse)
def protected_route(current_user: UserResponse = Depends(get_current_user)):
    return current_user



