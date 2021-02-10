from .exceptions import BinanceAPIException, BinanceRequestException
from .utils import create_query_string, create_sorted_list, generate_signature
from requests import Session
from requests.models import Response 
import time

class RequestHandler(object):
    def __init__(self,
                 api_key: str = None,
                 api_secret: str = None,
                 request_params: dict = None):
        
        self.api_key = api_key
        self.api_secret = api_secret
        self.request_params = request_params
        self.authenticated = False if((api_key is None) or (api_secret is None)) else True
        self.session = self._init_session()
        
    def _init_session(self) -> Session:
        session = Session()
        session.headers.update({'Accept': 'application/json',
                                'User-Agent': 'binance/python'})
        if self.authenticated:
            session.headers.update({'X-MBX-APIKEY': self.api_key})
        return session

    def _request(self,
                 method: str,
                 uri: str,
                 signed: bool = False,
                 forced_params=False,
                 **params):
        kwargs = {}
        kwargs['timeout'] = 10
        if self.request_params:
            kwargs.update(self.response_params)

        if signed:
            params = create_sorted_list(params)
            params.append(('timestamp', int(time.time() * 1000)))
            query_string = create_query_string(params)
            params.append(('signature' , generate_signature(query_string=query_string,
                                                            api_secret=self.api_secret)))
        kwargs['params'] = params
        response = getattr(self.session, method)(uri, **kwargs)
        return self._handle_response(response)

    def get(self, path, signed=False, **kwargs):
        if not self.authenticated and signed == True:
            raise TypeError("can call post on unauthenticated error")
        return self._request('get', path, signed, **kwargs)

    def post(self, path, signed=False, **kwargs):
        if not self.authenticated:
            raise TypeError("can call post on unauthenticated error")
        return self._request('post', path, signed, **kwargs)

    def put(self, path, signed=False, **kwargs):
        if not self.authenticated:
            raise TypeError("can call put on unauthenticated error")
        return self._request('put', path, signed, version, **kwargs)

    def delete(self, path, signed=False, **kwargs):
        if not self.authenticated:
            raise TypeError("can call delete on unauthenticated error")
        return self._request('delete', path, signed, version, **kwargs)

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
