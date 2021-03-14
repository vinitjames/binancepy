from requests.models import Response


class BinanceAPIError(Exception):
    def __init__(self, response: Response):
        self.code = 0
        try:
            json_res = response.json()
        except ValueError:
            self.message = 'Invalid JSON error message from Binance: {}'.format(response.text)
        else:
            self.message = json_res['msg']
            self.code = json_res['code']
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):
        return 'Binance API Error(code={}): {}'.format(self.code, self.messaage)

    
class BinanceResponseError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'BinanceResponseError: {}'.format(self.message)

    
class RequestHandlerError(Exception):

    def __init__(self, message:str = None):
        self.message = message

    def __str__(self):
        if self.message is None:
            return 'RequestHandlerError has been raised'
        return 'RequestHandlerError, {}'.format(self.message)

    
class SpotTradingError(Exception):

    def __init__(self, message:str = None):
        self.message = message

    def __str__(self):
        if self.message is None:
            return 'SpotTradingError has been raised'
        return 'SpotTradingError, {}'.format(self.message)

    
class MarginTradingError(Exception):

    def __init__(self, message:str = None):
        self.message = message

    def __str__(self):
        if self.message is None:
            return 'MarginTradingError has been raised'
        return 'MarginTradingError, {}'.format(self.message)

    
class FuturesTradingError(Exception):

    def __init__(self, message:str = None):
        self.message = message

    def __str__(self):
        if self.message is None:
            return 'FuturesTradingError has been raised'
        return 'FuturesTradingError, {}'.format(self.message)

    
class WalletError(Exception):

    def __init__(self, message:str = None):
        self.message = message

    def __str__(self):
        if self.message is None:
            return 'WalletError has been raised'
        return 'WalletError, {}'.format(self.message)

    
if __name__ == '__main__':
    pass
    
