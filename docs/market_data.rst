Market Data Endpoints
=====================

`Create a client to access market data`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For accesing market data both PublicClient or AuthenticatedClient can be used but since AuthenticatedClient requires an API Key and API Secret, it is simmpler to use PublicClient when only market data is needed.


.. code:: python
		  
		  from binance.client import PublicClient
		  client = PublicClient()

`Test Connectivity <https://binance-docs.github.io/apidocs/spot/en/#test-connectivity>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

		  client.ping()
		  
`Get Server Time <https://binance-docs.github.io/apidocs/spot/en/#check-server-time>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

		 server_time =  client.get_server_time()
		  
`Get Exchange Information <https://binance-docs.github.io/apidocs/spot/en/#exchange-information>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

		  exchange_info = client.get_exchange_info()

Get Symbol Information
^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

		  symbol_info = client.get_symbol_info()


`Get Order Book <https://binance-docs.github.io/apidocs/spot/en/#order-book>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    order_book = client.get_order_book(symbol='BNBBTC', limit=100)

	
`Get Recent Trades <https://binance-docs.github.io/apidocs/spot/en/#recent-trades-list>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    recent_trades = client.get_recent_trades(symbol='BNBBTC', limit=100)


`Get Aggregate Trades <https://binance-docs.github.io/apidocs/spot/en/#compressed-aggregate-trades-list>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

	   trades = client.get_agg_trades(symbol='BNBBTC',
	                                  formId=26129,
                                      startTime=1500541200,
                                      endTime=1500541250,
                                      limit=100)



`Get Kline/Candlesticks <binance.html#binance.client.Client.get_klines>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

	candles = client.get_klines(symbol='BNBBTC', interval=Client.KLINE_INTERVAL_30MINUTE)

`Get Historical Kline/Candlesticks <binance.html#binance.client.Client.get_historical_klines>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fetch klines for any date range and interval

.. code:: python
																																				  
   # fetch 1 minute klines for the last day up until now
   klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

   # fetch 30 minute klines for the last month of 2017
   klines = client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")

   # fetch weekly klines since it listed
   klines = client.get_historical_klines("NEOBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")




`Get Current average price for a symbol <https://binance-docs.github.io/apidocs/spot/en/#current-average-price>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

	avg_price = client.get_avg_price(symbol='BNBBTC')

`Get 24hr Ticker price change statistics <https://binance-docs.github.io/apidocs/spot/en/#24hr-ticker-price-change-statistics>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

	tickers = client.get_24hr_ticker(symbol='BNBBTC')


`Get Symbol Ticker <https://binance-docs.github.io/apidocs/spot/en/#symbol-price-ticker>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

	tickers = client.get_price_ticker(symbol='BNBBTC')
	

`Get Orderbook Tickers <https://binance-docs.github.io/apidocs/spot/en/#symbol-order-book-ticker>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

       tickers = client.get_orderbook_ticker(symbol='BNBBTC')
