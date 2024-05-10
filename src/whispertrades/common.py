import traceback
from typing import Any, Callable, Union

from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: bool
    message: str
    data: Union[list[dict], dict] = []
    pages: list = None  # TODO: TBC


class APIError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        if message == 'Invalid token permissions':
            raise TokenPermissionError(message)
        elif message == 'Not authenticated':
            raise InvalidTokenError(message)


class TokenPermissionError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class ReportRunningWarning(UserWarning):
    pass


class ReportUninitializedWarning(UserWarning):
    pass


class UpdatingDict(dict):
    def __init__(self, update_fn: Callable[[str], Any] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._update_fn = update_fn

    def __getitem__(self, key: str) -> Any:
        if key in self and self._update_fn:
            if not "IPython\\lib\\pretty.py" in traceback.extract_stack()[-2].filename:  # do not trigger update if called from IPython/Jupyter
                self[key] = self._update_fn(key)
        return super().__getitem__(key)
