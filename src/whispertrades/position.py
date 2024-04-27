from datetime import date, datetime
from typing import Literal, Optional, TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from . import WTClient
from .bot import BasicBot as Bot, BrokerConnection


class PositionLeg(BaseModel):
    status: Literal['OPEN', 'CLOSED']
    type: Literal['CALL', 'PUT']
    action: Literal['SELL_TO_OPEN', 'BUY_TO_OPEN', 'BUY_TO_CLOSE', 'SELL_TO_CLOSE']
    instrument: str
    expiration_date: date
    days_to_expiration: int
    days_to_expiration_at_exit: Optional[int]
    strike_price: float
    quantity: int
    quantity_open: int
    entered_at: datetime
    exited_at: Optional[datetime]
    entry_bid: float
    entry_ask: float
    entry_price: float
    exit_bid: Optional[float]
    exit_ask: Optional[float]
    exit_price: Optional[float]
    current_bid: Optional[float]
    current_mid: Optional[float]
    current_ask: Optional[float]
    current_profit: Optional[float]
    current_delta: Optional[float]
    profit_dollars: Optional[float]
    delta_at_entry: float
    delta_at_exit: Optional[float]
    iv_at_entry: float
    iv_at_exit: Optional[float]
    held_to_expiration: Optional[bool]
    assigned: Optional[bool]
    exercised: Optional[bool]


class PositionResponse(BaseModel):
    number: str
    status: Literal['OPEN', 'CLOSED']
    bot: Bot
    broker_connection: BrokerConnection
    is_paper: bool
    tags: str
    symbol: str
    type: str
    entered_at: datetime
    exited_at: Optional[datetime]
    entry_bid: float
    entry_ask: float
    entry_price: float
    exit_bid: Optional[float]
    exit_ask: Optional[float]
    exit_price: Optional[float]
    broker_fee: Optional[float]
    current_bid: Optional[float]
    current_mid: Optional[float]
    current_ask: Optional[float]
    current_profit: Optional[float]
    current_delta: Optional[float]
    entry_value: float
    exit_value: Optional[float]
    max_risk: float
    profit_dollars: Optional[float]
    starting_balance: float
    ending_balance: Optional[float]
    underlying_at_entry: float
    underlying_at_exit: Optional[float]
    vix_at_entry: float
    vix_at_exit: Optional[float]
    legs: list[PositionLeg]


class Position:
    def __init__(self, data: PositionResponse, client: 'WTClient', auto_refresh: bool):
        self._PositionResponse = data
        self.client = client
        self.auto_refresh = auto_refresh

        self.number = data.number
        self.status = data.status
        self.bot = data.bot
        self.broker_connection = data.broker_connection
        self.is_paper = data.is_paper
        self.tags = data.tags
        self.symbol = data.symbol
        self.type = data.type
        self.entered_at = data.entered_at
        self.exited_at = data.exited_at
        self.entry_bid = data.entry_bid
        self.entry_ask = data.entry_ask
        self.entry_price = data.entry_price
        self.exit_bid = data.exit_bid
        self.exit_ask = data.exit_ask
        self.exit_price = data.exit_price
        self.broker_fee = data.broker_fee
        self.current_bid = data.current_bid
        self.current_mid = data.current_mid
        self.current_ask = data.current_ask
        self.current_profit = data.current_profit
        self.current_delta = data.current_delta
        self.entry_value = data.entry_value
        self.exit_value = data.exit_value
        self.max_risk = data.max_risk
        self.profit_dollars = data.profit_dollars
        self.starting_balance = data.starting_balance
        self.ending_balance = data.ending_balance
        self.underlying_at_entry = data.underlying_at_entry
        self.underlying_at_exit = data.underlying_at_exit
        self.vix_at_entry = data.vix_at_entry
        self.vix_at_exit = data.vix_at_exit
        self.legs = data.legs

    def close(self):  # TODO: test when market open
        """
        Close this specific bot position. This is only valid during market hours and while the bot is set to Enabled or Disable on Close.
        Auth Required: Write Positions
        """
        response = self.client.session.put(f"{self.client.endpoint}bots/positions/{self.number}/close", headers=self.client.headers)
        response = BaseResponse(**orjson.loads(response.text))
        if response.success:
            self.__init__(PositionResponse(**response.data), self.client, self.auto_refresh)
            return response.message
        else:
            raise APIError(response.message)

    def __repr__(self) -> str:
        if self.auto_refresh:
            self.client.get_position(self.number)
        return str(self._PositionResponse)

    def __getattribute__(self, name):
        if not name.endswith('Response') and name not in ['number', 'broker_order_number', 'bot', 'is_paper'] and name in self._PositionResponse.model_fields and self.auto_refresh:
            self.client.get_position(self.number)
        return super().__getattribute__(name)
