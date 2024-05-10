import warnings
from datetime import date, datetime
from typing import Literal, Optional, TYPE_CHECKING

import orjson
from pydantic import BaseModel

from .bot import BasicBot
from .broker_connection import BaseBrokerConnection
from .common import APIError, BaseResponse, ReportUninitializedWarning

if TYPE_CHECKING:
    from . import WTClient

warnings.filterwarnings('always', category=ReportUninitializedWarning)


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
    status: Literal['Complete', 'Running', 'Draft']
    completed_at: Optional[datetime]
    start_date: date
    end_date: date
    run_until_latest_date: bool
    is_public: bool
    symbol: str
    nlv_source: Literal['Actual NLV', 'Percent of NLV', 'Fixed Balance', 'Specific Starting Balance']
    nlv_amount: Optional[float]
    bot_statuses: list[Literal['Enabled', 'Disabled']]
    brokers: Optional[list[BaseBrokerConnection]]
    bots: list[Optional[BasicBot]]
    bot_tags: list[Optional[str]]
    bot_position_tags: list[Optional[str]]
    results: Results


class Report:
    def __init__(self, data: ReportResponse, client: 'WTClient', auto_refresh: bool):
        self._ReportResponse: ReportResponse = data  #: raw response data from API
        self.client: 'WTClient' = client  #: the WTClient object that created this instance
        self.auto_refresh: bool = auto_refresh  #: auto_refresh toggle inherited from WTClient

        self.number: str = data.number  #: Report number
        self.name: str = data.name  #: Report name
        self.status: Literal['Complete', 'Running', 'Draft'] = data.status  #: Report status
        self.completed_at: Optional[datetime] = data.completed_at  #: Completed at
        self.start_date: date = data.start_date  #: Start date
        self.end_date: date = data.end_date  #: End date
        self.run_until_latest_date: bool = data.run_until_latest_date  #: Run until latest date
        self.is_public: bool = data.is_public  #: Is public
        self.symbol: str = data.symbol  #: Symbol
        self.nlv_source: Literal['Actual NLV', 'Percent of NLV', 'Fixed Balance', 'Specific Starting Balance'] = data.nlv_source  #: NLV source
        self.nlv_amount: Optional[float] = data.nlv_amount  #: NLV amount
        self.bot_statuses: List[Literal['Enabled', 'Disabled']] = data.bot_statuses  #: Bot statuses
        self.brokers: Optional[List[BaseBrokerConnection]] = data.brokers  #: Brokers
        self.bots: List[Optional[BasicBot]] = data.bots  #: Bots
        self.bot_tags: List[Optional[str]] = data.bot_tags  #: Bot tags
        self.bot_position_tags: List[Optional[str]] = data.bot_position_tags  #: Bot position tags
        self.results: Results = data.results  #: Results

        #: Daily results for this report
        #: Auth Required: Read Reports
        self.daily_results: List[ResultByDay] = data.results.days

        self._monthly_results: Optional[Dict[date, ResultByTimeframe]] = None
        self._yearly_results: Optional[Dict[date, ResultByTimeframe]] = None

    @property
    def monthly_results(self) -> Optional[dict[date, ResultByTimeframe]]:
        """
        Monthly results for this report
        Auth Required: Read Reports

        :return: Monthly results for this report in a dictionary with date as key and ResultByTimeframe as value
        """
        if self.auto_refresh:
            self.client.get_report(self.number)
        elif self._monthly_results is None:
            warnings.warn(f'Monthly results are not initialized yet for report {self.number} as you have turned off auto refresh. Please run client.get_report({self.number}) or turn on auto refresh to access it.', ReportUninitializedWarning)
        if self.auto_refresh or (self._monthly_results is None and self.results.years is not None):  # if previously uninitialized and now we have the raw data, initialize it. If auto refresh is on, reinitialize anyways
            r = {}
            for year in self.results.years.values():
                for month in year.months.values():
                    r.update({month.date: month})
            self._monthly_results = r
        return self._monthly_results

    @property
    def yearly_results(self) -> Optional[dict[date, ResultByTimeframe]]:
        """
        Yearly results for this report
        Auth Required: Read Reports

        :return: Yearly results for this report in a dictionary with date as key and ResultByTimeframe as value
        """
        if self.auto_refresh:
            self.client.get_report(self.number)
        elif self._yearly_results is None:
            warnings.warn(f'Yearly results are not initialized yet for report {self.number} as you have turned off auto refresh. Please run client.get_report({self.number}) or turn on auto refresh to access it.', ReportUninitializedWarning)
        if self.auto_refresh or (self._yearly_results is None and self.results.years is not None):  # if previously uninitialized and now we have the raw data, initialize it. If auto refresh is on, reinitialize anyways
            r = {}
            for year in self.results.years.values():
                year = ResultByTimeframe(**year.model_dump(exclude={'months'}))
                r.update({year.date: year})
            self._yearly_results = r
        return self._yearly_results

    def update(self, name: str = None, start_date: date = None, end_date: date = None, run_until_latest_date: bool = None) -> str:
        """
        Change a bot report name or date range
        Auth Required: Write Reports

        :param name: new name of the report
        :param start_date: new start date for the report
        :param end_date: new end date for the report
        :param run_until_latest_date: whether to run the report until the latest date
        :return: Update message from Whispertrades API
        """
        if not name and not start_date and not end_date and run_until_latest_date is None:
            raise ValueError('At least one of name, start_date, end_date, or run_until_latest_date is required. Name cannot be empty string.')
        if start_date and end_date and start_date > end_date:
            raise ValueError('Start date cannot be after end date.')
        payload = {}
        if name:
            payload['name'] = str(name)
        if start_date:  # YYYY-MM-DD
            payload['start_date'] = start_date.isoformat()
        if end_date:
            payload['end_date'] = end_date.isoformat()
        if run_until_latest_date is not None:
            payload['run_until_latest_date'] = run_until_latest_date
        response = self.client.session.put(f"{self.client.endpoint}bots/reports/{self.number}", headers=self.client.headers, json=payload)
        response = BaseResponse(**orjson.loads(response.text))
        if response.success:
            return response.message
        else:
            raise APIError(response.message)

    def run(self):
        """
        Run/refresh this report using its current configuration
        Auth Required: Write Reports
        """
        response = self.client.session.put(f"{self.client.endpoint}bots/reports/{self.number}/run", headers=self.client.headers)
        response = BaseResponse(**orjson.loads(response.text))
        if response.success:
            return response.message
        else:
            raise APIError(response.message)

    def __repr__(self) -> str:
        return f'<Report {self._ReportResponse}>'
