from fastapi import APIRouter, Depends
from .connection import get_db
from .auth import get_current_user
from .field import *
from .controller import *

router = APIRouter()

@router.post("/register", response_model=Response, responses={400: {"model": ResponseDetail}})
def register_user(request: RegisterField, db: Session = Depends(get_db)):
    return RegisterController(request, db)

@router.post("/auth", response_model=ResponseDetail, responses={400: {"model": Response}})
def login_for_access_token(request: LoginField, db: Session = Depends(get_db)):
    return LoginController(request, db)

#Protected Route with Header
@router.get("/auth", response_model=ResponseDetail, responses={400: {"model": Response}})
def user_credential(auth_user: Optional[ResponseDetail] = Depends(get_current_user)):
    return AuthUserController(auth_user)

@router.get("/user", response_model=ResponseDetail, responses={400: {"model": Response}})
def list_user(db: Session = Depends(get_db), auth_user: Optional[ResponseDetail] = Depends(get_current_user)):
    return UserListController(db, auth_user)

@router.post("/user", response_model=Response, responses={200:{"model": Response}, 400: {"model": ResponseDetail}})
def create_user(request: RegisterField, db: Session = Depends(get_db), auth_user: Optional[Response] = Depends(get_current_user)):
    return UserCreateController(request, db, auth_user)

@router.get('/user/{username}', response_model=ResponseDetail, responses={400:{"model": Response}})
def detail_user(username: str, db: Session = Depends(get_db), auth_user: Optional[ResponseDetail] = Depends(get_current_user)):
    return UserDetailsController(username, db, auth_user)

@router.put("/user/{username}", response_model=Response, responses={400: {"model": ResponseDetail}})
def edit_user(username: str, request: EditUserField, db: Session = Depends(get_db), auth_user: Optional[Response] = Depends(get_current_user)):
    return UserEditController(username, request, db, auth_user)

@router.delete("/user/{username}", response_model=Response, responses={400:{"model": ResponseDetail}})
def delete_user(username: str, db: Session = Depends(get_db), auth_user: Optional[Response] = Depends(get_current_user)):
    return UserDeleteController(username, db, auth_user)








