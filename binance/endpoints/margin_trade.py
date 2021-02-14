from abc import ABCMeta, abstractmethod
from typing import Union
from binance.utils import format_time, interval_to_ms

class MarginAccountEndpoints(metaclass = ABCMeta):
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
