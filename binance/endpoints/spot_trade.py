from abc import ABCMeta, abstractmethod
from typing import Union
from binance.utils import format_time, interval_to_ms
from binance.exceptions import SpotTradingError

class SpotAccountTradeEndpoints(metaclass = ABCMeta):

    @property
    @abstractmethod
    def request_handler(self):
        pass

    @property
    @abstractmethod
    def API_VERSION(self):
        pass

    @property
    @abstractmethod
    def ORDER_SIDE(self):
        pass
    
    @property
    @abstractmethod
    def ORDER_TYPE(self):
        pass
    
    @abstractmethod
    def _create_api_uri(self, path: str, version:str) -> str:
        pass

    def create_order(self,
                     symbol: str,
                     side: str,
                     type: str,
                     timeInForce: str = None,
                     quantity: float = None,
                     quoteOrderQty: float = None,
                     price: float = None,
                     newClientOrderId: str = None,
                     stopPrice: float = None,
                     icebergQty: float = None,
                     newOrderRespType: str = None,
                     recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        if(params['icebergQty'] is not None):
            params['timeInForce'] = self.TIME_IN_FORCE.GTC
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_api_uri('order',
                                   version=self.API_VERSION.PRIVATE)
        return self.request_handler.post(uri, signed=True, **params)

    def create_test_order(self,
                          symbol: str,
                          side: str,
                          type: str,
                          timeInForce: str = None,
                          quantity: float = None,
                          quoteOrderQty: float = None,
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
                                   version=self.API_VERSION.PRIVATE)
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
            raise SpotAccountTradeError(
                'Atleast on of orderId or origClientOrderId not passed',
                'for cancelling order')
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_api_uri('order',
                                   version=self.API_VERSION.PRIVATE)
        return self.request_handler.delete(uri, signed=True, **params)
    
    def cancel_all_orders(self,
                          symbol: str,
                          recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_api_uri('openOrders',
                                   version=self.API_VERSION.PRIVATE)
        return self.request_handler.delete(uri, signed=True, **params)

    def create_oco_order(self,
                         symbol: str,
                         side: str,
                         quantity: float,
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
                                   version=self.API_VERSION.PRIVATE)
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
        params['side'] = self.ORDER_SIDE.BUY
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
        params['side'] = self.ORDER_SIDE.SELL
        return self.create_oco_order(**params)
    
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
        params['side'] = self.ORDER_SIDE.BUY
        params['type'] = self.ORDER_TYPE.LIMIT
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
        params['side'] = self.ORDER_SIDE.SELL
        params['type'] = self.ORDER_TYPE.LIMIT 
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
        params['side'] = self.ORDER_SIDE.BUY
        params['type'] = self.ORDER_TYPE.LIMIT_MAKER
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
        params['side'] = self.ORDER_SIDE.SELL
        params['type'] = self.ORDER_TYPE.LIMIT_MAKER
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
        if(params['quantity'] is None) and (params['quoteOrderQty'] is None):
            raise SpotTradingError(
                'Atleast one of qantity or quoteOrderQty not specified')
        params['side'] = self.ORDER_SIDE.BUY
        params['type'] = self.ORDER_TYPE.MARKET
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
        if(params['quantity'] is None) and (params['quoteOrderQty'] is None):
            raise SpotTradingError(
                'Atleast one of qantity or quoteOrderQty not specified')
        params['side'] = self.ORDER_SIDE.SELL
        params['type'] = self.ORDER_TYPE.MARKET
        return self.create_order(**params)
    
    def stoploss_buy_order(self,
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
        params['side'] = self.ORDER_SIDE.BUY
        params['type'] = self.ORDER_TYPE.STOP_LOSS 
        
        return self.create_order(**params)

    def stoploss_sell_order(self,
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
        params['side'] = self.ORDER_SIDE.SELL
        params['type'] = self.ORDER_TYPE.STOP_LOSS 
        
        return self.create_order(**params)

    def stoploss_limit_buy_order(self,
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
        params['side'] = self.ORDER_SIDE.BUY
        params['type'] = self.ORDER_TYPE.STOP_LOSS_LIMIT 
        
        return self.create_order(**params)

    def stoploss_limit_sell_order(self,
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
        params['side'] = self.ORDER_SIDE.SELL
        params['type'] = self.ORDER_TYPE.STOP_LOSS_LIMIT 
        
        return self.create_order(**params)

    def takeprofit_buy_order(self,
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
        params['side'] = self.ORDER_SIDE.BUY
        params['type'] = self.ORDER_TYPE.TAKE_PROFIT 
        return self.create_order(**params)

    def takeprofit_sell_order(self,
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
        params['side'] = self.ORDER_SIDE.SELL
        params['type'] = self.ORDER_TYPE.TAKE_PROFIT 
        return self.create_order(**params)

    def takeprofit_limit_buy_order(self,
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
        params['side'] = self.ORDER_SIDE.BUY
        params['type'] = self.ORDER_TYPE.TAKE_PROFIT_LIMIT
        
        return self.create_order(**params)

    def takeprofit_limit_sell_order(self,
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
        params['side'] = self.ORDER_SIDE.SELL
        params['type'] = self.ORDER_TYPE.TAKE_PROFIT_LIMIT
        
        return self.create_order(**params)

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
                                   version=self.API_VERSION.PRIVATE)
        return self.request_handler.get(uri, signed=True, **params)

    def get_open_orders(self,
                        symbol: str = None,
                        recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_api_uri('openOrders',
                                   version=self.API_VERSION.PRIVATE)
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
                                   version=self.API_VERSION.PRIVATE)
        return self.request_handler.get(uri, signed=True, **params)

    def get_account_info(self,
                         recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_api_uri('account',
                                   version=self.API_VERSION.PRIVATE)
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
                                   version=self.API_VERSION.PRIVATE)
        return self.request_handler.get(uri, signed=True, **params)

if __name__ == '__main__':
    pass
