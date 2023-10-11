from datetime import datetime, time
from typing import Literal, Optional

from pydantic import BaseModel, field_validator

#
sample = [
    {
        "number": "VCRPZ6ZNZZ",
        "name": "test",
        "broker_connection": {
            "name": None,
            "number": "HQUQUE4JIS",
            "account_number": "YSO7QYGWXS",
        },
        "is_paper": True,
        "status": "Disabled",
        "can_enable": True,
        "can_disable": False,
        "symbol": "SPXW",
        "type": "Put Credit Spread",
        "notes": None,
        "last_active_at": None,
        "disabled_at": None,
        "entry_condition": {
            "allocation_type": "Contract Quantity",
            "contract_quantity": 1,
            "percent_of_portfolio": None,
            "leverage_amount": None,
            "entry_speed": "Normal",
            "maximum_entries_per_day": 1,
            "earliest_time_of_day": "21:31",
            "latest_time_of_day": "21:50",
            "days_of_week": "All",
            "minutes_between_positions": 0,
            "minimum_starting_premium": None,
            "maximum_starting_premium": None,
            "minimum_days_to_expiration": 1,
            "target_days_to_expiration": 1,
            "maximum_days_to_expiration": 3,
            "minimum_underlying_percent_move_from_close": "5.00%",
            "maximum_underlying_percent_move_from_close": "10.00%",
            "same_day_re_entry": None,
            "avoid_fomc": None,
            "move_strike_selection_with_conflict": "No",
            "variables": [],
            "call_short_strike_type": None,
            "call_short_strike_minimum_delta": None,
            "call_short_strike_target_delta": None,
            "call_short_strike_maximum_delta": None,
            "call_short_strike_minimum_premium": None,
            "call_short_strike_target_premium": None,
            "call_short_strike_maximum_premium": None,
            "call_long_strike_type": None,
            "call_long_strike_minimum_delta": None,
            "call_long_strike_target_delta": None,
            "call_long_strike_maximum_delta": None,
            "call_long_strike_minimum_premium": None,
            "call_long_strike_target_premium": None,
            "call_long_strike_maximum_premium": None,
            "call_spread_minimum_width_points": None,
            "call_spread_target_width_points": None,
            "call_spread_maximum_width_points": None,
            "call_spread_minimum_width_percent": None,
            "call_spread_target_width_percent": None,
            "call_spread_maximum_width_percent": None,
            "call_spread_strike_target_delta": None,
            "call_spread_strike_target_premium": None,
            "restrict_call_spread_width_by": None,
            "call_spread_smart_width": False,
            "put_short_strike_type": "Delta",
            "put_short_strike_minimum_delta": None,
            "put_short_strike_target_delta": "2.2",
            "put_short_strike_maximum_delta": None,
            "put_short_strike_minimum_premium": None,
            "put_short_strike_target_premium": None,
            "put_short_strike_maximum_premium": None,
            "put_long_strike_type": None,
            "put_long_strike_minimum_delta": None,
            "put_long_strike_target_delta": None,
            "put_long_strike_maximum_delta": None,
            "put_long_strike_minimum_premium": None,
            "put_long_strike_target_premium": None,
            "put_long_strike_maximum_premium": None,
            "put_spread_minimum_width_points": None,
            "put_spread_target_width_points": 300,
            "put_spread_maximum_width_points": None,
            "put_spread_minimum_width_percent": None,
            "put_spread_target_width_percent": None,
            "put_spread_maximum_width_percent": None,
            "put_spread_strike_target_delta": None,
            "put_spread_strike_target_premium": None,
            "restrict_put_spread_width_by": None,
            "put_spread_smart_width": True,
        },
        "exit_condition": {
            "exit_speed": "Normal",
            "profit_premium_value": "$5.00",
            "profit_target_percent": None,
            "stop_loss_percent": "10.00%",
            "loss_premium_value": "$5.00",
            "itm_percent_stop": "5.00%",
            "delta_stop": "5.0",
            "monitored_stop_sensitivity": "Normal",
            "trail_profit_percent_trigger": "5.00%",
            "trail_profit_percent_amount": "5.00%",
            "trail_profit_premium_trigger": "$5.00",
            "trail_profit_premium_amount": "$5.00",
            "variables": [],
            "close_short_strike_only": "No",
            "sell_abandoned_long_strike": "No",
        },
        "adjustments": [],
        "notifications": [],
        "variables": [],
    }
]


class BrokerConnection(BaseModel):
    name: Optional[str]  # only when using PAPER
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


