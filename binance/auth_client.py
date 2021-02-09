from .public_client import PublicClient
from .api_def import AuthenticatedAPI
#from requests import Session
from .request_handler import RequestHandler
from .utils import create_query_string, create_sorted_list, generate_signature
from .wallet import Wallet
import time

class AuthenticatedClient(PublicClient, AuthenticatedAPI):

    def __init__(self,
                 api_key: str,
                 api_secret: str,
                 endpoint_version: str = '',
                 request_params: dict = None,
                 tld: str = 'com'):

        super(AuthenticatedClient, self).__init__(endpoint_version=endpoint_version,
                                                  request_params=request_params,
                                                  tld=tld)
      
        self.WITHDRAW_API_URL = self.WITHDRAW_API_URL.format(endpoint_version, tld)
        self.MARGIN_API_URL = self.MARGIN_API_URL.format(endpoint_version, tld)
        self.WEBSITE_URL = self.WEBSITE_URL.format(endpoint_version, tld)
        self.FUTURES_URL = self.FUTURES_URL.format(endpoint_version, tld)
        self.request_handler = RequestHandler(api_key = api_key,
                                              api_secret = api_secret,
                                              request_params = request_params)
        self.wallet = Wallet(self.request_handler)
        #self._add_apikey_to_header()

    def _add_apikey_to_header(self):
        self.session.headers.update({'X-MBX-APIKEY': self.api_key})

    def __create_margin_api_uri(self, path: str):
        return self.MARGIN_API__URL + '/' + self.MARGIN_API_VERSION + '/' + path

    def _create_futures_api_uri(self, path: str):
        return self.FUTURES_API__URL + '/' + self.FUTURES_API_VERSION + '/' + path
    '''
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
    '''
    def create_order(self,
                     symbol: str,
                     side: str,
                     type: str,
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
        return self.request_handler.post(uri, signed=True, **params)

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
        params['type'] = self.ORDER_TYPE_LIMIT 
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
        return self.request_handler.post(uri, signed=True, **params)

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
        return self.create_oco_order(**params)

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
        return self.create_oco_order(**params)

    def create_test_order(self,
                          symbol: str,
                          side: str,
                          type: str,
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
        return self.request_handler.post(uri, signed=True, **params)

    def cancel_order(self,
                     symbol: str,
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
        return self.request_handler.delete(uri, signed=True, **params)
    
    def cancel_all_orders(self,
                          symbol: str,
                          recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_api_uri('openOrders',
                                   version=self.PRIVATE_API_VERSION)
        return self.request_handler.delete(uri, signed=True, **params)

    def get_order(self,
                  symbol: str,
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
        return self.request_handler.get(uri, signed=True, **params)

    def get_open_orders(self,
                        symbol: str = None,
                        recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_api_uri('openOrders',
                                   version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)

    def get_all_orders(self,
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
        return self.request_handler.get(uri, signed=True, **params)

    def get_account_info(self,
                         recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_api_uri('account',
                                   version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)

    def get_trade_list(self,
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
        return self.request_handler.get(uri, signed=True, **params)

    
    # margin endpoints
    def transfer_margin_to_spot(self,
                                asset: str,
                                amount: float,
                                recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['type'] = 2
        params = {k: v for k, v in params.items() if v is not None}
        
        uri = self._create_margin_api_uri('margin/transfer',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.post(uri, signed=True, **params)

    def transfer_spot_to_margin(self,
                                asset: str,
                                amount: float,
                                recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['type'] = 1
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_margin_api_uri('margin/transfer',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.post(uri, signed=True, **params)

    def margin_account_borrow(self,
                              asset: str,
                              amount: float,
                              isIsolated: bool = False,
                              symbol: str = None,
                              recvWindow: int = None):
        
        if(isIsolated == True) and (symbol == None):
            raise ValueError("isIsolated is true but symbol not specified")
        params = locals()
        del params['self']
        params['type'] = 1
        params = {k: v for k, v in params.items() if v is not None}
        params['isIsolated'] = 'TRUE' if (params['isIsolated'] == True) else 'FALSE'
        uri = self._create_margin_api_uri('margin/loan',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.post(uri, signed=True, **params)

    def margin_account_repay(self,
                             asset: str,
                             amount: float,
                             isIsolated: bool = False,
                             symbol: str = None,
                             recvWindow: int = None):
        
        if(isIsolated == True) and (symbol == None):
            raise ValueError("isIsolated is true but symbol not specified")
        params = locals()
        del params['self']
        params['type'] = 1
        params = {k: v for k, v in params.items() if v is not None}
        params['isIsolated'] = 'TRUE' if (params['isIsolated'] == True) else 'FALSE'
        uri = self._create_margin_api_uri('margin/repay',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.post(uri, signed=True, **params)

    def query_margin_asset(self,
                           asset: str):
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_margin_api_uri('margin/asset',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)

    def query_cross_margin_pair(self,
                                symbol: str):
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_margin_api_uri('margin/pair',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)

    def get_all_margin_assets(self):
        uri = self._create_margin_api_uri('margin/allAssets',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True)

    def get_all_cross_margin_pairs(self):
        uri = self._create_margin_api_uri('margin/allPairs',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True)

    def query_cross_margin_price_index(self,
                                       symbol: str):
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_margin_api_uri('margin/priceIndex',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)


    def create_margin_order(self,
                            symbol: str,
                            side: str,
                            type: str,
                            isIsolated: bool = False,
                            timeInForce: str = None,
                            quantity: float = None,
                            quoteOrderQty: float = None,
                            price: float = None,
                            newClientOrderId: str = None,
                            stopPrice: float = None,
                            icebergQty: float = None,
                            newOrderRespType: str = None,
                            sideEffectType: str = None,
                            recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        params['isIsolated'] = 'TRUE' if (params['isIsolated'] == True) else 'FALSE'
        uri = self._create_margin_api_uri('margin/order',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.post(uri, signed=True, **params)

    def margin_limit_buy_order(self,
                               symbol: str,
                               isIsolated: bool = False,
                               timeInForce: str = None,
                               quantity: float = None,
                               quoteOrderQty: float = None,
                               price: float = None,
                               newClientOrderId: str = None,
                               icebergQty: float = None,
                               newOrderRespType: str = None,
                               sideEffectType: str = None,
                               recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_BUY
        params['type'] = self.ORDER_TYPE_LIMIT
        return self.create_margin_order(**params)

    def margin_limit_sell_order(self,
                                symbol: str,
                                isIsolated: bool = False,
                                timeInForce: str = None,
                                quantity: float = None,
                                quoteOrderQty: float = None,
                                price: float = None,
                                newClientOrderId: str = None,
                                icebergQty: float = None,
                                newOrderRespType: str = None,
                                sideEffectType: str = None,
                                recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_SELL
        params['type'] = self.ORDER_TYPE_LIMIT
        return self.create_margin_order(**params)

    def margin_market_buy_order(self,
                                symbol: str,
                                isIsolated: bool = False,
                                timeInForce: str = None,
                                quantity: float = None,
                                quoteOrderQty: float = None,
                                newClientOrderId: str = None,
                                newOrderRespType: str = None,
                                sideEffectType: str = None,
                                recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_BUY
        params['type'] = self.ORDER_TYPE_MARKET
        return self.create_margin_order(**params)

    def margin_market_sell_order(self,
                                 symbol: str,
                                 isIsolated: bool = False,
                                 timeInForce: str = None,
                                 quantity: float = None,
                                 quoteOrderQty: float = None,
                                 newClientOrderId: str = None,
                                 newOrderRespType: str = None,
                                 sideEffectType: str = None,
                                 recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_SELL
        params['type'] = self.ORDER_TYPE_MARKET
        return self.create_margin_order(**params)
    
    def margin_limit_stop_loss_buy_order(self,
                                         symbol: str,
                                         stopPrice: float,
                                         isIsolated: bool = False,
                                         timeInForce: str = None,
                                         quantity: float = None,
                                         quoteOrderQty: float = None,
                                         price: float = None,
                                         newClientOrderId: str = None,
                                         icebergQty: float = None,
                                         newOrderRespType: str = None,
                                         sideEffectType: str = None,
                                         recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_BUY
        params['type'] = self.ORDER_TYPE_STOP_LOSS_LIMIT
        return self.create_margin_order(**params)

    def margin_limit_stop_loss_sell_order(self,
                                          symbol: str,
                                          stopPrice: float,
                                          isIsolated: bool = False,
                                          timeInForce: str = None,
                                          quantity: float = None,
                                          quoteOrderQty: float = None,
                                          price: float = None,
                                          newClientOrderId: str = None,
                                          icebergQty: float = None,
                                          newOrderRespType: str = None,
                                          sideEffectType: str = None,
                                          recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_SELL
        params['type'] = self.ORDER_TYPE_STOP_LOSS_LIMIT
        return self.create_margin_order(**params)

    def margin_stop_loss_buy_order(self,
                                   symbol: str,
                                   stopPrice: float,
                                   isIsolated: bool = False,
                                   timeInForce: str = None,
                                   quantity: float = None,
                                   quoteOrderQty: float = None,
                                   price: float = None,
                                   newClientOrderId: str = None,
                                   newOrderRespType: str = None,
                                   sideEffectType: str = None,
                                   recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_BUY
        params['type'] = self.ORDER_TYPE_STOP_LOSS
        return self.create_margin_order(**params)

    def margin_stop_loss_sell_order(self,
                                    symbol: str,
                                    stopPrice: float,
                                    isIsolated: bool = False,
                                    timeInForce: str = None,
                                    quantity: float = None,
                                    quoteOrderQty: float = None,
                                    price: float = None,
                                    newClientOrderId: str = None,
                                    newOrderRespType: str = None,
                                    sideEffectType: str = None,
                                    recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_SELL
        params['type'] = self.ORDER_TYPE_STOP_LOSS
        return self.create_margin_order(**params)

    def margin_take_profit_buy_order(self,
                                     symbol: str,
                                     stopPrice: float,
                                     isIsolated: bool = False,
                                     timeInForce: str = None,
                                     quantity: float = None,
                                     quoteOrderQty: float = None,
                                     price: float = None,
                                     newClientOrderId: str = None,
                                     newOrderRespType: str = None,
                                     sideEffectType: str = None,
                                     recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_BUY
        params['type'] = self.ORDER_TYPE_TAKE_PROFIT
        return self.create_margin_order(**params)

    def margin_take_profit_sell_order(self,
                                     symbol: str,
                                      stopPrice: float,
                                      isIsolated: bool = False,
                                      timeInForce: str = None,
                                      quantity: float = None,
                                      quoteOrderQty: float = None,
                                      price: float = None,
                                      newClientOrderId: str = None,
                                      newOrderRespType: str = None,
                                      sideEffectType: str = None,
                                      recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_SELL
        params['type'] = self.ORDER_TYPE_TAKE_PROFIT
        return self.create_margin_order(**params)
    
    def margin_take_profit_limit_buy_order(self,
                                           symbol: str,
                                           stopPrice: float,
                                           isIsolated: bool = False,
                                           timeInForce: str = None,
                                           quantity: float = None,
                                           quoteOrderQty: float = None,
                                           price: float = None,
                                           icebergQty: float = None,
                                           newClientOrderId: str = None,
                                           newOrderRespType: str = None,
                                           sideEffectType: str = None,
                                           recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_BUY
        params['type'] = self.ORDER_TYPE_TAKE_PROFIT_LIMIT
        return self.create_margin_order(**params)

    def margin_take_profit_limit_buy_order(self,
                                           symbol: str,
                                           stopPrice: float,
                                           isIsolated: bool = False,
                                           timeInForce: str = None,
                                           quantity: float = None,
                                           quoteOrderQty: float = None,
                                           price: float = None,
                                           icebergQty: float = None,
                                           newClientOrderId: str = None,
                                           newOrderRespType: str = None,
                                           sideEffectType: str = None,
                                           recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE_BUY
        params['type'] = self.ORDER_TYPE_TAKE_PROFIT_LIMIT
        return self.create_margin_order(**params)
        
    def cancel_margin_order(self,
                            symbol: str,
                            isIsolated: bool = False,
                            orderId:int = None,
                            origClientOrderId: str = None,
                            newClientOrderId: str = None,                            
                            recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params['isIsolated'] = 'TRUE' if (params['isIsolated'] == True) else 'FALSE'
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_margin_api_uri('margin/order',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.delete(uri, signed=True, **params)

    def cancel_all_margin_order(self,
                                symbol: str,
                                isIsolated: bool = False,
                                orderId:int = None,
                                origClientOrderId: str = None,
                                newClientOrderId: str = None,                            
                                recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params['isIsolated'] = 'TRUE' if (params['isIsolated'] == True) else 'FALSE'
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_margin_api_uri('margin/openOrders',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.delete(uri, signed=True, **params)

    
    def get_cross_margin_transfer_history(self,
                                          asset: str = None,
                                          type: str = None,
                                          startTime: int = None,
                                          endTime: int = None,
                                          current: int = 1,
                                          size: int = 10,
                                          archived: bool = False,
                                          recvWindow: int = None):
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_margin_api_uri('margin/transfer',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)

    def query_margin_loan_record(self,
                                 asset: str,
                                 isolatedSymbol: str = None,
                                 txId: int = None,
                                 startTime: int = None,
                                 endTime: int = None,
                                 current: int = 1,
                                 size: int = 10,
                                 archived: bool = False,
                                 recvWindow: int = None):
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_margin_api_uri('margin/loan',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)

    def query_margin_repay_record(self,
                                  asset: str,
                                  isolatedSymbol: str = None,
                                  txId: int = None,
                                  startTime: int = None,
                                  endTime: int = None,
                                  current: int = 1,
                                  size: int = 10,
                                  archived: bool = False,
                                  recvWindow: int = None):
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_margin_api_uri('margin/repay',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)

    def get_margin_interest_history(self,
                                    asset: str,
                                    isolatedSymbol: str = None,
                                    txId: int = None,
                                    startTime: int = None,
                                    endTime: int = None,
                                    current: int = 1,
                                    size: int = 10,
                                    archived: bool = False,
                                    recvWindow: int = None):
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_margin_api_uri('margin/interestHistory',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)

    def get_margin_force_liquidation_record(self,
                                            isolatedSymbol: str = None,
                                            txId: int = None,
                                            startTime: int = None,
                                            endTime: int = None,
                                            current: int = 1,
                                            size: int = 10,
                                            recvWindow: int = None):
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_margin_api_uri('margin/forceLiquidationRec',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)

    def query_cross_margin_account_details(self,
                                            recvWindow: int = None):
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_margin_api_uri('margin/account',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)

    def query_margin_account_order(self,
                                   symbol: str,
                                   isIsolated: bool = False,
                                   orderId: str = None,
                                   orderClientOrderId: str = None,
                                   recvWindow: int = None):
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        params['isIsolated'] = 'TRUE' if (params['isIsolated'] == True) else 'FALSE'
        uri = self._create_margin_api_uri('margin/order',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)

    def query_margin_account_open_orders(self,
                                         symbol: str = None,
                                         isIsolated: bool = False,
                                         recvWindow: int = None):
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        params['isIsolated'] = 'TRUE' if (params['isIsolated'] == True) else 'FALSE'
        uri = self._create_margin_api_uri('margin/openOrders',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)

    def query_margin_account_order(self,
                                   symbol: str,
                                   isIsolated: bool = False,
                                   orderId: str = None,
                                   startTime: int = None,
                                   endTime: int = None,
                                   limit: int = 500,
                                   recvWindow: int = None):
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        params['isIsolated'] = 'TRUE' if (params['isIsolated'] == True) else 'FALSE'
        uri = self._create_margin_api_uri('margin/allOrders',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)
    
    
if __name__ == '__main__':
    pass
