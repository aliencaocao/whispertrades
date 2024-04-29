from datetime import datetime
from typing import Literal, Optional, TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from . import WTClient
from .bot import BasicBot as Bot


class Leg(BaseModel):
    number: int
    type: Literal["CALL", "PUT"]
    instrument: str
    expiration_date: datetime
    strike_price: float
    instruction: Literal["SELL_TO_OPEN", "BUY_TO_OPEN", "BUY_TO_CLOSE", "SELL_TO_CLOSE"]
    quantity: int
    bid: float
    mid: float
    ask: float


class Submission(BaseModel):
    quantity: Optional[int]
    price: float
    bid: Optional[float]
    mid: Optional[float]
    ask: Optional[float]
    submitted_at: datetime


class Fill(BaseModel):
    leg_number: int
    quantity: int
    price: float
    filled_at: datetime
    bid: float
    mid: float
    ask: float


class OrderResponse(BaseModel):
    number: str
    broker_order_number: str
    status: Literal["WORKING", "FILLED", "CANCELED", "EXPIRED", "REJECTED"]
    type: Literal["OPENING", "CLOSING"]
    duration: Literal["GTC", "DAY"]
    bot: Bot
    is_paper: bool
    symbol: str
    original_quantity: int
    current_quantity: int
    filled_quantity: int
    order_price: float
    fill_price: Optional[float]
    broker_fee: Optional[float]
    submitted_at: datetime
    filled_at: Optional[datetime]
    canceled_at: Optional[datetime]
    legs: list[Leg]
    submissions: list[Optional[Submission]]
    fills: list[Optional[Fill]]


class Order:
    def __init__(self, data: OrderResponse, client: 'WTClient', auto_refresh: bool):
        self._OrderResponse: OrderResponse = data  #: raw response data from API
        self.client: 'WTClient' = client  #: the WTClient object that created this instance
        self.auto_refresh: bool = auto_refresh  #: auto_refresh toggle inherited from WTClient

        self.number: str = data.number  #: Order number
        self.broker_order_number: str = data.broker_order_number  #: Broker order number
        self.status: Literal["WORKING", "FILLED", "CANCELED", "EXPIRED", "REJECTED"] = data.status  #: Order status
        self.type: Literal["OPENING", "CLOSING"] = data.type  #: Order type
        self.duration: Literal["GTC", "DAY"] = data.duration  #: Order duration
        self.bot: Bot = data.bot  #: Bot object
        self.is_paper: bool = data.is_paper  #: If this is a paper order
        self.symbol: str = data.symbol  #: Symbol of the order
        self.original_quantity: int = data.original_quantity  #: Original quantity of the order
        self.current_quantity: int = data.current_quantity  #: Current quantity of the order
        self.filled_quantity: int = data.filled_quantity  #: Filled quantity of the order
        self.order_price: float = data.order_price  #: Order price
        self.fill_price: Optional[float] = data.fill_price  #: Fill price
        self.broker_fee: Optional[float] = data.broker_fee  #: Broker fee
        self.submitted_at: datetime = data.submitted_at  #: Submitted at
        self.filled_at: Optional[datetime] = data.filled_at  #: Filled at
        self.canceled_at: Optional[datetime] = data.canceled_at  #: Canceled at
        self.legs: List[Leg] = data.legs  #: Legs of the order
        self.submissions: List[Optional[Submission]] = data.submissions  #: Submissions of the order
        self.fills: List[Optional[Fill]] = data.fills  #: Fills of the order

    def __repr__(self) -> str:
        return f'<Order {self._OrderResponse}>'

    def __getattribute__(self, name):
        if not name.endswith('Response') and name not in ['number', 'broker_order_number', 'bot', 'is_paper'] and name in self._OrderResponse.model_fields and self.auto_refresh:
            self.client.get_order(self.number)
        return super().__getattribute__(name)
