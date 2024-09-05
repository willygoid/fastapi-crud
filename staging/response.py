from pydantic import BaseModel

#All response Format From API Defined Here

class FailedLoginResponse(BaseModel):
    status: str
    message: str

class SuccessLoginResponse(BaseModel):
    status: str
    message: str
    access_token: str
    token_type: str
    expires_in: str
