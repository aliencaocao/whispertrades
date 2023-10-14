from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: bool
    message: str
    data: list = []


class APIError(Exception):
    pass
