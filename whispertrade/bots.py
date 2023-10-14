from datetime import datetime, time
from typing import Literal, Optional

from pydantic import BaseModel, field_validator

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
            "allocation_type": "Leverage Amount",
            "contract_quantity": None,
            "percent_of_portfolio": None,
            "leverage_amount": "5.0",
            "entry_speed": "Normal",
            "maximum_entries_per_day": 5,
            "earliest_time_of_day": None,
            "latest_time_of_day": None,
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
            "variables": [
                {
                    "number": "MXCFKNY0BC",
                    "name": "testvar",
                    "condition": "Equal To",
                    "value": "hi",
                }
            ],
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
        "adjustments": [
            {
                "number": "JU4ABN7RRA",
                "status": "Enabled",
                "type": "Close Position Early",
                "days_of_week": "Monday, Wednesday, Thursday, Friday",
                "days_to_expiration": 3,
                "time_of_day": "21:33",
                "minimum_position_delta": "4.0%",
                "maximum_position_delta": "4.0%",
                "minimum_position_profit_percent": "4.00%",
                "maximum_position_profit_percent": "4.00%",
                "minimum_underlying_percent_move_from_close": "4.00%",
                "maximum_underlying_percent_move_from_close": "4.00%",
                "variables": [
                    {
                        "number": "MXCFKNY0BC",
                        "name": "testvar",
                        "condition": "Less Than",
                        "value": "444",
                    }
                ],
            }
        ],
        "notifications": [],
        "variables": [
            {
                "number": "MXCFKNY0BC",
                "name": "testvar",
                "value": None,
                "bot_value_to_set": "Free Text",
                "free_text_value_to_set": "hi",
                "last_updated_at": "2023-10-14T02:39:04.000000Z",
            }
        ],
    }

]


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


class Variable(BaseModel):
    number: str
    name: str
    value: Optional[str]
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
    free_text_value_to_set: Optional[str] = None
    last_updated_at: Optional[datetime] = None


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
    variables: list[Optional[Variable]]
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
    variables: list[Optional[Variable]]
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
    variables: list[Optional[Variable]]

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


class Notification(BaseModel):  # TODO: check
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

        # attributes for IDE type hinting
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
        self.variables: list[Optional[Variable]] = data.variables

    def __repr__(self):
        return str(self._BotResponse)
