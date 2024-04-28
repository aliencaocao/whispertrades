from datetime import date
from typing import Literal, Union

import orjson
from requests import Session
from requests_ratelimiter import LimiterAdapter

from .bot import Bot, BotResponse
from .common import APIError, BaseResponse, UpdatingDict
from .order import Order, OrderResponse
from .position import Position, PositionResponse
from .report import Report, ReportResponse
from .variable import Variable, VariableResponse

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
        :param auto_refresh: Defaults to True. If True, will automatically refresh the attribute on each access (excluding prints). This can be slow and may trigger rate limit. If you do not anticipate them changing often, set this to False. You can also call the respective refresh methods manually e.g. get_orders().
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
        self._variables: dict[str, Variable] = {}
        self._positions: dict[str, Position] = {}
        self._reports: UpdatingDict[str, Report] = UpdatingDict(update_fn=self.__get_reports_raw if self.auto_refresh else None)

        if auto_init:
            self.__get_bots(include_details=True)
            self.__get_orders()
            self.__get_variables()
            self.__get_positions()
            self.__get_reports()

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
        # print(orjson.loads(response.text))  # for debugging
        response = BaseResponse(**orjson.loads(response.text))
        if response.success:
            if isinstance(response.data, dict):
                response.data = [response.data]
            for bot_data in response.data:
                bot = Bot(BotResponse(**bot_data), self, self.auto_refresh)
                if bot.number in self._bots:
                    self._bots[bot.number].__dict__.update(bot.__dict__)  # copy the already cached data
                else:
                    self._bots[bot.number] = bot
            return self._bots
        else:
            raise APIError(response.message)

    def get_bots(self, statuses: list = None, include_details: bool = False) -> dict[str, Bot]:
        """
        Get information of all bots
        Auth Required: Read Bots
        :param statuses: Optional, list of statuses to filter by, valid values are "Enabled", "Disabled", "Disable on Close"
        :param include_details: Optional, defaults to False.
        """
        return self.__get_bots(statuses=statuses, include_details=include_details)

    def get_bot(self, bot_number: str, include_details: bool = True):
        """
        Get information of a bot by number
        Auth Required: Read Bots
        :param bot_number: e.g. BYZ8UNMX8M
        :param include_details: Optional, defaults to True.
        """
        self.__get_bots(bot_number=bot_number, include_details=include_details)
        return self._bots[bot_number]

    @property
    def bots(self) -> dict[str, Bot]:
        """
        Returns a list of Bot objects that was cached by the previous call to get_bots(). To refresh, call get_bots() again (not needed if auto_refresh was set to True). If get_bots() was never called, accessing this attribute will call get_bots() and return the result.
        Auth Required: Read Bots
        """
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
            if status not in ["WORKING", "FILLED", "CANCELED", "EXPIRED", "REJECTED"]:
                raise ValueError(f"Invalid status: {status}. Valid statuses are WORKING, FILLED, CANCELED, EXPIRED, REJECTED")
            payload['status'] = status
        if from_date:
            payload['from_date'] = from_date.strftime('%Y-%m-%d')
        if to_date:
            payload['to_date'] = to_date.strftime('%Y-%m-%d')
        if page is not None:
            if not isinstance(page, int):
                raise TypeError(f"Invalid type for page, expected int, got {type(page)}")
            payload['page'] = max(1, page)

        def request(payload):
            response = self.session.get(f"{self.endpoint}bots/{bot_number}orders/{number}", headers=self.headers, params=payload)
            response = BaseResponse(**orjson.loads(response.text))
            if response.success:
                if isinstance(response.data, dict):
                    response.data = [response.data]
                for order_data in response.data:
                    order = Order(OrderResponse(**order_data), self, self.auto_refresh)
                    if order.number in self._orders:
                        self._orders[order.number].__dict__.update(order.__dict__)
                    else:
                        self._orders[order.number] = order
                    if order.bot.number not in self._bots:
                        self.get_bot(order.bot.number, include_details=False)
                    self._bots[order.bot.number]._orders[order.number] = order
                return response.data
            else:
                raise APIError(response.message)

        r = request(payload)
        if page is None and len(r) == 100:  # get all pages
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
        Auth Required: Read Orders
        :param bot: Optional, filter by bot number or Bot instance. If empty, do not filter.
        :param status: Optional, filter by status, valid values are WORKING, FILLED, CANCELED, EXPIRED, REJECTED. If empty, do not filter.
        :param from_date: Optional, filter by date. If empty, do not filter.
        :param to_date: Optional, filter by date. If empty, do not filter.
        :param page: Optional, defaults to None. If provided, will return orders on that page. If empty, return all pages. Each page is 100 orders. Sorted from newest to oldest.
        """
        return self.__get_orders(bot=bot, status=status, from_date=from_date, to_date=to_date, page=page)

    def get_order(self, number: str) -> Order:
        """
        Get order by number
        Auth Required: Read Orders
        :param number: e.g. GZH7QT03FD
        """
        self.__get_orders(number=number)
        return self._orders[number]

    @property
    def orders(self) -> dict[str, Order]:
        """Returns a list of Order objects that was cached by the previous call to get_orders(). To refresh, call get_orders() again (not needed if auto_refresh was set to True). If get_orders() was never called, accessing this attribute will call get_orders() and return the result."""
        if not self._orders or self.auto_refresh:
            self.__get_orders()
        return self._orders

    def __get_variables(self, number: str = '') -> dict[str, Variable]:
        response = self.session.get(f"{self.endpoint}bots/variables/{number}", headers=self.headers)
        # print(orjson.loads(response.text))  # for debugging
        response = BaseResponse(**orjson.loads(response.text))
        if response.success:
            if isinstance(response.data, dict):
                response.data = [response.data]
            for variable_data in response.data:
                variable = Variable(VariableResponse(**variable_data), self, self.auto_refresh)
                if variable.number in self._variables:
                    self._variables[variable.number].__dict__.update(variable.__dict__)
                else:
                    self._variables[variable.number] = variable
            return self._variables
        else:
            raise APIError(response.message)

    def get_variables(self) -> dict[str, Variable]:
        """
        Get all variables in this account
        Auth Required: Read Variables
        """
        return self.__get_variables()

    def get_variable(self, number: str) -> Variable:
        """
        Get variable by number
        Auth Required: Read Variables
        :param number: e.g. GZH7QT03FD
        """
        self.__get_variables(number=number)
        return self._variables[number]

    @property
    def variables(self) -> dict[str, Variable]:
        """Returns a list of Variable objects that was cached by the previous call to get_variables(). To refresh, call get_variables() again (not needed if auto_refresh was set to True). If get_variables() was never called, accessing this attribute will call get_variables() and return the result."""
        if not self._variables or self.auto_refresh:
            self.__get_variables()
        return self._variables

    def __get_positions(self, number: str = '', bot: Union[Bot, str] = None, status: Literal["OPEN", "CLOSE"] = None, from_date: date = None, to_date: date = None, page: int = None) -> dict[str, Position]:
        payload = {}
        if bot:
            if isinstance(bot, Bot):
                bot_number = bot.number + '/'
            elif isinstance(bot, str):
                bot_number = str(bot) + '/'
            else:
                raise TypeError(f"Invalid type for bot, expected Bot or str, got {type(bot)}")
            payload['bot'] = bot_number
        if status:
            status = status.upper()
            if status not in ["OPEN", "CLOSE"]:
                raise ValueError(f"Invalid status: {status}. Valid statuses are OPEN and CLOSE.")
            payload['status'] = status
        if from_date:
            payload['from_date'] = from_date.strftime('%Y-%m-%d')
        if to_date:
            payload['to_date'] = to_date.strftime('%Y-%m-%d')
        if page is not None:
            if not isinstance(page, int):
                raise TypeError(f"Invalid type for page, expected int, got {type(page)}")
            payload['page'] = max(1, page)

        def request(payload):
            response = self.session.get(f"{self.endpoint}bots/positions/{number}", headers=self.headers, params=payload)
            response = BaseResponse(**orjson.loads(response.text))
            if response.success:
                if isinstance(response.data, dict):
                    response.data = [response.data]
                for position_data in response.data:
                    position = Position(PositionResponse(**position_data), self, self.auto_refresh)
                    self._positions[position.number] = position
                    if position.bot.number not in self._bots:
                        self.get_bot(position.bot.number, include_details=False)
                    self._bots[position.bot.number]._positions[position.number] = position
                return response.data
            else:
                raise APIError(response.message)

        r = request(payload)
        if page is None and len(r) == 100:  # page=None means default to 1st page, and if first page gives 100 result, there may be more, so try get all pages
            complete = False
            payload['page'] = 2
            while not complete:
                r = request(payload)
                if len(r) < 100:
                    complete = True
                else:
                    payload['page'] += 1
        return self._positions

    def get_positions(self, bot: Union[Bot, str] = None, status: Literal["OPEN", "CLOSE"] = None, from_date: date = None, to_date: date = None, page: int = None) -> dict[str, Position]:
        """
        Get positions, optionally filter by bot, status, date, page.
        Auth Required: Read Positions
        :param bot: Optional, filter by bot number or Bot instance. If empty, do not filter.
        :param status: Optional, filter by status, valid values are OPEN and CLOSE. If empty, do not filter.
        :param from_date: Optional, filter by date. If empty, do not filter.
        :param to_date: Optional, filter by date. If empty, do not filter.
        :param page: Optional, defaults to None. If provided, will return positions on that page. If empty, return all pages. Each page is 100 orders. Sorted from newest to oldest.
        """
        return self.__get_positions(bot=bot, status=status, from_date=from_date, to_date=to_date, page=page)

    def get_position(self, number: str) -> Position:
        """
        Get position by number
        Auth Required: Read Positions
        :param number: e.g. GZH7QT03FD
        """
        self.__get_positions(number=number)
        return self._positions[number]

    @property
    def positions(self) -> dict[str, Position]:
        """Returns a list of Position objects that was cached by the previous call to get_positions(). To refresh, call get_positions() again (not needed if auto_refresh was set to True). If get_positions() was never called, accessing this attribute will call get_positions() and return the result."""
        if not self._positions or self.auto_refresh:
            self.__get_positions()
        return self._positions

    def __get_reports_raw(self, number: str = '', return_raw: bool = False) -> Report:
        if not number and not return_raw:
            raise ValueError("Report number is required if return_raw is False.")
        response = self.session.get(f"{self.endpoint}bots/reports/{number}", headers=self.headers)
        response = BaseResponse(**orjson.loads(response.text))
        report_data = response.data
        # print(report_data)  # for debugging
        if response.success:
            return report_data if return_raw else Report(ReportResponse(**report_data), self, self.auto_refresh)
        else:
            raise APIError(response.message)

    def __get_reports(self, number: str = ''):
        response_data = self.__get_reports_raw(number=number, return_raw=True)
        if isinstance(response_data, dict):
            response_data = [response_data]
        for report_data in response_data:
            report = Report(ReportResponse(**report_data), self, self.auto_refresh)
            self._reports[report.number] = report
        return self._reports

    def get_reports(self, detailed: bool = False) -> dict[str, Report]:
        """
        Get all reports in this account. Note that this will NOT return detailed return data for each report.
        Auth Required: Read Reports
        :param detailed: Optional, defaults to False. If True, will return detailed return data for each report. This can be very slow. It is recommended to use get_report() to get detailed data for a specific report if you do not need all of them at once.
        """
        self.__get_reports()
        if detailed:
            for report in self._reports.values():
                self.__get_reports(number=report.number)
        return self._reports

    def get_report(self, number: str) -> Report:
        """
        Get report by number. Note that this will return detailed return data.
        Auth Required: Read Reports
        :param number: e.g. GZH7QT03FD
        """
        if not self.auto_refresh: self.__get_reports(number=number)  # if auto refresh is enabled, accessing the key below already refreshes so do not request again
        return self._reports[number]

    @property
    def reports(self):
        if not self._reports:  # auto refresh is handled in UpdatingDict during client init
            self.__get_reports()
        return self._reports

    def __repr__(self):
        token_redacted = self.token[:4] + '...' + self.token[-4:]
        return f'<WTClient token={token_redacted} auto_refresh={self.auto_refresh} endpoint={self.endpoint}>'