class EntryCondition(BaseModel):
    allocation_type: Literal["Leverage Amount", "Contract Quantity", "Percent of Portfolio"]
    contract_quantity: Optional[int]
    percent_of_portfolio: Optional[float]
    leverage_amount: Optional[str]  # TODO: check
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
    same_day_re_entry: Optional[str]  # TODO: check
    avoid_fomc: Optional[str]
    move_strike_selection_with_conflict: Literal["Yes", "No"]
    variables: list[str]  # TODO: check
    call_short_strike_type: Optional[str]  # TODO: check
    call_short_strike_minimum_delta: Optional[float]
    call_short_strike_target_delta: Optional[float]
    call_short_strike_maximum_delta: Optional[float]
    call_short_strike_minimum_premium: Optional[float]  # TODO: check
    call_short_strike_target_premium: Optional[float]  # TODO: check
    call_short_strike_maximum_premium: Optional[float]  # TODO: check
    call_long_strike_type: Optional[str]  # TODO: check
    call_long_strike_minimum_delta: Optional[float]
    call_long_strike_target_delta: Optional[float]
    call_long_strike_maximum_delta: Optional[float]
    call_long_strike_minimum_premium: Optional[float]  # TODO: check
    call_long_strike_target_premium: Optional[float]  # TODO: check
    call_long_strike_maximum_premium: Optional[float]  # TODO: check
    call_spread_minimum_width_points: Optional[float]  # TODO: check
    call_spread_target_width_points: Optional[float]  # TODO: check
    call_spread_maximum_width_points: Optional[float]  # TODO: check
    call_spread_minimum_width_percent: Optional[float]  # TODO: check
    call_spread_target_width_percent: Optional[float]  # TODO: check
    call_spread_maximum_width_percent: Optional[float]  # TODO: check
    call_spread_strike_target_delta: Optional[float]
    call_spread_strike_target_premium: Optional[float]  # TODO: check
    restrict_call_spread_width_by: Optional[str]  # TODO: check
    call_spread_smart_width: bool
    put_short_strike_type: Optional[str]
    put_short_strike_minimum_delta: Optional[float]
    put_short_strike_target_delta: Optional[float]
    put_short_strike_maximum_delta: Optional[float]
    put_short_strike_minimum_premium: Optional[float]  # TODO: check
    put_short_strike_target_premium: Optional[float]  # TODO: check
    put_short_strike_maximum_premium: Optional[float]  # TODO: check
    put_long_strike_type: Optional[str]  # TODO: check
    put_long_strike_minimum_delta: Optional[float]
    put_long_strike_target_delta: Optional[float]
    put_long_strike_maximum_delta: Optional[float]
    put_long_strike_minimum_premium: Optional[float]  # TODO: check
    put_long_strike_target_premium: Optional[float]  # TODO: check
    put_long_strike_maximum_premium: Optional[float]  # TODO: check
    put_spread_minimum_width_points: Optional[float]
    put_spread_target_width_points: Optional[float]
    put_spread_maximum_width_points: Optional[float]
    put_spread_minimum_width_percent: Optional[float]
    put_spread_target_width_percent: Optional[float]  # TODO: check
    put_spread_maximum_width_percent: Optional[float]  # TODO: check
    put_spread_strike_target_delta: Optional[float]
    put_spread_strike_target_premium: Optional[float]  # TODO: check
    restrict_put_spread_width_by: Optional[str]  # TODO: check
    put_spread_smart_width: bool

    @field_validator('days_of_week', mode='before', check_fields=True)
    def convert_days_of_week(cls, value):
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
    variables: list[str]  # TODO: check
    close_short_strike_only: Literal["Yes", "No"]
    sell_abandoned_long_strike: Literal["Yes", "No"]


class Adjustment(BaseModel):  # TODO: check
    number: str
    status: str
    type: str
    days_of_week: str
    days_to_expiration: int
    time_of_day: str
    minimum_position_delta: Optional[float]
    maximum_position_delta: Optional[float]
    minimum_position_profit_percent: Optional[float]
    maximum_position_profit_percent: Optional[float]
    minimum_underlying_percent_move_from_close: Optional[float]
    maximum_underlying_percent_move_from_close: Optional[float]
    variables: list[str]


class Notification(BaseModel):  # TODO: check
    number: str
    event: str
    type: str


class Variable(BaseModel):  # TODO: check
    number: str
    name: str
    value: str
    bot_value_to_set: Optional[str]
    free_text_value_to_set: Optional[str]
    last_updated_at: str


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
    variables: list[Optional[Variable]] = None


def toCamalCase(s: str) -> str:
    return s.replace('_', ' ').title().replace(' ', '')


class Bot:
    def __init__(self, data: BotResponse):
        self._BotResponse = data
        for key, value in data.model_dump().items():
            if isinstance(value, dict):
                value = globals()[toCamalCase(key)](**value)
            setattr(self, key, value)

    def __repr__(self):
        return str(self._BotResponse)
