from datetime import datetime
from typing import Literal, Optional, TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from . import WTClient


class BaseBrokerConnection(BaseModel):
    name: Optional[str]
    number: str
    account_number: str


class BrokerConnectionResponse(BaseBrokerConnection):
    broker: str
    status: Literal["Active", "Inactive"]
    net_liquidation_value: float
    expires_at: Optional[datetime]


class BrokerConnection:
    def __init__(self, data: BrokerConnectionResponse, client: 'WTClient', auto_refresh: bool = True):
        self._BrokerConnectionResponse: BrokerConnectionResponse = data  #: raw response data from API
        self.client: 'WTClient' = client  #: the WTClient object that created this instance
        self.auto_refresh: bool = auto_refresh  #: auto_refresh toggle inherited from WTClient

        self.name: Optional[str] = data.name  #: name of the connection as set by user
        self.number: str = data.number  #: connection number
        self.account_number: str = data.account_number  #: account number
        self.broker: str = data.broker  #: broker name
        self.status: Literal["Active", "Inactive"] = data.status  #: connection status
        self.net_liquidation_value: float = data.net_liquidation_value  #: net liquidation value
        self.expires_at: Optional[datetime] = data.expires_at  #: expiration date. Only for brokers without permanent connection. e.g. Schwab

    def __repr__(self):
        return str(self._BrokerConnectionResponse)
