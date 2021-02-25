================================
BinancePy  
================================
.. image:: https://img.shields.io/github/license/vinitjames/binancepy
    :target:  https://github.com/vinitjames/binancepy/blob/master/LICENSE

|
This is an unofficial Python wrapper for the `Binance exchange REST API v3 <https://github.com/binance/binance-spot-api-docs>`_.



Source code
https://github.com/vinitjames/binancepy

Documentation
https://python-binance.readthedocs.io/en/latest/

Binance API Telegram
https://t.me/binance_api_english

Make sure you update often and check the `Changelog <https://python-binance.readthedocs.io/en/latest/changelog.html>`_ for new features and bug fixes.

Features
--------
  
- Implementation of  Market Data, Trading and Wallet endpoints
- Market Data Endpoints accesible without binance api key
- No need to generate timestamps yourself, the wrapper does it for you
- Response exception handling
- Historical Kline/Candle fetching function
- Simple handling of authentication
- Spot Trading
- Margin Trading
- Futures Trading
- Wallet Info and Transfer functionality 
- Support other domains (.us, .jp, etc)
					  
Quick Start
-----------

To install as Python package run 

.. code-block:: bash

	pip install binancepy

Or clone the repo with git and install with version you want

.. code-block:: bash
				
	git clone -b 'branch name' https://github.com/vinitjames/binancepy.git
	cd binancepy
	pip install .

To run  the sample public client which does not require api keys run the command below:-

.. code-block:: bash
				
	python examples/sample_public_client.py

Fetching Market Data
--------------------

To fetch market data which uses binance market data endpoints api key is not required. All functionalities of PublicClient be used without an API key

.. code-block:: python

    from binance.client import PublicClient
   
    client = PublicClient()

	# creating a public client with default request params
    client = PublicClient()

    
    #getting server time
    result = client.get_server_time()

    
    # getting exchange info
    ex_info = client.get_exchange_info()


    # getting exchange info
    sym_info = client.get_symbol_info(symbol='ETHEUR')

    
    #getting price_ticker if symbol not included value for all symbols are returned
    price_ticker = client.get_price_ticker(symbol='ETHEUR')


    #getting orderbook ticker if symbol not included value for all symbols are returned
    orderbook_ticker = client.get_orderbook_ticker(symbol='ETHEUR')
    

    
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
                               interval = client.KLINE_INTERVAL.ONEDAY,
                               startTime = round(time.time()*1000) - 100000000,
                               endTime = round(time.time()*1000),
                               limit=5)
    


    ''' getting historical klines/candelstick for a symbol, 
        interval: is enum(1m, 1h, 2h ....) see api_def for more info
        startTime: time in milliseconds for the start time of the trades 
        endTime: time in milliseconds for the end time  of trades
        If startTime, and endTime are not sent, the most recent klines are returned.
        Default limit value = 500
    '''
    
    klines = client.get_historical_klines(symbol = 'ETHUSDT',
                               interval = client.KLINE_INTERVAL.ONEDAY,
                               startTime = '2/12/2018',
                               endTime = '12/12/2019')



`Register an account with Binance <https://www.binance.com/register.html?ref=10099792>`_.

`Generate an API Key <https://www.binance.com/userCenter/createApi.html>`_ and assign relevant permissions.

.. code-block:: python

    from binance.client import Client
   
    client = Client(api_key, api_secret)

    # get market depth
    depth = client.get_order_book(symbol='BNBBTC')
   
   # place a test market buy order, to place an actual order use the create_order function
   order = client.create_test_order(
				symbol='BNBBTC',
				side=Client.SIDE_BUY,
				type=Client.ORDER_TYPE_MARKET,
				quantity=100)

   # get all symbol prices
   prices = client.get_all_tickers()

   # withdraw 100 ETH
   # check docs for assumptions around withdrawals
   from binance.exceptions import BinanceAPIException, BinanceWithdrawException

   try:
     result = client.withdraw(
				asset='ETH',
				address='<eth_address>',
				amount=100)
	 except BinanceAPIException as e:
			print(e)
			
	 except BinanceWithdrawException as e:
            print(e)
	 else:
		print("Success")

	 # fetch list of withdrawals
	 withdraws = client.get_withdraw_history()

	 # fetch list of ETH withdrawals
	 eth_withdraws = client.get_withdraw_history(asset='ETH')

	 # get a deposit address for BTC
	 address = client.get_deposit_address(asset='BTC')

	 # start aggregated trade websocket for BNBBTC
	 def process_message(msg):
	     print("message type: {}".format(msg['e']))
		 print(msg)
		 

	# get historical kline data from any date range

	# fetch 1 minute klines for the last day up until now
	klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

	# fetch 30 minute klines for the last month of 2017
	klines = client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")

	# fetch weekly klines since it listed
	klines = client.get_historical_klines("NEOBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")

For more `check out the documentation <https://python-binance.readthedocs.io/en/latest/>`_.
