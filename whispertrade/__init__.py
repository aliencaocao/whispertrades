from pydantic import BaseModel
import requests
import orjson
from typing import Union, Optional

ENDPOINT = 'https://api.whispertrades.com/v1/'

from .bots import Bot, BotResponse


class BaseResponse(BaseModel):
    success: bool
    message: str
    data: list = []


class APIError(Exception):
    pass


class WTClient:
    """
    Client for the WhisperTrade API.
    To initialize, provide a valid API token. Endpoint can be customized if needed e.g. proxy server etc.
    """
    def __init__(self, token: str, auto_init: bool = True, endpoint: str = ENDPOINT):
        """
        :param token: API token obtained from WhisperTrade
        :param auto_init: Defaults to True. If True, will automatically query and cache all information about the account that the token has access to.
        :param endpoint: Optional, defaults to https://api.whispertrades.com/v1/
        """
        self.token = token
        self.endpoint = endpoint
        self.headers = {'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {self.token}'}
        self._bots: list[Bot] = []

        if auto_init:
            self._get_bots(include_details=True)

    @property
    def bots(self) -> list[Bot]:
        """Returns a list of Bot objects that was cached by the previous call to get_bots(). To refresh, call get_bots() again. If get_bots() was never called, accessing this attribute will call get_bots() and return the result."""
        if not self._bots:
            self._get_bots(include_details=True)
        return self._bots

    def _get_bots(self, bot_id: Union[int, str] = '', statuses: list = None, include_details: bool = False):
        payload = {}
        if isinstance(bot_id, int):
            bot_id = str(bot_id)
        valid_statuses = ["Enabled", "Disabled", "Disable on Close"]
        if statuses:
            for status in statuses:
                if status not in valid_statuses:
                    raise ValueError(f"Invalid status: {status}")
            payload['statuses'] = statuses
        if include_details:
            payload['include_details'] = include_details
        response = requests.get(f"{self.endpoint}bots/{bot_id}", headers=self.headers, params=payload)
        response = BaseResponse(**orjson.loads(response.text))
        print(response)
        if response.success:
            for bot_data in response.data:
                bot = Bot(BotResponse(**bot_data))
                self._bots.append(bot)
        else:
            raise APIError(response.message)

    def get_bots(self, statuses: list = None, include_details: bool = False):
        """
        Get information of all bots
        :param statuses: Optional, list of statuses to filter by, valid values are "Enabled", "Disabled", "Disable on Close"
        :param include_details: Optional, defaults to False.
        """
        return self._get_bots(statuses=statuses, include_details=include_details)

    def get_bot(self, bot_id: Union[int, str], statuses: list = None, include_details: bool = True):
        """
        Get information of a bot by ID
        :param bot_id: ID of the bot, e.g. BYZ8UNMX8M
        :param statuses: Optional, list of statuses to filter by, valid values are "Enabled", "Disabled", "Disable on Close"
        :param include_details: Optional, defaults to True.
        """
        return self._get_bots(bot_id=bot_id, statuses=statuses, include_details=include_details)
