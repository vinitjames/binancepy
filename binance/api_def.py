

BASE_URL = 'https://api{}.binance.{}'


class PublicAPI(object):
    # url definitions

    API_URL = BASE_URL + '/api'

    # public api version
    PUBLIC_API_VERSION = 'v1'

    # Kline/Candelstick interval m -> minutes; h -> hours; d -> days; w -> weeks; M -> months
    KLINE_INTERVAL_1MINUTE = '1m'
    KLINE_INTERVAL_3MINUTE = '3m'
    KLINE_INTERVAL_5MINUTE = '5m'
    KLINE_INTERVAL_15MINUTE = '15m'
    KLINE_INTERVAL_30MINUTE = '30m'
    KLINE_INTERVAL_1HOUR = '1h'
    KLINE_INTERVAL_2HOUR = '2h'
    KLINE_INTERVAL_4HOUR = '4h'
    KLINE_INTERVAL_6HOUR = '6h'
    KLINE_INTERVAL_8HOUR = '8h'
    KLINE_INTERVAL_12HOUR = '12h'
    KLINE_INTERVAL_1DAY = '1d'
    KLINE_INTERVAL_3DAY = '3d'
    KLINE_INTERVAL_1WEEK = '1w'
    KLINE_INTERVAL_1MONTH = '1M'


class AuthenticatedAPI():

    WITHDRAW_API_URL = BASE_URL + '/wapi'
    MARGIN_API_URL = BASE_URL + '/sapi'
    WEBSITE_URL = 'https://www.binance.{}'
    FUTURES_URL = BASE_URL + '/sapi'

    PRIVATE_API_VERSION = 'v3'
    WITHDRAW_API_VERSION = 'v3'
    MARGIN_API_VERSION = 'v1'
    FUTURES_API_VERSION = 'v1'

    # order status enum
    ORDER_STATUS_NEW = 'NEW'
    ORDER_STATUS_PARTIALLY_FILLED = 'PARTIALLY_FILLED'
    ORDER_STATUS_FILLED = 'FILLED'
    ORDER_STATUS_CANCELED = 'CANCELED'
    ORDER_STATUS_PENDING_CANCEL = 'PENDING_CANCEL'
    ORDER_STATUS_REJECTED = 'REJECTED'
    ORDER_STATUS_EXPIRED = 'EXPIRED'

    # order type
    ORDER_TYPE_LIMIT = 'LIMIT'
    ORDER_TYPE_MARKET = 'MARKET'
    ORDER_TYPE_STOP_LOSS = 'LOSS'
    ORDER_TYPE_STOP_LOSS_LIMIT = 'LIMIT'
    ORDER_TYPE_TAKE_PROFIT = 'PROFIT'
    ORDER_TYPE_TAKE_PROFIT_LIMIT = 'PROFIT_LIMIT'
    ORDER_TYPE_LIMIT_MAKER = 'LIMIT_MAKER'

    # order side
    ORDER_SIDE_BUY = 'BUY'
    ORDER_SIDE_SELL = 'SELL'

    # Time in force for order
    TIME_IN_FORCE_GTC = 'GTC'  # Good till cancelled
    TIME_IN_FORCE_IOC = 'IOC'  # Immediate or cancel
    TIME_IN_FORCE_FOK = 'FOK'  # Fill or kill'

    # new order response type
    ORDER_RESPONSE_TYPE_ACK = 'ACK'
    ORDER_RESPONSE_TYPE_RESULT = 'RESULT'
    ORDER_RESPONSE_TYPE_FULL = 'FULL'


# websocket depths
WEBSOCKET_DEPTH_5 = '5'
WEBSOCKET_DEPTH_10 = '10'
WEBSOCKET_DEPTH_20 = '20'

if __name__ == '__main__':
    import ipdb
    ipdb.set_trace()
