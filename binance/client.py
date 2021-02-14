from .api_def import *
from .exceptions import BinanceAPIException, BinanceRequestException
from .request_handler import RequestHandler
from .utils import create_query_string, create_sorted_list, generate_signature
from .wallet import Wallet
from binance.endpoints.market_data import MarketDataEndpoints
from binance.endpoints.spot_trade import SpotAccountTradeEndpoints
from binance.endpoints.margin_trade import MarginAccountEndpoints
from typing import Union
import time

class PublicClient(MarketDataEndpoints):

    def __init__(self,
                 endpoint_version: str = '',
                 request_params: dict = None,
                 tld: str = 'com'):
        
        self.API_URL = ApiUrl.DEFAULT.format(endpoint_version, tld)
        self._request_handler = RequestHandler(request_params = request_params)
        self._kline_interval = KlineInterval

    @property
    def KLINE_INTERVAL(self):
        return self._kline_interval
    
    @property
    def request_handler(self):
        return self._request_handler
    
    def _create_api_uri(self, path: str, version=ApiVersion.PUBLIC) -> str:
        return self.API_URL + '/' + version + '/' + path

 
class AuthenticatedClient(MarketDataEndpoints,
                          SpotAccountTradeEndpoints,
                          MarginAccountEndpoints
                          ):

    def __init__(self,
                 api_key: str,
                 api_secret: str,
                 endpoint_version: str = '',
                 request_params: dict = None,
                 tld: str = 'com'):


        self.WITHDRAW_API_URL = self.WITHDRAW_API_URL.format(endpoint_version, tld)
        self.MARGIN_API_URL = self.MARGIN_API_URL.format(endpoint_version, tld)
        self.WEBSITE_URL = self.WEBSITE_URL.format(endpoint_version, tld)
        self.FUTURES_URL = self.FUTURES_URL.format(endpoint_version, tld)
        self._request_handler = RequestHandler(api_key = api_key,
                                               api_secret = api_secret,
                                               request_params = request_params)
        self._order_type = OrderType
        self._order_side = OrderSide
        self.wallet = Wallet(self.request_handler)
        #self._add_apikey_to_header()

    @property
    def ORDER_TYPE(self):
        return self._order_type

    @property
    def ORDER_SIDE(self):
        return self._order_side
    
    @property
    def request_handler(self):
        return self._request_handler
    
    def _create_api_uri(self, path: str, version=ApiVersion.PUBLIC) -> str:
        return self.API_URL + '/' + version + '/' + path

    def __create_margin_api_uri(self, path: str):
        return self.MARGIN_API__URL + '/' + self.MARGIN_API_VERSION + '/' + path

    def _create_futures_api_uri(self, path: str):
        return self.FUTURES_API__URL + '/' + self.FUTURES_API_VERSION + '/' + path
    
    
if __name__ == '__main__':
    pass
