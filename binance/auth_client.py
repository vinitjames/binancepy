from public_client import PublicClient
from api_def import AuthenticatedAPI
from requests import Session
from utils import create_query_string, generate_signature


class AuthenticatedClient(PublicClient, AuthenticatedAPI):

    def __init__(self, api_key: str, api_secret: str,
                 endpoint_version: str = '', request_params: dict = None, tld: str = 'com'):

        self.api_key = api_key
        self.api_secret = api_secret

        self.WITHDRAW_API_URL = self.WITHDRAW_API_URL.format(
            endpoint_version, tld)
        self.MARGIN_API_URL = self.MARGIN_API_URL.format(endpoint_version, tld)
        self.WEBSITE_URL = self.WEBSITE_URL.format(endpoint_version, tld)
        self.FUTURES_URL = self.FUTURES_URL.format(endpoint_version, tld)

        super(AuthenticatedClient, self).__init__(endpoint_version=endpoint_version,
                                                  request_params=request_params,
                                                  tld=tld)
        self._add_apikey_to_header()

    def _add_apikey_to_header(self):
        self.session.headers.update({'X-MBX-APIKEY': self.api_key})

    def _create_withdraw_api_uri(self, path: str):
        return self.WITHDRAW_API__URL + '/' + self.WITHDRAW_API_VERSION + '/' + path

    def __create_margin_api_uri(self, path: str):
        return self.MARGIN_API__URL + '/' + self.MARGIN_API_VERSION + '/' + path

    def _create_futures_api_uri(self, path: str):
        return self.FUTURES_API__URL + '/' + self.FUTURES_API_VERSION + '/' + path

    def _request_auth(self, method: str, path: str,
                      signed: bool, forced_params=False, **params):
        kwargs = {}
        kwargs['timeout'] = 10
        if self._requests_params:
            kwargs.update(self.response_params)

        if verified:
            params['timestamp'] = int(time.time() * 1000)
            query_string = create_query_string(params)
            params['signature'] = generate_signature(query_string=query_string,
                                                     api_secret=self.api_secret)

        kwargs[params] = params

        response = getattr(self.session, method)(uri, **kwargs)
        return self.handle_response(response)

    def _get(self, path, signed=False, **kwargs):
        return self._request_auth('get', path, signed, **kwargs)

    def _post(self, path, signed=False, **kwargs):
        return self._request_auth('post', path, signed, **kwargs)

    def _put(self, path, signed=False, **kwargs):
        return self._request_auth('put', path, signed, version, **kwargs)

    def _delete(self, path, signed=False, **kwargs):
        return self._request_auth('delete', path, signed, version, **kwargs)

    def create_order(self,
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
                     newOrderRespType: str = None,
                     recvWindow: int = None) -> dict:

        params = locals()
        params = {k: v for k, v in params.iteritems() if v is not None}
        uri = self._create_api_uri('order',
                                   version=self.PRIVATE_API_VERSION)
        return self._post(uri, signed=True, **params)

    def create_oco_order(self,
                         symbol: str,
                         side: str,
                         quantity: int,
                         price: float,
                         type: str,
                         timestamp: int,
                         timeInForce: str = None,

                         quoteOrderQty: int = None,

                         newClientOrderId: str = None,
                         stopPrice: float = None,
                         icebergQty: float = None,
                         newOrderRespType: str = None,
                         recvWindow: int = None) -> dict:

        params = locals()
        params = {k: v for k, v in params.iteritems() if v is not None}
        uri = self._create_api_uri('order',
                                   version=self.PRIVATE_API_VERSION)
        return self._post(uri, signed=True, **params)

    def create_test_order(self,
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
                          newOrderRespType: str = None,
                          recvWindow: int = None) -> dict:

        params = locals()
        params = {k: v for k, v in params.iteritems() if v is not None}
        uri = self._create_api_uri('order/test',
                                   version=self.PRIVATE_API_VERSION)
        return self._post(uri, signed=True, **params)

    def cancel_order(self,
                     symbol: str,
                     timestamp: int,
                     orderId: int = None,
                     origClientOrderId: str = None,
                     newClientOrderId: str = None,
                     recvWindow: int = None) -> dict:

        params = locals()
        if(params['orderId'] == None) and (params['origClientOrderId'] == None):
            raise ValueError('Atleast on of orderId or origClientOrderId not passed',
                             'for cancelling order')
        params = {k: v for k, v in params.iteritems() if v is not None}
        uri = self._create_api_uri('order',
                                   version=self.PRIVATE_API_VERSION)
        return self._delete(uri, signed=True, **params)

    def cancel_all_orders(self,
                          symbol: str,
                          timestamp: int,
                          recvWindow: int = None) -> dict:
        params = locals()
        params = {k: v for k, v in params.iteritems() if v is not None}
        uri = self._create_api_uri('openOrders',
                                   version=self.PRIVATE_API_VERSION)
        return self._delete(uri, signed=True, **params)

    def query_order(self,
                    symbol: str,
                    timestamp: int,
                    orderId: int = None,
                    origClientOrderId: str = None,
                    recvWindow: int = None) -> dict:

        params = locals()
        if(params['orderId'] == None) and (params['origClientOrderId'] == None):
            raise ValueError('Atleast on of orderId or origClientOrderId not passed',
                             'for querying  order')
        params = {k: v for k, v in params.iteritems() if v is not None}
        uri = self._create_api_uri('order',
                                   version=self.PRIVATE_API_VERSION)
        return self._get(uri, signed=True, **params)

    def query_open_orders(self,
                          timestamp: int,
                          symbol: str = None,
                          recvWindow: int = None) -> dict:

        params = locals()
        params = {k: v for k, v in params.iteritems() if v is not None}
        uri = self._create_api_uri('openOrders',
                                   version=self.PRIVATE_API_VERSION)
        return self._get(uri, signed=True, **params)

    def query_all_orders(self,
                         symbol: str,
                         orderId: str = None,
                         startTime: int = None,
                         endTime: int = None,
                         limit: int = None,
                         recvWindow: int = None) -> dict:

        params = locals()
        params = {k: v for k, v in params.iteritems() if v is not None}
        uri = self._create_api_uri('allOrders',
                                   version=self.PRIVATE_API_VERSION)
        return self._get(uri, signed=True, **params)

    def query_account_info(self,
                           recvWindow: int = None) -> dict:

        params = locals()
        params = {k: v for k, v in params.iteritems() if v is not None}
        uri = self._create_api_uri('account',
                                   version=self.PRIVATE_API_VERSION)
        return self._get(uri, signed=True, **params)

    def query_trade_list(self,
                         symbol: str,
                         startTime: int = None,
                         endTime: int = None,
                         formId: int = None,
                         limit: int = None,
                         recvWindow: int = None) -> dict:

        params = locals()
        params = {k: v for k, v in params.iteritems() if v is not None}
        uri = self._create_api_uri('myTrades',
                                   version=self.PRIVATE_API_VERSION)
        return self._get(uri, signed=True, **params)


if __name__ == '__main__':
    pass
