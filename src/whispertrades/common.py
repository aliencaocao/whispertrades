from typing import Any, Callable, Union

from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: bool
    message: str
    data: Union[list[dict], dict] = []


class APIError(Exception):
    pass


class UpdatingDict(dict):
    def __init__(self, update_fn: Callable[[str], Any] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_fn = update_fn

    def __getitem__(self, key):
        if key not in self:
            if self.update_fn:
                self[key] = self.update_fn(key)
            else:
                raise KeyError(f"Key {key} not found in the dictionary.")
        return super().__getitem__(key)
