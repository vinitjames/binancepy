

BASE_URL = 'https://api{}.binance.{}'


class ApiVersion(object):
    PUBLIC   = 'v1'
    PRIVATE  = 'v3'
    WITHDRAW = 'v3'
    MARGIN   = 'v1'
    FUTURES  = 'v1'

class ApiUrl(object):
    DEFAULT  = BASE_URL + '/api'
    WITHDRAW = BASE_URL + '/wapi'
    MARGIN   = BASE_URL + '/sapi'
    WEBSITE  = 'https://www.binance.{}'
    FUTURES  = BASE_URL + '/sapi'
     
class KlineInterval(object):
    ONEMINUTE     = '1m'
    THREEMINUTE   = '3m'
    FIVEMINUTE    = '5m'
    FIFTEENMINUTE = '15m'
    THIRTYMINUTE  = '30m'
    ONEHOUR       = '1h'
    TWOHOUR       = '2h'
    FOURHOUR      = '4h'
    SIXHOUR       = '6h'
    EIGHTHOUR     = '8h'
    TWELVEHOUR    = '12h'
    ONEDAY        = '1d'
    THREEDAY      = '3d'
    ONEWEEK       = '1w'
    ONEMONTH      = '1M'
    
class OrderStatus(object):
    NEW              = 'NEW'
    PARTIALLY_FILLED = 'PARTIALLY_FILLED'
    FILLED           = 'FILLED'
    CANCELED         = 'CANCELED'
    PENDING_CANCEL   = 'PENDING_CANCEL'
    REJECTED         = 'REJECTED'
    EXPIRED          = 'EXPIRED'

class OrderType(object):
    LIMIT             = 'LIMIT'
    MARKET            = 'MARKET'
    STOP_LOSS         = 'STOP_LOSS'
    STOP_LOSS_LIMIT   = 'STOP_LOSS_LIMIT'
    TAKE_PROFIT       = 'TAKE_PROFIT'
    TAKE_PROFIT_LIMIT = 'TAKE_PROFIT_LIMIT'
    LIMIT_MAKER       = 'LIMIT_MAKER'

class OrderSide(object):
    BUY  = 'BUY'
    SELL = 'SELL'

class TimeInForce(object):
    GTC = 'GTC'  # Good till cancelled
    IOC = 'IOC'  # Immediate or cancel
    FOK = 'FOK'  # Fill or kill'

class OrderResponseType(Object):
    ACK    = 'ACK'
    RESULT = 'RESULT'
    FULL   = 'FULL'
    
    
# websocket depths
WEBSOCKET_DEPTH_5 = '5'
WEBSOCKET_DEPTH_10 = '10'
WEBSOCKET_DEPTH_20 = '20'

if __name__ == '__main__':
    pass
