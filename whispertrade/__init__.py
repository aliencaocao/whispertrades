from typing import Union

import orjson
import requests
from pydantic import BaseModel

from .bots import Bot, BotResponse
from .common import APIError, BaseResponse

ENDPOINT = 'https://api.whispertrades.com/v1/'


class WTClient:
    """
    Client for the WhisperTrade API.
    To initialize, provide a valid API token. Endpoint can be customized if needed e.g. proxy server etc.
    """

    def __init__(self, token: str, auto_init: bool = True, endpoint: str = ENDPOINT):
        """
        :param token: API token obtained from WhisperTrade
        :param auto_init: Defaults to True. If True, will automatically query and cache all information about the account that the token has access to.
        :param endpoint: Optional, defaults to https://api.whispertrades.com/v1/, only for debugging or proxying purposes.
        """
        self.token = token
        self.endpoint = endpoint
        self.headers = {'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {self.token}'}
        self._bots: dict[str, Bot] = {}

        if auto_init:
            self.__get_bots(include_details=True)

    @property
    def bots(self) -> dict[str, Bot]:
        """Returns a list of Bot objects that was cached by the previous call to get_bots(). To refresh, call get_bots() again. If get_bots() was never called, accessing this attribute will call get_bots() and return the result."""
        if not self._bots:
            self.__get_bots(include_details=True)
        return self._bots

    def __get_bots(self, bot_number: str = '', statuses: list = None, include_details: bool = False) -> dict[str, Bot]:
        payload = {}
        if isinstance(bot_number, int):
            bot_number = str(bot_number)
        valid_statuses = ["Enabled", "Disabled", "Disable on Close"]
        if statuses:
            for status in statuses:
                if status not in valid_statuses:
                    raise ValueError(f"Invalid status: {status}. Valid status are {valid_statuses}")
            payload['statuses'] = statuses
        if include_details:
            payload['include_details'] = include_details
        response = requests.get(f"{self.endpoint}bots/{bot_number}", headers=self.headers, params=payload)
        response = BaseResponse(**orjson.loads(response.text))
        if response.success:
            for bot_data in response.data:
                if bot_data['name'] == 'test':
                    print(bot_data)
                bot = Bot(BotResponse(**bot_data))
                self._bots[bot.number] = bot
            return self.bots
        else:
            raise APIError(response.message)

    def get_bots(self, statuses: list = None, include_details: bool = False) -> dict[str, Bot]:
        """
        Get information of all bots
        :param statuses: Optional, list of statuses to filter by, valid values are "Enabled", "Disabled", "Disable on Close"
        :param include_details: Optional, defaults to False.
        """
        return self.__get_bots(statuses=statuses, include_details=include_details)

    def get_bot(self, bot_number: Union[int, str], statuses: list = None, include_details: bool = True):
        """
        Get information of a bot by number
        :param bot_number: e.g. BYZ8UNMX8M
        :param statuses: Optional, list of statuses to filter by, valid values are "Enabled", "Disabled", "Disable on Close"
        :param include_details: Optional, defaults to True.
        """
        self.__get_bots(bot_number=bot_number, statuses=statuses, include_details=include_details)
        return self.bots[bot_number]
