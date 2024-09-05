from fastapi import FastAPI, Request, HTTPException
from .route import router as auth_router
from .models import Base
from .connection import engine
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/api")

#Custom Error Handling
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = ""
    for error in exc.errors():
        loc = " -> ".join(str(x) for x in error.get("loc", []))
        details += f"{loc}: {error.get('msg', '')}\n"

    return JSONResponse(
        status_code=400,
        content={
            "status": "failed",
            "message": "Validation error",
            "details": details.strip()
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "failed",
            "message": exc.detail
        }
    )
