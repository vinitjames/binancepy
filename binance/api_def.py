

BASE_URL = 'https://api{}.binance.{}'


class ApiVersion(object):
    PUBLIC   = 'v1'
    PRIVATE  = 'v3'
    WITHDRAW = 'v3'
    MARGIN   = 'v1'
    FUTURES  = 'v1'
    WALLET1  = 'v1'
    WALLET2  = 'v3'

class ApiUrl(object):
    def __init__(self, endpoint_version = '', tld = 'com'):
        self._tld = tld
        self._base_url = BASE_URL.format(endpoint_version, tld)        
        self.DEFAULT  = self._base_url + '/api'
        self.WITHDRAW = self._base_url + '/wapi'
        self.MARGIN   = self._base_url + '/sapi'
        self.WEBSITE  = 'https://www.binance.{}'.format(self._tld)
        self.FUTURES  = self._base_url + '/sapi'
        self.WALLET1 = self._base_url + '/sapi'
        self.WALLET2 = self._base_url + '/wapi'
        
     
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
    
class SideEffectType(object):
    NO_SIDE_EFFECT = 'NO_SIDE_EFFECT'
    MARGIN_BUY     = 'MARGIN_BUY'
    AUTO_REPAY     = 'AUTO_REPAY'
    NO_SIDE_EFFECT = 'NO_SIDE_EFFECT'
    
class TimeInForce(object):
    GTC = 'GTC'  # Good till cancelled
    IOC = 'IOC'  # Immediate or cancel
    FOK = 'FOK'  # Fill or kill'

class OrderResponseType(object):
    ACK    = 'ACK'
    RESULT = 'RESULT'
    FULL   = 'FULL'

class MarginTransferType(object):
    MAIN_C2C        = 'MAIN_C2C'
    MAIN_UMFUTURE   = 'MAIN_UMFUTURE'
    MAIN_CMFUTURE   = 'MAIN_CMFUTURE'
    MAIN_MARGIN     = 'MAIN_MARGIN' 
    MAIN_MINING     = 'MAIN_MINING' 
    C2C_MAIN        = 'C2C_MAIN'   
    C2C_UMFUTURE    = 'C2C_UMFUTURE' 
    C2C_MINING      = 'C2C_MINING' 
    C2C_MARGIN      = 'C2C_MARGIN'
    UMFUTURE_MAIN   = 'UMFUTURE_MAIN'
    UMFUTURE_C2C    = 'UMFUTURE_C2C'
    UMFUTURE_MARGIN = 'UMFUTURE_MARGIN'
    CMFUTURE_MAIN   = 'CMFUTURE_MAIN'
    CMFUTURE_MARGIN = 'CMFUTURE_MARGIN'
    MARGIN_MAIN     = 'MARGIN_MAIN'
    MARGIN_UMFUTURE = 'MARGIN_UMFUTURE'
    MARGIN_CMFUTURE = 'MARGIN_CMFUTURE' 
    MARGIN_MINING   = 'MARGIN_MINING'
    MARGIN_C2C      = 'MARGIN_C2C'
    MINING_MAIN     = 'MINING_MAIN' 
    MINING_UMFUTURE = 'MINING_UMFUTURE'
    MINING_C2C      = 'MINING_C2C'
    MINING_MARGIN   = 'MINING_MARGIN'

class FuturesTransferType(object):
    SPOT_TO_USDT = 1
    USDT_TO_SPOT = 2
    SPOT_TO_COIN = 3
    COIN_TO_SPOT = 4

class DepositHistoryStatus(object):
    PENDING  = 0
    SUCCESS  = 1   
    CREDITED_NONWITHDRAW = 6
    
class WithrawHistoryStatus(object):
    EMAIL_SENT        = 0
    CANCELLED         = 1
    AWAITING_APPROVAL = 2
    REJECTED          = 3
    PROCESSING        = 4
    FAILURE           = 5
    COMPLETED         = 6
    
class WalletType(object):
    SPOT    = 'SPOT'
    MARGIN  = 'MARGIN'
    FUTURES = 'FUTURES'
    
# websocket depths
WEBSOCKET_DEPTH_5 = '5'
WEBSOCKET_DEPTH_10 = '10'
WEBSOCKET_DEPTH_20 = '20'

if __name__ == '__main__':
    pass
