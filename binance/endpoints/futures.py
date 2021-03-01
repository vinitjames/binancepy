from abc import ABCMeta, abstractmethod
from typing import Union
from binance.utils import format_time
from binance.exceptions import FuturesTradingError

class FuturesEndpoints(metaclass = ABCMeta):

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
    def FUTURES_TRANSFER_TYPE(self):
        pass
    
    @abstractmethod
    def _create_futures_api_uri(self, path: str, version:str) -> str:
        pass

    def future_account_transfer(self,
                                asset: str,
                                amount: float,
                                type: int,
                                recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_futures_api_uri('futures/transfer')
        return self.request_handler.post(uri, signed=True, **params)

    def get_future_transaction_history(self,
                                       asset: str,
                                       startTime: Union[int, str] = None,
                                       endTime: Union[int, str] = None,
                                       current: int = None,
                                       size: int = None,
                                       recvWindow: int = None) -> dict :
        params = locals()
        del params['self']
        if params['startTime'] is not None:
            params['startTime'] = format_time(params['startTime'])
        if params['endTime'] is not None:
            params['endTime'] = format_time(params['endTime'])
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_futures_api_uri('futures/transfer')
        return self.request_handler.get(uri, signed=True, **params)

    def cross_collateral_borrow(self,
                                coin: str,
                                collateralCoin: str,
                                amount: float = None,
                                collateralAmount: float = None,
                                recvWindow: int = None) -> dict :
        
        params = locals()
        del params['self']        
        if (params['amount'] is None) and (params['collateralAmount'] is None):
            raise FuturesTradingError("amount or collateralAmount not provided for borrow cross collateral")
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_futures_api_uri('futures/loan/borrow')
        return self.request_handler.post(uri, signed=True, **params)

    def cross_collateral_borrow_history(self,
                                        coin: str = None,
                                        startTime: Union[int, str] = None,
                                        endTime: Union[int, str] = None,
                                        limit: int = None,
                                        recvWindow: int = None) -> dict :
        
        params = locals()
        del params['self']
        if params['startTime'] is not None:
            params['startTime'] = format_time(params['startTime'])
        if params['endTime'] is not None:
            params['endTime'] = format_time(params['endTime'])
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_futures_api_uri('futures/loan/borrow/history')
        return self.request_handler.get(uri, signed=True, **params)

    def cross_collateral_repay(self,
                               coin: str,
                               collateralCoin: str,
                               amount: float,
                               recvWindow: int = None) -> dict :
        
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_futures_api_uri('futures/loan/repay')
        return self.request_handler.post(uri, signed=True, **params)

    def cross_collateral_repay_history(self,
                                       coin: str = None,
                                       startTime: Union[int, str] = None,
                                       endTime: Union[int, str] = None,
                                       limit: int = None,
                                       recvWindow: int = None) -> dict :
        
        params = locals()
        del params['self']
        if params['startTime'] is not None:
            params['startTime'] = format_time(params['startTime'])
        if params['endTime'] is not None:
            params['endTime'] = format_time(params['endTime'])
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_futures_api_uri('futures/loan/repay/history')
        return self.request_handler.get(uri, signed=True, **params)

    def cross_collateral_wallet(self,
                                recvWindow: int = None) -> dict :
        
        params = {}
        if recvWindow  is not None:
            params['recvWindow'] = recvWindow
        uri = self._create_futures_api_uri('futures/loan/wallet')
        return self.request_handler.get(uri, signed=True, **params)

    def cross_collateral_info(self,
                              collateralCoin: str = None,
                              recvWindow: int = None) -> dict :

        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_futures_api_uri('futures/loan/configs')
        return self.request_handler.get(uri, signed=True, **params)

    def cross_collateral_ltv_rate(self,
                                  collateralCoin: str,
                                  amount: float,
                                  direction: str,
                                  recvWindow: int = None) -> dict :

        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_futures_api_uri('futures/loan/calcAdjustLevel')
        return self.request_handler.get(uri, signed=True, **params)

    def cross_collateral_ltv_max_amount(self,
                                        collateralCoin: str,
                                        recvWindow: int = None) -> dict :

        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_futures_api_uri('futures/loan/calcMaxAdjustAmount')
        return self.request_handler.get(uri, signed=True, **params)

    def cross_collateral_ltv_adjust(self,
                                    collateralCoin: str,
                                    amount: float,
                                    direction: str,
                                    recvWindow: int = None) -> dict :

        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_futures_api_uri('futures/loan/adjustCollateral')
        return self.request_handler.post(uri, signed=True, **params)

    def cross_collateral_ltv_history(self,
                                     loanCoin: str = None,
                                     collateralCoin: str = None,
                                     startTime: Union[int, str] = None,
                                     endTime: Union[int, str] = None,
                                     limit: int = None,
                                     recvWindow: int = None) -> dict :

        params = locals()
        del params['self']
        if params['startTime'] is not None:
            params['startTime'] = format_time(params['startTime'])
        if params['endTime'] is not None:
            params['endTime'] = format_time(params['endTime'])
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_futures_api_uri('futures/loan/adjustCollateral/history')
        return self.request_handler.get(uri, signed=True, **params)

    def cross_collateral_liquidation_history(self,
                                             loanCoin: str = None,
                                             collateralCoin: str = None,
                                             startTime: Union[int, str] = None,
                                             endTime: Union[int, str] = None,
                                             limit: int = None,
                                             recvWindow: int = None) -> dict :

        params = locals()
        del params['self']
        if params['startTime'] is not None:
            params['startTime'] = format_time(params['startTime'])
        if params['endTime'] is not None:
            params['endTime'] = format_time(params['endTime'])
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_futures_api_uri('futures/loan/liquidationHistory')
        return self.request_handler.get(uri, signed=True, **params)

    def check_collateral_repay_limit(self,
                                     coin: str,
                                     collateralCoin: str,
                                     recvWindow: int = None) -> dict :

        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_futures_api_uri('futures/loan/collateralRepayLimit')
        return self.request_handler.get(uri, signed=True, **params)

    def get_collateral_repay_quote(self,
                                   coin: str,
                                   collateralCoin: str,
                                   amount: float,
                                   recvWindow: int = None) -> dict :

        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_futures_api_uri('futures/loan/collateralRepay')
        return self.request_handler.get(uri, signed=True, **params)

    def repay_with_collateral(self,
                              quoteId: str,
                              recvWindow: int = None) -> dict :

        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_futures_api_uri('futures/loan/collateralRepay')
        return self.request_handler.post(uri, signed=True, **params)

    def collateral_repay_result(self,
                                quoteId: str,
                                recvWindow: int = None) -> dict :

        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_futures_api_uri('futures/loan/collateralRepayResult')
        return self.request_handler.get(uri, signed=True, **params)

    def cross_collateral_interest_history(self,
                                          collateralCoin: str = None,
                                          startTime: Union[int, str] = None,
                                          endTime: Union[int, str] = None,
                                          current: int = None,
                                          limit: int = None,
                                          recvWindow: int = None) -> dict :

        params = locals()
        del params['self']
        if params['startTime'] is not None:
            params['startTime'] = format_time(params['startTime'])
        if params['endTime'] is not None:
            params['endTime'] = format_time(params['endTime'])
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_futures_api_uri('futures/loan/interestHistory')
        return self.request_handler.get(uri, signed=True, **params)


    
