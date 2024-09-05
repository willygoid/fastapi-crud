from pydantic import BaseModel
from typing import Optional, Union

#All response Format From API Defined Here
class Response(BaseModel):
    status: str
    message: str

class ResponseDetail(BaseModel):
    status: str
    message: str
    details: Optional[Union[str, dict, list]] = None