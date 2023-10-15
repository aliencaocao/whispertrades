from datetime import date
from typing import Literal, Union

import orjson
from requests import Session
from requests_ratelimiter import LimiterAdapter

from .bot import Bot, BotResponse
from .common import APIError, BaseResponse
from .order import Order, OrderResponse

__version__ = '0.1.0'
__author__ = 'Billy Cao'
ENDPOINT = 'https://api.whispertrades.com/v1/'


class WTClient:
    """
    Client for the WhisperTrade API.
    To initialize, provide a valid API token. Endpoint can be customized if needed e.g. proxy server etc.
    """

    def __init__(self, token: str, auto_init: bool = True, auto_refresh: bool = True, session: Session = None, endpoint: str = ENDPOINT):
        """
        :param token: API token obtained from WhisperTrade
        :param auto_init: Defaults to True. If True, will automatically query and cache all information about the account that the token has access to. This can be slow.
        :param auto_refresh: Defaults to True. If True, will automatically refresh the attribute on each access. This can be slow. If you do not anticipate them changing often, set this to False. You can also call the respective refresh methods manually.
        :param session: Provide your own requests Session object if needed. Defaults to a new session. Rate limiting will be applied on this session.
        :param endpoint: Optional, defaults to https://api.whispertrades.com/v1/, only for debugging or proxying purposes.
        """
        self.token = token
        self.endpoint = endpoint
        self.auto_refresh = auto_refresh
        self.session = session or Session()
        self.session.mount(self.endpoint, LimiterAdapter(per_minute=30, burst=0))
        self.headers = {'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {self.token}'}
        self._bots: dict[str, Bot] = {}
        self._orders: dict[str, Order] = {}

        if auto_init:
            self.__get_bots(include_details=True)
            self.__get_orders()

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
        response = self.session.get(f"{self.endpoint}bots/{bot_number}", headers=self.headers, params=payload)
        response = BaseResponse(**orjson.loads(response.text))
        if response.success:
            if isinstance(response.data, dict):
                response.data = [response.data]
            for bot_data in response.data:
                bot = Bot(BotResponse(**bot_data), self, self.auto_refresh)
                if bot.number in self._bots:
                    self._bots[bot.number].__dict__.update(bot.__dict__)  # copy the already cached data
                self._bots[bot.number] = bot
            return self._bots
        else:
            raise APIError(response.message)

    def get_bots(self, statuses: list = None, include_details: bool = False) -> dict[str, Bot]:
        """
        Get information of all bots
        :param statuses: Optional, list of statuses to filter by, valid values are "Enabled", "Disabled", "Disable on Close"
        :param include_details: Optional, defaults to False.
        """
        return self.__get_bots(statuses=statuses, include_details=include_details)

    def get_bot(self, bot_number: str, include_details: bool = True):
        """
        Get information of a bot by number
        :param bot_number: e.g. BYZ8UNMX8M
        :param include_details: Optional, defaults to True.
        """
        self.__get_bots(bot_number=bot_number, include_details=include_details)
        return self.bots[bot_number]

    @property
    def bots(self) -> dict[str, Bot]:
        """Returns a list of Bot objects that was cached by the previous call to get_bots(). To refresh, call get_bots() again (not needed if auto_refresh was set to True). If get_bots() was never called, accessing this attribute will call get_bots() and return the result."""
        if not self._bots or self.auto_refresh:
            self.__get_bots(include_details=True)
        return self._bots

    def __get_orders(self, number: str = '', bot: Union[Bot, str] = None, status: Literal["WORKING", "FILLED", "CANCELED"] = None, from_date: date = None, to_date: date = None, page: int = None) -> dict[str, Order]:
        payload = {}
        if bot:
            if isinstance(bot, Bot):
                bot_number = bot.number + '/'
            elif isinstance(bot, str):
                bot_number = str(bot) + '/'
            else:
                raise TypeError(f"Invalid type for bot, expected Bot or str, got {type(bot)}")
        else:
            bot_number = ''
        if status:
            status = status.upper()
            if status not in ["WORKING", "FILLED", "CANCELED"]:  # TODO: check if EXPIRED is valid
                raise ValueError(f"Invalid status: {status}. Valid status are WORKING, FILLED, CANCELED")
            payload['status'] = status
        if from_date:
            payload['from_date'] = from_date
        if to_date:
            payload['to_date'] = to_date
        if page is not None:
            if not isinstance(page, int):
                raise TypeError(f"Invalid type for page, expected int, got {type(page)}")
            payload['page'] = max(1, page)

        def request(payload):
            response = self.session.get(f"{self.endpoint}bots/{bot_number}orders/{number}", headers=self.headers, params=payload)
            response = BaseResponse(**orjson.loads(response.text))
            if response.success:
                for order_data in response.data:
                    order = Order(OrderResponse(**order_data), self)
                    self._orders[order.number] = order
                    if order.bot.number not in self._bots:
                        print(order.bot.number)
                        self.get_bot(order.bot.number, include_details=False)
                    self._bots[order.bot.number]._orders[order.number] = order
                return response.data
            else:
                raise APIError(response.message)

        r = request(payload)
        if page is None and len(r) < 100:  # get all pages
            complete = False
            payload['page'] = 2
            while not complete:
                r = request(payload)
                if len(r) < 100:
                    complete = True
                else:
                    payload['page'] += 1
        return self._orders

    def get_orders(self, bot: Union[Bot, str] = None, status: Literal["WORKING", "FILLED", "CANCELED"] = None, from_date: date = None, to_date: date = None, page: int = None) -> dict[str, Order]:
        """
        Get orders, optionally filter by bot, status, date, page.
        :param bot: Optional, filter by bot number or Bot instance. If empty, do not filter.
        :param status: Optional, filter by status, valid values are WORKING, FILLED, CANCELED. If empty, do not filter.
        :param from_date: Optional, filter by date. If empty, do not filter.
        :param to_date: Optional, filter by date. If empty, do not filter.
        :param page: Optional, defaults to None. If provided, will return orders on that page. If empty, return all pages. Each page is 100 orders.
        """
        return self.__get_orders(bot=bot, status=status, from_date=from_date, to_date=to_date, page=page)

    def get_order(self, number: str):
        """
        Get order by number
        :param number: e.g. GZH7QT03FD
        """
        return self.__get_orders(number=number)

    @property
    def orders(self) -> dict[str, Order]:
        """Returns a list of Order objects that was cached by the previous call to get_orders(). To refresh, call get_orders() again (not needed if auto_refresh was set to True). If get_orders() was never called, accessing this attribute will call get_orders() and return the result."""
        if not self._orders or self.auto_refresh:
            self.__get_orders()
        return self._orders
