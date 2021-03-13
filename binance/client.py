from .api_def import ApiUrl, ApiVersion
from .api_def import KlineInterval, DepositHistoryStatus
from .api_def import OrderResponseType, OrderSide, OrderStatus, OrderType
from .api_def import SideEffectType, TimeInForce 
from .api_def import WithrawHistoryStatus, WalletType
from .request_handler import RequestHandler
from binance.endpoints.market_data import MarketDataEndpoints
from binance.endpoints.margin_trade import MarginAccountEndpoints
from binance.endpoints.spot_trade import SpotAccountTradeEndpoints
from binance.endpoints.wallet import WalletEndpoints


class PublicClient(MarketDataEndpoints):

    def __init__(self,
                 endpoint_version: str='',
                 request_params: dict=None,
                 tld: str='com'):       
        self.API_URL = ApiUrl(endpoint_version, tld)
        self._request_handler = RequestHandler(request_params=request_params)
        self._kline_interval = KlineInterval

    @property
    def KLINE_INTERVAL(self):
        return self._kline_interval
    
    @property
    def request_handler(self):
        return self._request_handler
    
    def _create_api_uri(self, path: str, version=ApiVersion.PUBLIC) -> str:
        return self.API_URL.DEFAULT + '/' + version + '/' + path

 
class AuthenticatedClient(MarketDataEndpoints,
                          MarginAccountEndpoints,
                          SpotAccountTradeEndpoints,
                          WalletEndpoints):

    def __init__(self,
                 api_key: str,
                 api_secret: str,
                 endpoint_version: str = '',
                 request_params: dict = None,
                 tld: str = 'com'):

        self.API_URL = ApiUrl(endpoint_version, tld)
        self._api_version = ApiVersion
        self._deposit_history_status = DepositHistoryStatus
        self._kline_interval = KlineInterval
        self._request_handler = RequestHandler(api_key=api_key,
                                               api_secret=api_secret,
                                               request_params=request_params)
        self._order_response_type = OrderResponseType
        self._order_side = OrderSide
        self._order_status = OrderStatus
        self._order_type = OrderType
        self._side_effect_type = SideEffectType
        self._time_in_force = TimeInForce
        self._withdraw_history_status = WithrawHistoryStatus
        self._wallet_type = WalletType

    @property
    def KLINE_INTERVAL(self):
        return self._kline_interval

    @property
    def ORDER_TYPE(self):
        return self._order_type

    @property
    def ORDER_SIDE(self):
        return self._order_side

    @property
    def API_VERSION(self):
        return self._api_version

    @property
    def ORDER_STATUS(self):
        return self._order_status

    @property
    def ORDER_RESPONSE_TYPE(self):
        return self._order_response_type
    
    @property
    def SIDE_EFFECT_TYPE(self):
        return self._side_effect_type
    
    @property
    def TIME_IN_FORCE(self):
        return self._time_in_force
    
    @property
    def request_handler(self):
        return self._request_handler

    @property
    def DEPOSIT_HISTORY_STATUS(self):
        return self._deposit_history_status

    @property
    def WALLET_TYPE(self):
        return self._wallet_type

    @property
    def WITHDRAW_HISTORY_STATUS(self):
        return self._withdraw_history_status

    def _create_api_uri(self, path: str, version=ApiVersion.PUBLIC) -> str:
        return self.API_URL.DEFAULT + '/' + version + '/' + path

    def _create_margin_api_uri(self, path: str):
        return self.API_URL.MARGIN + '/' + self.API_VERSION.MARGIN + '/' + path

    def _create_futures_api_uri(self, path: str):
        return self.API_URL.FUTURES + '/' + self.FUTURES_API_VERSION + '/' + path

    def _create_wallet_v3_api_uri(self, path: str):
        return self.API_URL.WALLET2 + '/' + self.API_VERSION.WALLET2 + '/' + path

    def _create_wallet_v1_api_uri(self, path: str):
        return self.API_URL.WALLET1 + '/' + self.API_VERSION.WALLET1 + '/' + path

    
if __name__ == '__main__':
    pass
