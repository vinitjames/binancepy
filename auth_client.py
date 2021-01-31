from public_client import PublicClient
from api_def import AuthenticatedAPI
from requests import Session

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

    def _request_auth(self, ):
        pass
        
if __name__ == '__main__':
    import ipdb; ipdb.set_trace() 
