import warnings
from datetime import date, datetime
from typing import Literal, Optional, TYPE_CHECKING

from pydantic import BaseModel

from .bot import BasicBot, BrokerConnection

if TYPE_CHECKING:
    from . import WTClient


class BasicReportDetail(BaseModel):
    total_trades: Optional[int]
    winning_trades: Optional[int]
    losing_trades: Optional[int]
    win_percent: Optional[float]


class BotReportDetail(BasicBot, BasicReportDetail):
    average_entry_price: float
    average_exit_price: float
    average_profit_price: float
    average_gain: float
    average_win: float
    average_loss: float
    premium_collected: float
    premium_retained: float
    premium_retained_percent: float
    total_profit: float


class ResultByDay(BaseModel):
    date: date
    current_drawdown_dollars: float
    current_drawdown_percent: float
    day_return_percent: float
    profit: float
    total_return_percent: float
    underlying_current_drawdown_days: int
    underlying_current_drawdown_percent: float
    underlying_day_return_percent: float
    underlying_total_return_percent: float


class ResultByTimeframe(BasicReportDetail):
    date: date
    starting_net_liquidation_value: float
    ending_net_liquidation_value: float
    broker_fees: float
    total_return_dollars: float
    total_return_percent: float
    max_drawdown_dollars: float
    max_drawdown_percent: float
    underlying_max_drawdown_percent: float
    underlying_total_return_percent: float


class ResultByYear(ResultByTimeframe):
    months: dict[Literal['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], ResultByTimeframe]


class Results(BasicReportDetail):
    starting_net_liquidation_value: float
    ending_net_liquidation_value: float
    average_gain: Optional[float]
    average_win: Optional[float]
    average_loss: Optional[float]
    broker_fees: Optional[float]
    premium_collected: Optional[float]
    premium_retained: Optional[float]
    premium_retained_percent: Optional[float]
    total_return_dollars: float
    total_return_percent: float
    max_drawdown_dollars: float
    max_drawdown_percent: float
    max_drawdown_days: int
    cagr: float
    sharpe: float
    sortino: float
    mar: float
    annualized_volatility: float
    correlation: float
    beta: float
    underlying_total_return_percent: float
    underlying_max_drawdown_percent: float
    underlying_max_drawdown_days: int
    underlying_cagr: float
    underlying_sharpe: float
    underlying_sortino: float
    underlying_mar: float
    underlying_annualized_volatility: float
    bots: list[BotReportDetail] = None
    years: dict[int, ResultByYear] = None
    days: list[ResultByDay] = None


class ReportResponse(BaseModel):
    number: str
    name: str
    status: Literal['Complete', 'Running', 'Draft']  # TODO: verify Running
    completed_at: Optional[datetime]
    start_date: date
    end_date: date
    run_until_latest_date: bool
    is_public: bool
    symbol: str
    nlv_source: Literal['Actual NLV', 'Percent of NLV', 'Fixed Balance', 'Specific Starting Balance']
    nlv_amount: Optional[float]
    bot_statuses: list[Literal['Enabled', 'Disabled']]
    brokers: Optional[list[BrokerConnection]]
    bots: list[Optional[BasicBot]]
    bot_tags: list[Optional[str]]
    bot_position_tags: list[Optional[str]]
    results: Results


class Report:
    def __init__(self, data: ReportResponse, client: 'WTClient', auto_refresh: bool):
        self._ReportResponse = data
        self.client = client
        self.auto_refresh = auto_refresh

        self.number = data.number
        self.name = data.name
        self.status = data.status
        self.completed_at = data.completed_at
        self.start_date = data.start_date
        self.end_date = data.end_date
        self.run_until_latest_date = data.run_until_latest_date
        self.is_public = data.is_public
        self.symbol = data.symbol
        self.nlv_source = data.nlv_source
        self.nlv_amount = data.nlv_amount
        self.bot_statuses = data.bot_statuses
        self.brokers = data.brokers
        self.bots = data.bots
        self.bot_tags = data.bot_tags
        self.bot_position_tags = data.bot_position_tags
        self.results = data.results
        self.daily_results = data.results.days
        self._monthly_results = None
        self._yearly_results = None

    @property
    def monthly_results(self) -> Optional[dict[date, ResultByTimeframe]]:
        if self.auto_refresh:
            self.client.get_report(self.number)
        elif self._monthly_results is None:
            warnings.warn(f'Monthly results are not initialized yet for report {self.number} as you have turned off auto refresh. Please run client.get_report({self.number}) or turn on auto refresh to access it.', UserWarning)
        if self.auto_refresh or (self._monthly_results is None and self.results.years is not None):  # if previously uninitialized and now we have the raw data, initialize it. If auto refresh is on, reinitialize anyways
            r = {}
            for year in self.results.years.values():
                for month in year.months.values():
                    r.update({month.date: month})
            self._monthly_results = r
        return self._monthly_results

    @property
    def yearly_results(self) -> Optional[dict[date, ResultByTimeframe]]:
        if self.auto_refresh:
            self.client.get_report(self.number)
        elif self._yearly_results is None:
            warnings.warn(f'Yearly results are not initialized yet for report {self.number} as you have turned off auto refresh. Please run client.get_report({self.number}) or turn on auto refresh to access it.', UserWarning)
        if self.auto_refresh or (self._yearly_results is None and self.results.years is not None):  # if previously uninitialized and now we have the raw data, initialize it. If auto refresh is on, reinitialize anyways
            r = {}
            for year in self.results.years.values():
                year = ResultByTimeframe(**year.model_dump(exclude={'months'}))
                r.update({year.date: year})
            self._yearly_results = r
        return self._yearly_results

    def __repr__(self) -> str:
        return f'<Report {self._ReportResponse}>'
