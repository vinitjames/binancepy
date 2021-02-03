from .api_def import PublicAPI
from .exceptions import BinanceAPIException, BinanceRequestException
from .utils import format_time
from requests import Session
from requests.models import Response
from typing import Union



class PublicClient(PublicAPI):

    def __init__(self, endpoint_version: str = '', request_params: dict = None, tld: str = 'com'):
        self.API_URL = self.API_URL.format(endpoint_version, tld)
        self.session = self._init_session()
        self.request_params = request_params

    def _init_session(self) -> Session:
        session = Session()
        session.headers.update({'Accept': 'application/json',
                                'User-Agent': 'binance/python'})
        return session

    def _create_api_uri(self, path: str, version=PublicAPI.PUBLIC_API_VERSION):
        return self.API_URL + '/' + version + '/' + path

    def _request_public(self, uri, **params):

        kwargs = {}
        kwargs['params'] = params
        kwargs['timeout'] = 10
        if self.request_params:
            kwargs.update(self.request_params)
        response = self.session.get(uri, **kwargs)
        return self._handle_response(response)

    @classmethod
    def _handle_response(cls, response: Response) -> dict:
        if(type(response) != Response):
            raise ValueError(
                "Client Error: _handle resource was not called with Response Type")
        if(not str(response.status_code).startswith('2')):
            raise BinanceAPIException(response)

        try:
            return response.json()
        except ValueError:
            raise BinanceRequestException(response)

    def ping(self) -> dict:
        uri = self._create_api_uri('ping')
        return self._request_public(uri)

    def get_server_time(self) -> dict:
        uri = self._create_api_uri('time')
        return self._request_public(uri)

    def get_exchange_info(self) -> dict:
        uri = self._create_api_uri('exchangeInfo')
        return self._request_public(uri)

    def get_symbol_info(self, symbol: str) -> dict:
        resp_data = self.get_exchange_info()
        for sym_data in resp_data['symbols']:
            if(sym_data['symbol'] == symbol.upper()):
                return sym_data
        return None

    def get_price_ticker(self, symbol: str = None) -> dict:
        uri = self._create_api_uri('ticker/price')
        if(symbol == None):
            return self._request_public(uri)
        return self._request_public(uri, symbol=symbol)

    def get_orderbook_ticker(self, symbol: str = None) -> dict:
        uri = self._create_api_uri('ticker/bookTicker')
        if(symbol == None):
            return self._request_public(uri)
        return self._request_public(uri, symbol=symbol)

    def get_order_book(self, symbol: str, limit: int = 100):
        uri = self._create_api_uri('depth')
        return self._request_public(uri, symbol=symbol, limit=limit)

    def get_avg_price(self, symbol: str) -> dict:
        #avg price does not work with v1
        uri = self._create_api_uri('avgPrice', version='v3') 
        return self._request_public(uri, symbol=symbol)

    def get_24hr_ticker(self, symbol: str = None) -> dict:
        uri = self._create_api_uri('ticker/24hr')
        if(symbol == None):
            return self._request_public(uri)
        return self._request_public(uri, symbol=symbol)

    def get_recent_trades(self, symbol: str, limit: int = 100) -> dict:
        uri = self._create_api_uri('trades')
        return self._request_public(uri, symbol=symbol, limit=limit)

    def get_agg_trades(self, symbol: str,
                       formId: int = None,
                       startTime: int = None,
                       endTime: int = None,
                       limit: int = 500):
        params = locals()
        del params['self']
        params = {k:v for k,v in params.items() if v is not None}
        uri = self._create_api_uri('aggTrades')
        return self._request_public(uri, **params)

    def get_klines(self, symbol: str,
                   interval: str,
                   startTime: Union[int, str] = None,
                   endTime: Union[int, str] = None,
                   limit: int = None):
        
        params = locals()
        if(params['startTime'] != None):
            params['startTime'] = format_time(params['startTime'])
        if(params['endTime'] != None):
            params['endTime'] = format_time(params['endTime'])
        del params['self']
        params = {k:v for k,v in params.items() if v is not None}
        uri = self._create_api_uri('klines')
        return self._request_public(uri, **params)


if __name__ == '__main__':
    pass
