# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter  # Correctly import from fastapi-limiter
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from . import models, schemas, crud, security
from .database import engine, Base, get_db
from .limiter import init_limiter  # This is your custom function to initialize the limiter
from .seeder import seed_roles #dbseeder

app = FastAPI()

@app.on_event("startup")
async def startup():
    # Initialize Redis for rate limiting
    await init_limiter(app)

    # Create database tables
    Base.metadata.create_all(bind=engine)

    # Seed roles
    db: Session = next(get_db())
    seed_roles(db)


# Registration route
@app.post("/register/", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# Login route with rate limiting
@app.post("/login", dependencies=[Depends(RateLimiter(times=5, seconds=60))])  # Use RateLimiter from fastapi-limiter
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, credential=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

# Protected route with JWT token required
@app.get("/users/me/", response_model=schemas.UserOut)
def read_users_me(current_user: schemas.UserOut = Depends(security.get_current_active_user)):
    return current_user
