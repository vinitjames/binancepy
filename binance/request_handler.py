from .exceptions import BinanceAPIError, BinanceResponseError
from .exceptions import RequestHandlerError
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
            params.append(('signature', generate_signature(
                query_string=query_string,
                api_secret=self.api_secret)))
        kwargs['params'] = params
        response = getattr(self.session, method)(uri, **kwargs)
        return self._handle_response(response)

    def get(self, path, signed=False, **kwargs):
        if not self.authenticated and signed is True:
            raise RequestHandlerError(
                "Unauthenticated client issued a signed GET http request")
        return self._request('get', path, signed, **kwargs)

    def post(self, path, signed=False, **kwargs):
        if not self.authenticated:
            raise RequestHandlerError(
                "Unauthenticated client issued a POST http request")
        return self._request('post', path, signed, **kwargs)

    def put(self, path, signed=False, **kwargs):
        if not self.authenticated:
            raise RequestHandlerError(
                "Unauthenticated client issued a PUT http request")
        return self._request('put', path, signed, **kwargs)

    def delete(self, path, signed=False, **kwargs):
        if not self.authenticated:
            raise RequestHandlerError(
                "Unauthenticated client issued a DELETE http request")
        return self._request('delete', path, signed, **kwargs)

    @classmethod
    def _handle_response(cls, response: Response) -> dict:
        if(type(response) != Response):
            raise RequestHandlerError(
                " _handle_response called with an argument  which is not of type Response")
        if not (200 <= response.status_code < 300):
            raise BinanceAPIError(response)
        try:
            return response.json()
        except ValueError:
            raise BinanceResponseError("Invalid Response: {}".format(response.text))

        
if __name__ == '__main__':
    pass
