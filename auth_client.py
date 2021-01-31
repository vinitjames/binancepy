from public_client import PublicClient
from api_def import AuthenticatedAPI
from requests import Session
from utils import create_query_string, generate_signature

class AuthenticatedClient(PublicClient, AuthenticatedAPI):

    def __init__(self, api_key: str, api_secret: str,
                 endpoint_version: str='', request_params:dict = None, tld: str='com'):
        
        self.api_key = api_key
        self.api_secret = api_secret

        self.WITHDRAW_API_URL = self.WITHDRAW_API_URL.format(endpoint_version, tld)
        self.MARGIN_API_URL = self.MARGIN_API_URL.format(endpoint_version, tld)
        self.WEBSITE_URL = self.WEBSITE_URL.format(endpoint_version, tld)
        self.FUTURES_URL = self.FUTURES_URL.format(endpoint_version, tld)
                                
        super(AuthenticatedClient, self).__init__(endpoint_version = endpoint_version,
                                                  request_params = request_params,
                                                  tld = tld)
        self._add_apikey_to_header()
            
    def _add_apikey_to_header(self): 
        self.session.headers.update({'X-MBX-APIKEY':self.api_key})

    def _create_withdraw_api_uri(self, path: str):
        return self.WITHDRAW_API__URL + '/' + self.WITHDRAW_API_VERSION + '/' + path

    def __create_margin_api_uri(self, path: str):
        return self.MARGIN_API__URL + '/' + self.MARGIN_API_VERSION + '/' + path

    def _create_futures_api_uri(self, path: str):
        return self.FUTURES_API__URL + '/' + self.FUTURES_API_VERSION + '/' + path

    def _request_auth(self, method: str, path: str,
                      verified: bool, forced_params = False, **params):
        kwargs = {}
        kwargs['timeout'] = 10
        if self._requests_params:
            kwargs.update(self.response_params)
        
        if verified:
            params['timestamp'] = int(time.time() * 1000)
            query_string = create_query_string(params)
            params['signature'] = generate_signature(query_string = query_string,
                                                     api_secret = self.api_secret)

        kwargs[params]=params
            
        response = getattr(self.session, method)(uri, **kwargs)
        return self.handle_response(response)

    
    def _get(self, path, signed=False, version=PUBLIC_API_VERSION, **kwargs):
                return self._request_api('get', path, signed, version, **kwargs)

    def _post(self, path, signed=False, version=PUBLIC_API_VERSION, **kwargs):
        return self._request_api('post', path, signed, version, **kwargs)
    
    def _put(self, path, signed=False, version=PUBLIC_API_VERSION, **kwargs):
        return self._request_api('put', path, signed, version, **kwargs)

    def _delete(self, path, signed=False, version=PUBLIC_API_VERSION, **kwargs):
        return self._request_api('delete', path, signed, version, **kwargs)

    def create(self,
               symbol: str,
               side: str,
               type: str,
               timestamp: int,
               timeInForce: str = None,
               quantity: int = None,
               quoteOrderQty: int = None,
               price: float = None,
               newClientOrderId: str = None,
               stopPrice: float = None,
               icebergQty: float = None,
               newOrderRespType: str =None,
               recvWindow: int = None):

    # to do add conditions on parameters
        pass
        
if __name__ == '__main__':
    pass
