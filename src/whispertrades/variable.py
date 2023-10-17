from datetime import datetime
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel

from .common import BaseResponse

if TYPE_CHECKING:
    from . import WTClient


class BaseVariable(BaseModel):
    number: str
    name: str
    value: Optional[str]
    free_text_value_to_set: Optional[str] = None
    last_updated_at: Optional[datetime] = None


class Condition(BaseModel):
    condition: str
    value: str


class VariableResponse(BaseVariable):
    bot: Optional[str]
    conditions: list[Optional[Condition]]


class Variable:
    def __init__(self, data: VariableResponse, client: 'WTClient', auto_refresh: bool):
        self._VariableResponse = data
        self.client = client
        self.auto_refresh = auto_refresh

        self.number = data.number
        self.name = data.name
        self.value = data.value
        self.free_text_value_to_set = data.free_text_value_to_set
        self.last_updated_at = data.last_updated_at
        self.bot = data.bot
        self.conditions = data.conditions

    def edit(self, name: str = None, value: str = None) -> str:
        if not name or value is None:
            raise ValueError('Either name or value are required. Name cannot be empty string.')
        if self.bot:
            raise ValueError('You can only update variables that are not associated with a bot.')
        payload = {}
        if name:
            payload['name'] = name
        if value is not None:
            payload['value'] = value
        response = self.client.session.put(f"{self.client.endpoint}bots/{self.bot}/variables/{self.number}", headers=self.client.headers, json=payload)
        response = BaseResponse(**orjson.loads(response.text))
        if response.success:
            self.__init__(VariableResponse(**response.data), self.client, self.auto_refresh)
            return response.message
        else:
            raise APIError(response.message)

    def __repr__(self):
        if self.auto_refresh:
            self.client.get_variable(self.number)
        return str(self._VariableResponse)

    def __getattribute__(self, name):
        if not name.endswith('Response') and name not in ['number', 'bot'] and name in self._VariableResponse.model_fields and self.auto_refresh:
            self.client.get_variable(self.number)
        return super().__getattribute__(name)
