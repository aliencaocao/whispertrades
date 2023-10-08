import requests
from whispertrade import ENDPOINT
from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime, time

#
# bot_response = {
#         "entry_condition": {
#             "allocation_type": "Leverage Amount",
#             "contract_quantity": null,
#             "percent_of_portfolio": null,
#             "leverage_amount": "2.5",
#             "entry_speed": "Normal",
#             "maximum_entries_per_day": 1,
#             "earliest_time_of_day": "9:35 AM",
#             "latest_time_of_day": null,
#             "days_of_week": "Monday",
#             "minutes_between_positions": 0,
#             "minimum_starting_premium": null,
#             "maximum_starting_premium": null,
#             "minimum_days_to_expiration": 4,
#             "target_days_to_expiration": 4,
#             "maximum_days_to_expiration": 4,
#             "minimum_underlying_percent_move_from_close": null,
#             "maximum_underlying_percent_move_from_close": null,
#             "same_day_re_entry": null,
#             "avoid_fomc": null,
#             "move_strike_selection_with_conflict": "Yes",
#             "variables": [],
#             "call_short_strike_type": null,
#             "call_short_strike_minimum_delta": null,
#             "call_short_strike_target_delta": null,
#             "call_short_strike_maximum_delta": null,
#             "call_short_strike_minimum_premium": null,
#             "call_short_strike_target_premium": null,
#             "call_short_strike_maximum_premium": null,
#             "call_long_strike_type": null,
#             "call_long_strike_minimum_delta": null,
#             "call_long_strike_target_delta": null,
#             "call_long_strike_maximum_delta": null,
#             "call_long_strike_minimum_premium": null,
#             "call_long_strike_target_premium": null,
#             "call_long_strike_maximum_premium": null,
#             "call_spread_minimum_width_points": null,
#             "call_spread_target_width_points": null,
#             "call_spread_maximum_width_points": null,
#             "call_spread_minimum_width_percent": null,
#             "call_spread_target_width_percent": null,
#             "call_spread_maximum_width_percent": null,
#             "call_spread_strike_target_delta": null,
#             "call_spread_strike_target_premium": null,
#             "restrict_call_spread_width_by": null,
#             "call_spread_smart_width": false,
#             "put_short_strike_type": "Delta",
#             "put_short_strike_minimum_delta": "15.0",
#             "put_short_strike_target_delta": "20.0",
#             "put_short_strike_maximum_delta": "22.0",
#             "put_short_strike_minimum_premium": null,
#             "put_short_strike_target_premium": null,
#             "put_short_strike_maximum_premium": null,
#             "put_long_strike_type": null,
#             "put_long_strike_minimum_delta": null,
#             "put_long_strike_target_delta": null,
#             "put_long_strike_maximum_delta": null,
#             "put_long_strike_minimum_premium": null,
#             "put_long_strike_target_premium": null,
#             "put_long_strike_maximum_premium": null,
#             "put_spread_minimum_width_points": null,
#             "put_spread_target_width_points": 75,
#             "put_spread_maximum_width_points": 90,
#             "put_spread_minimum_width_percent": null,
#             "put_spread_target_width_percent": null,
#             "put_spread_maximum_width_percent": null,
#             "put_spread_strike_target_delta": null,
#             "put_spread_strike_target_premium": null,
#             "restrict_put_spread_width_by": null,
#             "put_spread_smart_width": false
#         },
#         "exit_condition": {
#             "exit_speed": "Normal",
#             "profit_premium_value": "$0.05",
#             "profit_target_percent": null,
#             "stop_loss_percent": "350",
#             "loss_premium_value": null,
#             "itm_percent_stop": null,
#             "delta_stop": null,
#             "monitored_stop_sensitivity": "Normal",
#             "trail_profit_percent_trigger": null,
#             "trail_profit_percent_amount": null,
#             "trail_profit_premium_trigger": null,
#             "trail_profit_premium_amount": null,
#             "variables": [],
#             "close_short_strike_only": "No",
#             "sell_abandoned_long_strike": "Yes"
#         },
#         "adjustments": [
#             {
#                 "number": "JPYW9UK9AL",
#                 "status": "Enabled",
#                 "type": "Enter Second Position",
#                 "days_of_week": "All",
#                 "days_to_expiration": 1,
#                 "time_of_day": "3:45 PM",
#                 "minimum_position_delta": null,
#                 "maximum_position_delta": null,
#                 "minimum_position_profit_percent": null,
#                 "maximum_position_profit_percent": null,
#                 "minimum_underlying_percent_move_from_close": null,
#                 "maximum_underlying_percent_move_from_close": null,
#                 "variables": []
#             }
#         ],
#         "notifications": [
#             {
#                 "number": "CKYLJK5O9E",
#                 "event": "Order Filled",
#                 "type": "Email"
#             },
#             {
#                 "number": "SMUAJAY9BK",
#                 "event": "Position Expired",
#                 "type": "Email"
#             },
#         ],
#         "variables": [
#             {
#                 "number": "VIZG80TGC9",
#                 "name": "Weekly PCS Realized Profit Today",
#                 "value": "150.56",
#                 "bot_value_to_set": "Bot Profit Realized Today $",
#                 "free_text_value_to_set": null,
#                 "last_updated_at": "2023-10-05T18:55:23.000000Z"
#             },
#         ]
#     }
# }


