from .public_client import PublicClient
from .api_def import AuthenticatedAPI
from requests import Session
from .utils import create_query_string, create_sorted_list, generate_signature
import time

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

    def _request_auth(self, method: str, uri: str,
                      signed: bool, forced_params=False, **params):
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
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_api_uri('order',
                                   version=self.PRIVATE_API_VERSION)
        return self._post(uri, signed=True, **params)

    def limit_buy_order(self,
                        symbol: str,
                        price: float,
                        quantity: int,
                        timeInForce: str,
                        quoteOrderQty: int = None, 
                        newClientOrderId: str = None,
                        icebergQty: float = None,
                        newOrderRespType: str = None,
                        recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_BUY
        params['type'] = self.ORDER_TYPE_LIMIT
        return self.create_order(**params)
    
    def limit_sell_order(self,
                         symbol: str,
                         price: float,
                         quantity: int,
                         timeInForce: str,
                         quoteOrderQty: int = None, 
                         newClientOrderId: str = None,
                         icebergQty: float = None,
                         newOrderRespType: str = None,
                         recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_SELL
        params['type'] = self.ORDER_TYPE_STOP_LOSS_LIMIT \
            if stopPrice != None else self.ORDER_TYPE_LIMIT
        
        return self.create_order(**params)

    def limit_maker_buy_order(self,
                              symbol: str,
                              price: float,
                              quantity: int,
                              timeInForce: str = None,
                              quoteOrderQty: int = None, 
                              newClientOrderId: str = None,
                              icebergQty: float = None,
                              newOrderRespType: str = None,
                              recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_BUY
        params['type'] = self.ORDER_TYPE_LIMIT_MAKER
        return self.create_order(**params)

    def limit_maker_sell_order(self,
                               symbol: str,
                               price: float,
                               quantity: int,
                               timeInForce: str = None,
                               quoteOrderQty: int = None, 
                               newClientOrderId: str = None,
                               icebergQty: float = None,
                               newOrderRespType: str = None,
                               recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_SELL
        params['type'] = self.ORDER_TYPE_LIMIT_MAKER
        return self.create_order(**params)

    def market_buy_order(self,
                         symbol: str,
                         quantity: int = None,
                         quoteOrderQty: int = None, 
                         timeInForce: str = None,
                         newClientOrderId: str = None,
                         newOrderRespType: str = None,
                         recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        if(params['quantity'] == None) and (params['quoteOrderQty'] == None):
            raise ValueError('Atleast one of qantity or quoteOrderQty not specified')
        params['side'] = self.ORDER_SIDE_BUY
        params['type'] = self.ORDER_TYPE_MARKET
        return self.create_order(**params)


    def market_sell_order(self,
                          symbol: str,
                          quantity: int = None,
                          quoteOrderQty: int = None, 
                          timeInForce: str = None,
                          newClientOrderId: str = None,
                          newOrderRespType: str = None,
                          recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        if(params['quantity'] == None) and (params['quoteOrderQty'] == None):
            raise ValueError('Atleast one of qantity or quoteOrderQty not specified')
        params['side'] = self.ORDER_SIDE_SELL
        params['type'] = self.ORDER_TYPE_MARKET
        return self.create_order(**params)
    
    
    def stoploss_buy(self,
                     symbol: str,
                     quantity: int,
                     stopPrice:str,
                     timeInForce: str = None,
                     quoteOrderQty: int = None, 
                     newClientOrderId: str = None,
                     newOrderRespType: str = None,
                     recvWindow: int = None) -> dict :
        
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_BUY
        params['type'] = self.ORDER_TYPE_STOP_LOSS 
        
        return self.create_order(**params)

    def stoploss_sell(self,
                      symbol: str,
                      quantity: int,
                      stopPrice:str,
                      timeInForce: str = None,
                      quoteOrderQty: int = None, 
                      newClientOrderId: str = None,
                      newOrderRespType: str = None,
                      recvWindow: int = None) -> dict :
        
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_SELL
        params['type'] = self.ORDER_TYPE_STOP_LOSS 
        
        return self.create_order(**params)

    def stoploss_limit_buy(self,
                           symbol: str,
                           price:str,
                           quantity: int,
                           timeInForce: str,
                           stopPrice:str,
                           quoteOrderQty: int = None, 
                           newClientOrderId: str = None,
                           icebergQty: float = None,
                           newOrderRespType: str = None,
                           recvWindow: int = None) -> dict :
        
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_BUY
        params['type'] = self.ORDER_TYPE_STOP_LOSS_LIMIT 
        
        return self.create_order(**params)

    def stoploss_limit_sell(self,
                            symbol: str,
                            price:str,
                            quantity: int,
                            timeInForce: str,
                            stopPrice:str,
                            quoteOrderQty: int = None, 
                            newClientOrderId: str = None,
                            icebergQty: float = None,
                            newOrderRespType: str = None,
                            recvWindow: int = None) -> dict :
        
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_SELL
        params['type'] = self.ORDER_TYPE_STOP_LOSS_LIMIT 
        
        return self.create_order(**params)

    def takeprofit_buy(self,
                       symbol: str,
                       quantity: int,
                       stopPrice:str,
                       timeInForce: str = None,
                       quoteOrderQty: int = None, 
                       newClientOrderId: str = None,
                       newOrderRespType: str = None,
                       recvWindow: int = None) -> dict :
        
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_BUY
        params['type'] = self.ORDER_TYPE_TAKE_PROFIT 
        
        return self.create_order(**params)

    def takeprofit_sell(self,
                        symbol: str,
                        quantity: int,
                        stopPrice:str,
                        timeInForce: str = None,
                        quoteOrderQty: int = None, 
                        newClientOrderId: str = None,
                        newOrderRespType: str = None,
                        recvWindow: int = None) -> dict :
        
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_BUY
        params['type'] = self.ORDER_TYPE_TAKE_PROFIT 
        
        return self.create_order(**params)

    def takeprofit_limit_buy(self,
                             symbol: str,
                             quantity: int,
                             stopPrice:str,
                             timeInForce: str,
                             icebergQty: float = None,
                             quoteOrderQty: int = None, 
                             newClientOrderId: str = None,
                             newOrderRespType: str = None,
                             recvWindow: int = None) -> dict :
        
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_BUY
        params['type'] = self.ORDER_TYPE_TAKE_PROFIT_LIMIT
        
        return self.create_order(**params)

    def takeprofit_limit_sell(self,
                              symbol: str,
                              quantity: int,
                              stopPrice:str,
                              timeInForce: str,
                              icebergQty: float = None,
                              quoteOrderQty: int = None, 
                              newClientOrderId: str = None,
                              newOrderRespType: str = None,
                              recvWindow: int = None) -> dict :
        
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_SELL
        params['type'] = self.ORDER_TYPE_TAKE_PROFIT_LIMIT
        
        return self.create_order(**params)

    
    
    def create_oco_order(self,
                         symbol: str,
                         side: str,
                         quantity: int,
                         price: float,
                         stopPrice: float,
                         listClientOrderId: str = None,
                         limitClientOrderId: str = None,
                         
                         limitIcebergQty: float = None,
                         stopClientOrderId: str = None,
                         stopLimitPrice: float = None,
                         stopIcebergQty: float = None,
                         stopLimitTimeInForce: str = None,
                         newOrderRespType: str = None,
                         recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_api_uri('order/oco',
                                   version=self.PRIVATE_API_VERSION)
        return self._post(uri, signed=True, **params)

    def oco_buy_order(self,
                      symbol: str,
                      quantity: int,
                      price: float,
                      stopPrice: float,
                      listClientOrderId: str = None,
                      limitClientOrderId: str = None,   
                      limitIcebergQty: float = None,
                      stopClientOrderId: str = None,
                      stopLimitPrice: float = None,
                      stopIcebergQty: float = None,
                      stopLimitTimeInForce: str = None,
                      newOrderRespType: str = None,
                      recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_BUY
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_api_uri('order/oco',
                                   version=self.PRIVATE_API_VERSION)
        return self._post(uri, signed=True, **params)

    def oco_sell_order(self,
                       symbol: str,
                       quantity: int,
                       price: float,
                       stopPrice: float,
                       listClientOrderId: str = None,
                       limitClientOrderId: str = None,   
                       limitIcebergQty: float = None,
                       stopClientOrderId: str = None,
                       stopLimitPrice: float = None,
                       stopIcebergQty: float = None,
                       stopLimitTimeInForce: str = None,
                       newOrderRespType: str = None,
                       recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_SELL
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_api_uri('order/oco',
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
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
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
        del params['self']
        if(params['orderId'] == None) and (params['origClientOrderId'] == None):
            raise ValueError('Atleast on of orderId or origClientOrderId not passed',
                             'for cancelling order')
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_api_uri('order',
                                   version=self.PRIVATE_API_VERSION)
        return self._delete(uri, signed=True, **params)

    def cancel_all_orders(self,
                          symbol: str,
                          timestamp: int,
                          recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
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
        del params['self']
        if(params['orderId'] == None) and (params['origClientOrderId'] == None):
            raise ValueError('Atleast on of orderId or origClientOrderId not passed',
                             'for querying  order')
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_api_uri('order',
                                   version=self.PRIVATE_API_VERSION)
        return self._get(uri, signed=True, **params)

    def query_open_orders(self,
                          timestamp: int,
                          symbol: str = None,
                          recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
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
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_api_uri('allOrders',
                                   version=self.PRIVATE_API_VERSION)
        return self._get(uri, signed=True, **params)

    def query_account_info(self,
                           recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
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
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_api_uri('myTrades',
                                   version=self.PRIVATE_API_VERSION)
        return self._get(uri, signed=True, **params)

    

if __name__ == '__main__':
    pass
