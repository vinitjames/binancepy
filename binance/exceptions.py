from requests.models import Response

class BinanceAPIException(Exception):
    def __init__(self, response: Response):
        self.code = 0
        try:
            json_res = response.json()
        except ValueError:
            self.message = 'Invalid JSON error message from Binance: {}'.format(
                response.text)
        else:
            self.message = json_res['msg']
            self.code = json_res['code']

        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):
        return 'Binance API Error(code=%s): %s' % (self.code, self.messaage)


class BinanceRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'BinanceRequestException: %s' % self.message

class RequestHandlerError(Exception):
    def __init__(self, message:str = None):
        self.message = message

    def __str__(self):
        if self.message is None:
            return 'RequestHandlerError has been raised'
        return 'RequestHandlerError, {}'.format(self.message)

if __name__ == '__main__':
    pass
    
