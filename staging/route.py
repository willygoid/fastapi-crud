from fastapi import APIRouter, Depends
from .connection import get_db
from .auth import get_current_user
from .response import *
from .field import *
from .controller import *

router = APIRouter()

# @router.post("/register", response_model=Response, responses={400: {"model": ResponseDetail}})
# def register_user(request: RegisterField, db: Session = Depends(get_db)):
#     return RegisterController(request, db)

@router.post("/login", response_model=ResponseDetail, responses={400: {"model": Response}})
def login_for_access_token(request: LoginField, db: Session = Depends(get_db)):
    return LoginController(request, db)

#Protected Route with Header
@router.get("/credential", response_model=ResponseDetail, responses={400: {"model": Response}})
def user_credential(auth_user: Optional[ResponseDetail] = Depends(get_current_user)):
    return UserDetailsContoller(auth_user)

@router.post("/user", response_model=Response, responses={400: {"model": ResponseDetail}})
def create_user(request: RegisterField, db: Session = Depends(get_db), auth_user: Optional[Response] = Depends(get_current_user)):
    return UserCreateController(request, db, auth_user)

@router.put("/user/{user_id}", response_model=Response, responses={400: {"model": ResponseDetail}})
def edit_user(user_id: int, request: RegisterField, db: Session = Depends(get_db), auth_user: Optional[Response] = Depends(get_current_user)):
    return UserEditController(user_id, request, db, auth_user)

@router.delete("/user/{user_id}", response_model=Response, responses={400:{"model": ResponseDetail}})
def delete_user(user_id, db: Session = Depends(get_db), auth_user: Optional[Response] = Depends(get_current_user)):
    return UserDeleteController(user_id, db, auth_user)