class BrokerConnection(BaseModel):
    name: str
    number: str
    account_number: str


class EntryCondition(BaseModel):
    allocation_type: Literal["Leverage Amount", "Fixed Contract Quantity", "Percent of Portfolio"]
    contract_quantity: Optional[int]  # TODO: check
    percent_of_portfolio: Optional[int]  # TODO: check
    leverage_amount: Optional[str]
    entry_speed: Literal["Patient", "Normal", "Aggressive"]
    maximum_entries_per_day: int
    earliest_time_of_day: str
    latest_time_of_day: Optional[time]
    days_of_week: Literal["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    minutes_between_positions: int
    minimum_starting_premium: Optional[float]
    maximum_starting_premium: Optional[float]
    minimum_days_to_expiration: int
    target_days_to_expiration: int
    maximum_days_to_expiration: int
    minimum_underlying_percent_move_from_close: Optional[float]
    maximum_underlying_percent_move_from_close: Optional[float]
    same_day_re_entry: Optional[str]
    avoid_fomc: Optional[str]
    move_strike_selection_with_conflict: str
    variables: list[str]
    call_short_strike_type: Optional[str]
    call_short_strike_minimum_delta: Optional[float]
    call_short_strike_target_delta: Optional[float]
    call_short_strike_maximum_delta: Optional[float]
    call_short_strike_minimum_premium: Optional[float]
    call_short_strike_target_premium: Optional[float]
    call_short_strike_maximum_premium: Optional[float]
    call_long_strike_type: Optional[str]
    call_long_strike_minimum_delta: Optional[float]
    call_long_strike_target_delta: Optional[float]
    call_long_strike_maximum_delta: Optional[float]
    call_long_strike_minimum_premium: Optional[float]
    call_long_strike_target_premium: Optional[float]
    call_long_strike_maximum_premium: Optional[float]
    call_spread_minimum_width_points: Optional[float]
    call_spread_target_width_points: Optional[float]
    call_spread_maximum_width_points: Optional[float]
    call_spread_minimum_width_percent: Optional[float]
    call_spread_target_width_percent: Optional[float]
    call_spread_maximum_width_percent: Optional[float]
    call_spread_strike_target_delta: Optional[float]
    call_spread_strike_target_premium: Optional[float]
    restrict_call_spread_width_by: Optional[str]
    call_spread_smart_width: bool
    put_short_strike_type: Optional[str]
    put_short_strike_minimum_delta: Optional[float]
    put_short_strike_target_delta: Optional[float]
    put_short_strike_maximum_delta: Optional[float]
    put_short_strike_minimum_premium: Optional[float]
    put_short_strike_target_premium: Optional[float]
    put_short_strike_maximum_premium: Optional[float]
    put_long_strike_type: Optional[str]
    put_long_strike_minimum_delta: Optional[float]
    put_long_strike_target_delta: Optional[float]
    put_long_strike_maximum_delta: Optional[float]
    put_long_strike_minimum_premium: Optional[float]
    put_long_strike_target_premium: Optional[float]
    put_long_strike_maximum_premium: Optional[float]
    put_spread_minimum_width_points: Optional[float]
    put_spread_target_width_points: Optional[float]
    put_spread_maximum_width_points: Optional[float]
    put_spread_minimum_width_percent: Optional[float]
    put_spread_target_width_percent: Optional[float]
    put_spread_maximum_width_percent: Optional[float]
    put_spread_strike_target_delta: Optional[float]
    put_spread_strike_target_premium: Optional[float]
    restrict_put_spread_width_by: Optional[str]
    put_spread_smart_width: bool


class ExitCondition(BaseModel):
    exit_speed: str
    profit_premium_value: Optional[str]
    profit_target_percent: Optional[float]
    stop_loss_percent: Optional[float]
    loss_premium_value: Optional[float]
    itm_percent_stop: Optional[float]
    delta_stop: Optional[float]
    monitored_stop_sensitivity: str
    trail_profit_percent_trigger: Optional[float]
    trail_profit_percent_amount: Optional[float]
    trail_profit_premium_trigger: Optional[float]
    trail_profit_premium_amount: Optional[float]
    variables: list[str]
    close_short_strike_only: str
    sell_abandoned_long_strike: str


class Adjustment(BaseModel):
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


class Notification(BaseModel):
    number: str
    event: str
    type: str


class Variable(BaseModel):
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
    entry_condition: Optional[EntryCondition]
    exit_condition: Optional[ExitCondition]
    adjustments: Optional[list[Adjustment]]
    notifications: Optional[list[Notification]]
    variables: Optional[list[Variable]]


class Bot:
    def __init__(self, data: BotResponse):
        for key, value in data.model_dump().items():
            setattr(self, key, value)