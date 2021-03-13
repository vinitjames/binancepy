from abc import ABCMeta, abstractmethod
from typing import Union
from binance.utils import format_time, interval_to_ms
import time


class MarketDataEndpoints(metaclass = ABCMeta):

    @property
    @abstractmethod
    def request_handler(self):
        pass

    @property
    @abstractmethod
    def KLINE_INTERVAL(self):
        pass
    
    @abstractmethod
    def _create_api_uri(self, path: str, version: str) -> str:
        pass
        
    def ping(self) -> dict:
        uri = self._create_api_uri('ping')
        return self.request_handler.get(uri)

    def get_server_time(self) -> dict:
        uri = self._create_api_uri('time')
        return self.request_handler.get(uri)

    def get_exchange_info(self) -> dict:
        uri = self._create_api_uri('exchangeInfo')
        return self.request_handler.get(uri)

    def get_symbol_info(self, symbol: str) -> dict:
        resp_data = self.get_exchange_info()
        for sym_data in resp_data['symbols']:
            if(sym_data['symbol'] == symbol.upper()):
                return sym_data
        return None

    def get_price_ticker(self, symbol: str = None) -> dict:
        uri = self._create_api_uri('ticker/price')
        if(symbol == None):
            return self.request_handler.get(uri)
        return self.request_handler.get(uri, symbol=symbol)

    def get_orderbook_ticker(self, symbol: str = None) -> dict:
        uri = self._create_api_uri('ticker/bookTicker')
        if(symbol is None):
            return self.request_handler.get(uri)
        return self.request_handler.get(uri, symbol=symbol)

    def get_order_book(self, symbol: str, limit: int = 100):
        uri = self._create_api_uri('depth')
        return self.request_handler.get(uri, symbol=symbol, limit=limit)

    def get_avg_price(self, symbol: str) -> dict:
        #avg price does not work with v1
        uri = self._create_api_uri('avgPrice', version='v3')
        return self.request_handler.get(uri, symbol=symbol)

    def get_24hr_ticker(self, symbol: str = None) -> dict:
        uri = self._create_api_uri('ticker/24hr')
        if(symbol == None):
            return self.request_handler.get(uri)
        return self.request_handler.get(uri, symbol=symbol)
    
    def get_recent_trades(self, symbol: str, limit: int = 100) -> dict:
        uri = self._create_api_uri('trades')
        return self.request_handler.get(uri, symbol=symbol, limit=limit)

    def get_agg_trades(self, symbol: str,
                       formId: int = None,
                       startTime: int = None,
                       endTime: int = None,
                       limit: int = 500):
        params = locals()
        del params['self']
        if(params['startTime'] is not None):
            params['startTime'] = format_time(params['startTime'])
        if(params['endTime'] is not None):
            params['endTime'] = format_time(params['endTime'])
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_api_uri('aggTrades')
        return self.request_handler.get(uri, **params)

    def get_klines(self,
                   symbol: str,
                   interval: str,
                   startTime: Union[int, str] = None,
                   endTime: Union[int, str] = None,
                   limit: int = None) -> dict:
        
        params = locals()
        del params['self']
        if(params['startTime'] is not None):
            params['startTime'] = format_time(params['startTime'])
        if(params['endTime'] is not None):
            params['endTime'] = format_time(params['endTime'])
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_api_uri('klines')
        return self.request_handler.get(uri, **params)

    def _get_earliest_valid_timestamp(self, symbol: str, interval: str):
                
        kline = self.get_klines(
            symbol=symbol,
            interval=interval,
            limit=1,
            startTime=0,
            endTime=None)
        return kline[0][0]

    def get_historical_klines(self,
                              symbol: str,
                              interval: str,
                              startTime: Union[int, str],
                              endTime: Union[int, str] = None) -> dict:
        params = locals()
        del params['self']
        earliest_timestamp = self._get_earliest_valid_timestamp(symbol,
                                                                interval)
        
        params['startTime'] = format_time(params['startTime'])
        params['startTime'] = max(earliest_timestamp, params[
            'startTime'])
        if(params['endTime'] is not None):
            params['endTime'] = format_time(params['endTime'])
        if(params['endTime'] is not None) and (params['startTime'] > params['endTime']):
            raise ValueError('startTime entered is greater than endTime')
        params = {k: v for k, v in params.items() if v is not None}
        params['limit'] = 500
        data = []
        api_call_count = 0
        while(True):
            fetched_data = self.get_klines(**params)
            api_call_count+=1
            data.extend(fetched_data)
            if(len(fetched_data) < params['limit']):
                break
            params['startTime'] = fetched_data[-1][0] + interval_to_ms(interval)
            if (api_call_count) == 3:
                time.sleep(0.5)
                api_call_count = 0
        return data
