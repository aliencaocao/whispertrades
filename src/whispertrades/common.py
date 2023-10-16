from typing import Union

from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: bool
    message: str
    data: Union[list[dict], dict] = []


class APIError(Exception):
    pass
