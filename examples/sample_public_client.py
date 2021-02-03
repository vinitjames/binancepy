import sys
sys.path.insert(0, '../')
from binance.public_client import PublicClient

if __name__ == '__main__':
    # creating a public client with default request params
    client = PublicClient()

    
    #getting server time
    print("Binance Server Time: ", client.get_server_time())

    
    # getting exchange inf0
    ex_info = client.get_exchange_info()
    print("exchange info response keys: ", ex_info.keys())

    
    # getting exchange info
    sym_info = client.get_symbol_info(symbol='ETHEUR')
    print("symbol info: ", sym_info )

    
    #getting price_ticker if symbol not included value for all symbols are returned
    price_ticker = client.get_price_ticker(symbol='ETHEUR')
    print("price ticker: ", price_ticker)

    
    #getting orderbook ticker if symbol not included value for all symbols are returned
    orderbook_ticker = client.get_orderbook_ticker(symbol='ETHEUR')
    print("orderbook ticker: ", orderbook_ticker)

    
    """ getting orderbook for a symbol,
        limit param gives the no of entries to be returned default value = 100 
    """
    orderbook = client.get_order_book(symbol='ETHEUR', limit = 10)
    print("orderbook: ", orderbook)

    
    #getting average price, for the specified symbol
    avg_price = client.get_avg_price('ETHEUR')
    print("average price: ", avg_price)

    
    #getting 24hr price ticker, if symbol not included value for all symbols are returned
    _24_hr_ticker = client.get_24hr_ticker('ETHEUR')
    print("24 hr ticker: ", _24_hr_ticker)

    
    ''' getting recent trades for a symbol, limit is for number of last n trades
        Default limit value = 100
    '''
    recent_trades = client.get_recent_trades('ETHEUR', limit=5)
    print("recent trades: ", recent_trades)

    
    ''' getting aggregate trades for a symbol, limit is for number of last n trades
        startTime: time in milliseconds for the start time of the trades 
        endTime: time in milliseconds for the end time  of trades
        If startTime and endTime are sent, time between startTime and endTime 
        must be less than 1 hour.
        If fromId, startTime, and endTime are not sent, the most recent aggregate 
        trades will be returned.
        Default limit value of no of aggregate trades= 500
    '''
    import time 
    agg_trades = client.get_agg_trades(symbol='ETHEUR',
                                       startTime = round(time.time()*1000) - 1000000,
                                       endTime = round(time.time()*1000),
                                       limit=5)
    print("agg trades: ", agg_trades)


    ''' getting klines/candelstick for a symbol, 
        interval: is enum(1m, 1h, 2h ....) see api_def for more info
        startTime: time in milliseconds for the start time of the trades 
        endTime: time in milliseconds for the end time  of trades
        If startTime, and endTime are not sent, the most recent klines are returned.
        Default limit value = 500
    '''
    klines = client.get_klines(symbol = 'ETHEUR',
                               interval = client.KLINE_INTERVAL_1HOUR,
                               startTime = round(time.time()*1000) - 100000000,
                               endTime = round(time.time()*1000),
                               limit=5)
    print("klines: ", klines)
