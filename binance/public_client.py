
from .api_def import PublicAPI
from .exceptions import BinanceAPIException, BinanceRequestException

from binance.endpoints.market_data import MarketDataEndpoints
from .request_handler import RequestHandler
from typing import Union
import time

class PublicClient(PublicAPI, MarketDataEndpoints):

    def __init__(self,
                 endpoint_version: str = '',
                 request_params: dict = None,
                 tld: str = 'com'):
        
        self.API_URL = self.API_URL.format(endpoint_version, tld)
        self._request_handler = RequestHandler(request_params = request_params)


    @property
    def request_handler(self):
        return self._request_handler
    
    def _create_api_uri(self, path: str, version=PublicAPI.PUBLIC_API_VERSION) -> str:
        return self.API_URL + '/' + version + '/' + path

if __name__ == '__main__':
    pass
