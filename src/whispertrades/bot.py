from datetime import datetime, time
from typing import Literal, Optional, TYPE_CHECKING

from pydantic import BaseModel, field_validator

if TYPE_CHECKING:
    from . import WTClient
from .order import Order
from .common import APIError, BaseResponse
from .variable import BaseVariable

import orjson


class BrokerConnection(BaseModel):
    name: Optional[str]
    number: str
    account_number: str


class DayOfWeek(BaseModel):
    days_of_week: str

    @field_validator('days_of_week')
    def validate_days_of_week(cls, days_of_week: str):
        valid_values = ["All", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for day in days_of_week.split(', '):
            if day not in valid_values:
                raise ValueError(f"Invalid day of the week: {day}")
        return days_of_week


class BotVariable(BaseVariable):
    condition: Literal["Contains", "Equal To", "Not Equal To", "Less Than", "Greater Than"] = None
    bot_value_to_set: Optional[Literal[
        "Free Text",
        "Bot Open Position Count",
        "Bot Positions Entered Today Count",
        "Bot Positions Exited Today Count",
        "Bot Current Position Delta",
        "Bot Current Position MID Price",
        "Bot Current Position Minutes in Trade",
        "Bot Current Position Days in Trade",
        "Bot Current Position Minutes to Expiration",
        "Bot Current Position DTE",
        "Bot Current Position Profit $",
        "Bot Current Position Profit %",
        "Bot Last Closed Position Today Profit $",
        "Bot Profit Realized Today $"
    ]] = None


class EntryCondition(BaseModel):
    allocation_type: Literal["Leverage Amount", "Contract Quantity", "Percent of Portfolio"]
    contract_quantity: Optional[int]
    percent_of_portfolio: Optional[float]
    leverage_amount: Optional[float]
    entry_speed: Literal["Patient", "Normal", "Aggressive"]
    maximum_entries_per_day: int
    earliest_time_of_day: Optional[time]
    latest_time_of_day: Optional[time]
    days_of_week: DayOfWeek
    minutes_between_positions: int
    minimum_starting_premium: Optional[str]
    maximum_starting_premium: Optional[str]
    minimum_days_to_expiration: int
    target_days_to_expiration: int
    maximum_days_to_expiration: int
    minimum_underlying_percent_move_from_close: Optional[str]
    maximum_underlying_percent_move_from_close: Optional[str]
    same_day_re_entry: Optional[Literal["Profit", "Loss"]]
    avoid_fomc: Optional[str]
    move_strike_selection_with_conflict: bool
    variables: list[Optional[BotVariable]]
    call_short_strike_type: Optional[Literal["Delta", "Premium"]]
    call_short_strike_minimum_delta: Optional[float]
    call_short_strike_target_delta: Optional[float]
    call_short_strike_maximum_delta: Optional[float]
    call_short_strike_minimum_premium: Optional[str]
    call_short_strike_target_premium: Optional[str]
    call_short_strike_maximum_premium: Optional[str]
    call_long_strike_type: Optional[Literal["Delta", "Premium"]]
    call_long_strike_minimum_delta: Optional[float]
    call_long_strike_target_delta: Optional[float]
    call_long_strike_maximum_delta: Optional[float]
    call_long_strike_minimum_premium: Optional[str]
    call_long_strike_target_premium: Optional[str]
    call_long_strike_maximum_premium: Optional[str]
    call_spread_minimum_width_points: Optional[float]
    call_spread_target_width_points: Optional[float]
    call_spread_maximum_width_points: Optional[float]
    call_spread_minimum_width_percent: Optional[str]
    call_spread_target_width_percent: Optional[str]
    call_spread_maximum_width_percent: Optional[str]
    call_spread_strike_target_delta: Optional[float]
    call_spread_strike_target_premium: Optional[str]
    restrict_call_spread_width_by: Optional[Literal["Points", "Percent"]]
    call_spread_smart_width: bool
    put_short_strike_type: Optional[Literal["Delta", "Premium"]]
    put_short_strike_minimum_delta: Optional[float]
    put_short_strike_target_delta: Optional[float]
    put_short_strike_maximum_delta: Optional[float]
    put_short_strike_minimum_premium: Optional[str]
    put_short_strike_target_premium: Optional[str]
    put_short_strike_maximum_premium: Optional[str]
    put_long_strike_type: Optional[Literal["Delta", "Premium"]]
    put_long_strike_minimum_delta: Optional[float]
    put_long_strike_target_delta: Optional[float]
    put_long_strike_maximum_delta: Optional[float]
    put_long_strike_minimum_premium: Optional[str]
    put_long_strike_target_premium: Optional[str]
    put_long_strike_maximum_premium: Optional[str]
    put_spread_minimum_width_points: Optional[float]
    put_spread_target_width_points: Optional[float]
    put_spread_maximum_width_points: Optional[float]
    put_spread_minimum_width_percent: Optional[str]
    put_spread_target_width_percent: Optional[str]
    put_spread_maximum_width_percent: Optional[str]
    put_spread_strike_target_delta: Optional[float]
    put_spread_strike_target_premium: Optional[str]
    restrict_put_spread_width_by: Optional[Literal["Points", "Percent"]]
    put_spread_smart_width: bool

    @field_validator('days_of_week', mode='before', check_fields=True)
    def __convert_days_of_week(cls, value):
        if isinstance(value, str):
            return DayOfWeek(**{'days_of_week': value})
        elif isinstance(value, dict):
            return DayOfWeek(**value)
        elif isinstance(value, DayOfWeek):
            return value
        else:
            raise ValueError(f"Invalid days_of_week type: must be DayOfWeek or dict, got {type(value)}")


class ExitCondition(BaseModel):
    exit_speed: Literal["Super Patient", "Patient", "Normal", "Aggressive", "Super Aggressive"]
    profit_premium_value: Optional[str]
    profit_target_percent: Optional[str]
    stop_loss_percent: Optional[str]
    loss_premium_value: Optional[str]
    itm_percent_stop: Optional[str]
    delta_stop: Optional[float]
    monitored_stop_sensitivity: Literal["Patient", "Normal", "Aggressive"]
    trail_profit_percent_trigger: Optional[str]
    trail_profit_percent_amount: Optional[str]
    trail_profit_premium_trigger: Optional[str]
    trail_profit_premium_amount: Optional[str]
    variables: list[Optional[BotVariable]]
    close_short_strike_only: bool
    sell_abandoned_long_strike: bool


class Adjustment(BaseModel):
    number: str
    status: str
    type: str
    days_of_week: DayOfWeek
    days_to_expiration: int
    time_of_day: time
    minimum_position_delta: Optional[str]
    maximum_position_delta: Optional[str]
    minimum_position_profit_percent: Optional[str]
    maximum_position_profit_percent: Optional[str]
    minimum_underlying_percent_move_from_close: Optional[str]
    maximum_underlying_percent_move_from_close: Optional[str]
    variables: list[Optional[BotVariable]]

    @field_validator('days_of_week', mode='before', check_fields=True)
    def __convert_days_of_week(cls, value):
        if isinstance(value, str):
            return DayOfWeek(**{'days_of_week': value})
        elif isinstance(value, dict):
            return DayOfWeek(**value)
        elif isinstance(value, DayOfWeek):
            return value
        else:
            raise ValueError(f"Invalid days_of_week type: must be DayOfWeek or dict, got {type(value)}")


class Notification(BaseModel):
    number: str
    event: Literal[
        "Order Placed",
        "Order Filled",
        "Order Canceled",
        "Position % In-the-Money",
        "Position % Loss",
        "Position % Profit",
        "Position Days to Expiration",
        "Position Delta (Loss)",
        "Position Expired"
    ]
    type: Literal["Email"]


class BotResponse(BaseModel):
    number: str
    name: str
    broker_connection: BrokerConnection
    is_paper: bool
    status: Literal["Enabled", "Disabled", "Disable on Close"]
    can_enable: bool
    can_disable: bool
    symbol: str
    type: str
    notes: Optional[str]
    last_active_at: Optional[datetime]
    disabled_at: Optional[datetime]
    entry_condition: EntryCondition = None
    exit_condition: ExitCondition = None
    adjustments: list[Optional[Adjustment]] = None
    notifications: list[Optional[Notification]] = None
    variables: list[Optional[BotVariable]] = None


def toCamalCase(s: str) -> str:
    return s.replace('_', ' ').title().replace(' ', '')


class Bot:
    def __init__(self, data: BotResponse, client: 'WTClient', auto_refresh: bool = True):
        self._BotResponse = data
        self.client = client
        self.auto_refresh = auto_refresh

        self.number: str = data.number
        self.name: str = data.name
        self.broker_connection: BrokerConnection = data.broker_connection
        self.is_paper: bool = data.is_paper
        self.status: Literal["Enabled", "Disabled", "Disable on Close"] = data.status
        self.can_enable: bool = data.can_enable
        self.can_disable: bool = data.can_disable
        self.symbol: str = data.symbol
        self.type: str = data.type
        self.notes: Optional[str] = data.notes
        self.last_active_at: Optional[datetime] = data.last_active_at
        self.disabled_at: Optional[datetime] = data.disabled_at
        self.entry_condition: EntryCondition = data.entry_condition
        self.exit_condition: ExitCondition = data.exit_condition
        self.adjustments: list[Optional[Adjustment]] = data.adjustments
        self.notifications: list[Optional[Notification]] = data.notifications
        self.variables: list[Optional[BotVariable]] = data.variables

        self.endpoint = f'{self.client.endpoint}bots/{self.number}/'

        self._orders: dict[str, Order] = {}

    def __repr__(self):
        return f'<Bot {self.number} - {self.name}>'

    def enable(self):
        response = requests.put(self.endpoint + 'enable', headers=self.client.headers)
        response = BaseResponse(**orjson.loads(response.text))
        if not response.success:
            raise APIError(response.message)

    def disable(self):
        response = requests.put(self.endpoint + 'disable', headers=self.client.headers)
        response = BaseResponse(**orjson.loads(response.text))
        if not response.success:
            raise APIError(response.message)

    @property
    def orders(self) -> dict[str, Order]:
        if not self._orders or self.auto_refresh:
            orders = self.client.get_orders(bot=self)
            self._orders.update(orders)
        return self._orders

    @property
    def positions(self):
        return

    @property
    def reports(self):
        return
