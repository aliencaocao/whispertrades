from datetime import datetime
from typing import Optional, TYPE_CHECKING

import orjson
from pydantic import BaseModel

from .common import APIError, BaseResponse

if TYPE_CHECKING:
    from . import WTClient


class BaseVariable(BaseModel):
    number: str
    name: str
    value: Optional[str]
    free_text_value: Optional[str] = None
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
        self.free_text_value = data.free_text_value
        self.last_updated_at = data.last_updated_at
        self.bot = data.bot
        self.conditions = data.conditions

        if data.bot is None:
            self.free_text_value = data.value  # Variables not associated with bots are always free text

    def update(self, name: str = None, value: str = None) -> str:
        """
        Change this variable name or free text value
        Auth Required: Write Variables
        :param name: new name of the variable
        :param value: New free text value for the variable. This is only valid if the variable is a "Free Text" type that is not associated with a bot
        :return: message from Whispertrades API
        """
        if not name and value is None:
            raise ValueError('Either name or value are required. Name cannot be empty string.')
        if value is not None:
            if self.bot:
                raise ValueError('You can only update values of variables that are not associated with a bot.')
            if self.free_text_value is None:  # currently this is not needed as all variables without a bot associated will always be free text, but this line is kept for future possible expansion
                raise ValueError('You can only update free text variables.')
        payload = {}
        if name:
            payload['name'] = str(name)
        if value is not None:
            payload['value'] = str(value)
        response = self.client.session.put(f"{self.client.endpoint}bots/variables/{self.number}", headers=self.client.headers, json=payload)
        response = BaseResponse(**orjson.loads(response.text))
        if response.success:
            self.__init__(VariableResponse(**response.data), self.client, self.auto_refresh)
            return response.message
        else:
            raise APIError(response.message)

    def __repr__(self):
        return f'<Variable {self._VariableResponse}>'

    def __getattribute__(self, name):
        if not name.endswith('Response') and name not in ['number', 'bot'] and name in self._VariableResponse.model_fields and self.auto_refresh:
            self.client.get_variable(self.number)
        return super().__getattribute__(name)
