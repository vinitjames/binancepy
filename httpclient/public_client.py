import api_def
from requests import Session
from requests.models import Response
from exceptions import BinanceAPIException, BinanceRequestException

class PublicClient(object):
    
    def __init__(self, api_key: str=None, endpoint_version: str='', tld: str='com'):
        self.api_url = API_URL.format(endpoint_version, tld)
        self.website_url = WEBSITE_URL.format(endpoint_version, tld)
        self.session = Session()
        self.api_key = api_key;
    
    def _init_session(self) -> Session:
        session = Session().headers.update({'Accept':'application/json',
                                            'User-Agent':'binance/python'})
        return session

    def create_api_uri(self, path: str, signed = False, version = PUBLIC_API_VERSION):
        if signed:
            version = PRIVATE_API_VERSION
        return self.api_url + '/' + version + '/' + path
    
    def _request(self, method, uri, **kwargs):
        response = getattr(self.session, method)(uri, **kwargs) 
        return self._handle(response)

            
    def _get(self, path: str, **kwargs) -> dict:
        return self._request('get', path, **kwargs)
    
    def _post(self, path: str, **kwargs)-> dict:
        return self._request('post', path, **kwargs)
    
    def _put(self, path: str, **kwargs) -> dict:
        return self._request('put', path, **kwargs)
    
    def _delete(self, path: str, **kwargs) -> dict:
        return self._request('delete', path, **kwargs)


    @classmethod
    def _handle_response(cls, response: Response) -> dict:
        if(type(response) != Response):
            raise ValueError("Client Error: _handle resource was not called with Response Type")
        if( not str(response.status_code).startswith('2')):
            raise BinanceAPIException(response)

        try:
            return response.json()
        except ValueError:
            raise BinanceRequestException(response)
        

    def ping(self) -> dict: 
        uri = self.create_api_uri('ping')
        return self._get(uri)

    def get_server_time(self) -> dict:
        uri = self.create_api_uri('time')
        return self._get(uri)

    def get_exchange_info(self) -> dict:
        uri = self.create_api_uri('exchangeInfo')
        return self._get(uri)

    def get_symbol_info(self, symbol: str) -> dict:
        resp_data = get_exchange_info()
        for sym_data in resp_data['symbol']:
            if(sym_data['symbol'] == symbol.upper()):
                return sym_data
        return None

    def get_price_ticker(self, symbol: str = None) -> dict:
        uri = self.create_api_uri('ticker/price')
        if(symbol == None):
            return self._get(uri)
        return self._get(uri, symbol = symbol)

    def get_orderbook_ticker(self, symbol: str = None) -> dict:
        uri = self.create_api_uri('ticker/bookTricker')
        if(symbol == None):
            return self._get(uri)
        return self._get(uri, symbol = symbol)

    
    def get_order_book(self, symbol: str, limit: int = 100):
        uri = self.create_api_uri('depth')
        return self._get(uri, symbol = symbol, limit = limit)

    def get_avg_price(self, symbol: str = None)->dict:
        uri = self.create_api_uri('avgPrice')
        return self._get(uri, symbol = symbol)

    def get_price_ticker(self, symbol: str = None) -> dict:
        uri = self.create_api_uri('ticker/24hr')
        if(symbol == None):
            return self._get(uri)
        return self._get(uri, symbol = symbol)
        
        

    
        
        
    
        
