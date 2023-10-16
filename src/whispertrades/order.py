from datetime import datetime
from typing import Literal, Optional, TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from . import WTClient


class Bot(BaseModel):
    name: str
    number: str


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
    bid: float
    mid: Optional[float]
    ask: float
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
    def __init__(self, data: OrderResponse, client: 'WTClient'):
        self._OrderResponse = data
        self.client = client

        self.number = data.number
        self.broker_order_number = data.broker_order_number
        self.status = data.status
        self.type = data.type
        self.duration = data.duration
        self.bot = data.bot
        self.is_paper = data.is_paper
        self.symbol = data.symbol
        self.original_quantity = data.original_quantity
        self.current_quantity = data.current_quantity
        self.filled_quantity = data.filled_quantity
        self.order_price = data.order_price
        self.fill_price = data.fill_price
        self.broker_fee = data.broker_fee
        self.submitted_at = data.submitted_at
        self.filled_at = data.filled_at
        self.canceled_at = data.canceled_at
        self.legs = data.legs
        self.submissions = data.submissions
        self.fills = data.fills

    def __repr__(self) -> str:
        return str(self._OrderResponse)
