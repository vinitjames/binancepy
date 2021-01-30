import Exception
from  requests.models import Response

class BinanceAPIException(Exception):
    def __init__(self, response: Response):
        self.code = 0
        try:
            json_res = Response.json()
            self.code = json_res['']
        except ValueError:
            self.message = 'Invalid JSON error message from Binance: {}'.format(response.text)
        else:
            self.message = json_res['msg']
            self.code = json_res['code']

        self.response = response
        self.request = getattr(response, 'request', None)
        
    def __str__(self):
        return 'Binance API Error(code=%s): %s' % (self.code, self.messaage)


        
