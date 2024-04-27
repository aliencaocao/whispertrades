from datetime import datetime, time
from typing import Literal, Optional, TYPE_CHECKING

from pydantic import BaseModel, field_validator

if TYPE_CHECKING:
    from . import WTClient
    from .order import Order
    from .position import Position
from .common import APIError, BaseResponse
from .variable import BaseVariable

import orjson


class BrokerConnection(BaseModel):
    name: Optional[str]
    number: str
    account_number: str


class DaysOfWeek(BaseModel):
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
        "Bot Current Position ITM %",
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
    frequency: Literal["Sequential", "Daily", "Weekly"]
    allocation_type: Literal["Leverage Amount", "Contract Quantity", "Percent of Portfolio"]
    contract_quantity: Optional[int]
    percent_of_portfolio: Optional[float]
    leverage_amount: Optional[float]
    long_call_ratio_quantity: Optional[int]
    short_call_ratio_quantity: Optional[int]
    long_put_ratio_quantity: Optional[int]
    short_put_ratio_quantity: Optional[int]
    entry_speed: Literal["Patient", "Normal", "Aggressive"]
    maximum_concurrent_positions: Optional[int]
    maximum_entries_per_day: int
    earliest_time_of_day: Optional[time]
    latest_time_of_day: Optional[time]
    day_of_week: Optional[Literal["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]]
    days_of_week: Optional[DaysOfWeek]
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
    call_short_strike_percent_otm_minimum: Optional[str]
    call_short_strike_target_percent_otm: Optional[str]
    call_short_strike_percent_otm_maximum: Optional[str]
    call_long_strike_type: Optional[Literal["Delta", "Premium"]]
    call_long_strike_minimum_delta: Optional[float]
    call_long_strike_target_delta: Optional[float]
    call_long_strike_maximum_delta: Optional[float]
    call_long_strike_minimum_premium: Optional[str]
    call_long_strike_target_premium: Optional[str]
    call_long_strike_maximum_premium: Optional[str]
    call_long_strike_percent_otm_minimum: Optional[str]
    call_long_strike_target_percent_otm: Optional[str]
    call_long_strike_percent_otm_maximum: Optional[str]
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
    put_short_strike_type: Optional[Literal["Delta", "Premium", "% OTM"]]
    put_short_strike_minimum_delta: Optional[float]
    put_short_strike_target_delta: Optional[float]
    put_short_strike_maximum_delta: Optional[float]
    put_short_strike_minimum_premium: Optional[str]
    put_short_strike_target_premium: Optional[str]
    put_short_strike_maximum_premium: Optional[str]
    put_short_strike_percent_otm_minimum: Optional[str]
    put_short_strike_target_percent_otm: Optional[str]
    put_short_strike_percent_otm_maximum: Optional[str]
    put_long_strike_type: Optional[Literal["Delta", "Premium", "% OTM"]]
    put_long_strike_minimum_delta: Optional[float]
    put_long_strike_target_delta: Optional[float]
    put_long_strike_maximum_delta: Optional[float]
    put_long_strike_minimum_premium: Optional[str]
    put_long_strike_target_premium: Optional[str]
    put_long_strike_maximum_premium: Optional[str]
    put_long_strike_percent_otm_minimum: Optional[str]
    put_long_strike_target_percent_otm: Optional[str]
    put_long_strike_percent_otm_maximum: Optional[str]
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
            return DaysOfWeek(**{'days_of_week': value})
        elif isinstance(value, dict):
            return DaysOfWeek(**value)
        elif isinstance(value, DaysOfWeek):
            return value
        else:
            raise ValueError(f"Invalid days_of_week type: must be DaysOfWeek or dict, got {type(value)}")


class ExitCondition(BaseModel):
    exit_speed: Literal["Super Patient", "Patient", "Normal", "Aggressive", "Super Aggressive"]
    profit_premium_value: Optional[str]
    profit_target_percent: Optional[str]
    stop_loss_percent: Optional[str]
    loss_premium_value: Optional[str]
    itm_percent_stop: Optional[str]
    otm_percent_stop: Optional[str]
    delta_stop: Optional[float]
    monitored_stop_sensitivity: Literal["Patient", "Normal", "Aggressive"]
    trail_profit_percent_trigger: Optional[str]
    trail_profit_percent_amount: Optional[str]
    trail_profit_premium_trigger: Optional[str]
    trail_profit_premium_amount: Optional[str]
    variables: list[Optional[BotVariable]]
    close_short_strike_only: bool
    sell_abandoned_long_strike: bool


class AdjustmentTime(BaseModel):
    start_time: time
    end_time: Optional[time]

    @classmethod
    def from_string(cls, time_range_str: str) -> 'AdjustmentTime':
        splt_time_str = time_range_str.split(' to ')
        start_str = splt_time_str[0]
        start_time = datetime.strptime(start_str, '%H:%M').time()
        end_time = None
        if len(splt_time_str) == 2:
            end_str = splt_time_str[1]
            end_time = datetime.strptime(end_str, '%H:%M').time()
        return cls(**{'start_time': start_time, 'end_time': end_time})


class Adjustment(BaseModel):
    number: str
    status: str
    type: str
    days_of_week: DaysOfWeek
    days_to_expiration: int
    time_of_day: AdjustmentTime
    minimum_position_delta: Optional[str]
    maximum_position_delta: Optional[str]
    minimum_position_profit_percent: Optional[str]
    maximum_position_profit_percent: Optional[str]
    minimum_position_otm_percent: Optional[str]
    maximum_position_otm_percent: Optional[str]
    minimum_underlying_percent_move_from_close: Optional[str]
    maximum_underlying_percent_move_from_close: Optional[str]
    variables: list[Optional[BotVariable]]

    @field_validator('days_of_week', mode='before', check_fields=True)
    def __convert_days_of_week(cls, value):
        if isinstance(value, str):
            return DaysOfWeek(**{'days_of_week': value})
        elif isinstance(value, dict):
            return DaysOfWeek(**value)
        elif isinstance(value, DaysOfWeek):
            return value
        else:
            raise ValueError(f"Invalid days_of_week type: must be DaysOfWeek or dict, got {type(value)}")

    @field_validator('time_of_day', mode='before', check_fields=True)
    def __convert_time_of_day(cls, value):
        if isinstance(value, str):
            return AdjustmentTime.from_string(value)
        elif isinstance(value, AdjustmentTime):
            return value
        else:
            raise ValueError(f"Invalid time_of_day type: must be AdjustmentTime or str, got {type(value)}")


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


class BasicBot(BaseModel):
    name: str
    number: str


class BotResponse(BasicBot):
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

        self._orders: dict[str, 'Order'] = {}
        self._positions: dict[str, 'Position'] = {}

    def __repr__(self):
        if self.auto_refresh:
            self.client.get_bot(self.number, include_details=False)  # dont need detail here as only need the name
        return f'<Bot {self.number} - {self.name}>'

    def enable(self):
        """
        Enable a bot that is currently disabled or disable on close
        Auth Required: Write Bots
        """
        response = requests.put(self.endpoint + 'enable', headers=self.client.headers)
        response = BaseResponse(**orjson.loads(response.text))
        if not response.success:
            raise APIError(response.message)

    def disable(self):
        """
        Disable a bot that is currently enabled. If the bot has open positions, the bot will move to Disable on Close. If there are no open positions, the bot will move to Disabled.
        Auth Required: Write Bots
        """
        response = requests.put(self.endpoint + 'disable', headers=self.client.headers)
        response = BaseResponse(**orjson.loads(response.text))
        if not response.success:
            raise APIError(response.message)

    def open_position(self):  # TODO: test when market open
        """
        Open a new position for the bot. This is only valid during market hours, while the bot is enabled, and while the bot has no more than one position currently open. This API request will ignore any entry filters configured for the bot and will immediately enter a new position when submitted.
        Auth Required: Write Positions
        """
        response = requests.post(self.endpoint + 'open', headers=self.client.headers)
        response = BaseResponse(**orjson.loads(response.text))
        if not response.success:
            raise APIError(response.message)

    def close_all_positions(self):  # TODO: test when market open
        """
        Close open position(s) for the bot. This is only valid during market hours and while the bot is set to Enabled or Disable on Close.
        Auth Required: Write Positions
        """
        response = requests.put(self.endpoint + 'close', headers=self.client.headers)
        response = BaseResponse(**orjson.loads(response.text))
        if not response.success:
            raise APIError(response.message)

    @property
    def orders(self) -> dict[str, 'Order']:
        if not self._orders or self.auto_refresh:
            orders = self.client.get_orders(bot=self)
            self._orders.update(orders)
        return self._orders

    @property
    def positions(self):
        if not self._positions or self.auto_refresh:
            positions = self.client.get_positions(bot=self)
            self._positions.update(positions)
        return self._positions

    @property
    def reports(self):
        return
