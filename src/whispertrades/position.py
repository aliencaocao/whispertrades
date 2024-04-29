from datetime import date, datetime
from typing import Literal, Optional, TYPE_CHECKING

import orjson
from pydantic import BaseModel

if TYPE_CHECKING:
    from . import WTClient
from .bot import BasicBot as Bot, BrokerConnection
from .common import APIError, BaseResponse


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
        self._PositionResponse: PositionResponse = data  #: raw response data from API
        self.client: 'WTClient' = client  #: the WTClient object that created this instance
        self.auto_refresh: bool = auto_refresh  #: auto_refresh toggle inherited from WTClient

        self.number: str = data.number  #: Position number
        self.status: Literal['OPEN', 'CLOSED'] = data.status  #: Position status
        self.bot: Bot = data.bot  #: Bot object
        self.broker_connection: BrokerConnection = data.broker_connection  #: Broker connection
        self.is_paper: bool = data.is_paper  #: If this is a paper position
        self.tags: str = data.tags  #: Tags
        self.symbol: str = data.symbol  #: Symbol
        self.type: str = data.type  #: Type
        self.entered_at: datetime = data.entered_at  #: Entered at
        self.exited_at: Optional[datetime] = data.exited_at  #: Exited at
        self.entry_bid: float = data.entry_bid  #: Entry bid
        self.entry_ask: float = data.entry_ask  #: Entry ask
        self.entry_price: float = data.entry_price  #: Entry price
        self.exit_bid: Optional[float] = data.exit_bid  #: Exit bid
        self.exit_ask: Optional[float] = data.exit_ask  #: Exit ask
        self.exit_price: Optional[float] = data.exit_price  #: Exit price
        self.broker_fee: Optional[float] = data.broker_fee  #: Broker fee
        self.current_bid: Optional[float] = data.current_bid  #: Current bid
        self.current_mid: Optional[float] = data.current_mid  #: Current mid
        self.current_ask: Optional[float] = data.current_ask  #: Current ask
        self.current_profit: Optional[float] = data.current_profit  #: Current profit
        self.current_delta: Optional[float] = data.current_delta  #: Current delta
        self.entry_value: float = data.entry_value  #: Entry value
        self.exit_value: Optional[float] = data.exit_value  #: Exit value
        self.max_risk: float = data.max_risk  #: Max risk
        self.profit_dollars: Optional[float] = data.profit_dollars  #: Profit dollars
        self.starting_balance: float = data.starting_balance  #: Starting balance
        self.ending_balance: Optional[float] = data.ending_balance  #: Ending balance
        self.underlying_at_entry: float = data.underlying_at_entry  #: Underlying at entry
        self.underlying_at_exit: Optional[float] = data.underlying_at_exit  #: Underlying at exit
        self.vix_at_entry: float = data.vix_at_entry  #: VIX at entry
        self.vix_at_exit: Optional[float] = data.vix_at_exit  #: VIX at exit
        self.legs: List[PositionLeg] = data.legs  #: Legs

    def close(self):
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
        return f'<Position {self._PositionResponse}>'

    def __getattribute__(self, name):
        if not name.endswith('Response') and name not in ['number', 'broker_order_number', 'bot', 'is_paper'] and name in self._PositionResponse.model_fields and self.auto_refresh:
            self.client.get_position(self.number)
        return super().__getattribute__(name)
