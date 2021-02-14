================================
BinancePy  
================================

This is an unofficial Python wrapper for the `Binance exchange REST API v3 <https://github.com/binance/binance-spot-api-docs>`_. I am in no way affiliated with Binance, use at your own risk.

Note
----

																											
Source code
https://github.com/vinitjames/binancepy

Documentation
https://python-binance.readthedocs.io/en/latest/

Binance API Telegram
https://t.me/binance_api_english

Make sure you update often and check the `Changelog <https://python-binance.readthedocs.io/en/latest/changelog.html>`_ for new features and bug fixes.

Features
--------

- Implementation of all General, Market Data and Account endpoints.
- Simple handling of authentication
- No need to generate timestamps yourself, the wrapper does it for you
- Response exception handling
- Websocket handling with reconnection and multiplexed connections
- Symbol Depth Cache
- Historical Kline/Candle fetching function
- Withdraw functionality
- Deposit addresses
- Margin Trading
- Futures Trading
- Support other domains (.us, .jp, etc)
					  
Quick Start
-----------

`Register an account with Binance <https://www.binance.com/register.html?ref=10099792>`_.

`Generate an API Key <https://www.binance.com/userCenter/createApi.html>`_ and assign relevant permissions.

.. code:: bash

pip install binancepy


.. code:: python

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
# do something

from binance.websockets import BinanceSocketManager
bm = BinanceSocketManager(client)
bm.start_aggtrade_socket('BNBBTC', process_message)
bm.start()

# get historical kline data from any date range

# fetch 1 minute klines for the last day up until now
klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

# fetch 30 minute klines for the last month of 2017
klines = client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")

# fetch weekly klines since it listed
klines = client.get_historical_klines("NEOBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")

For more `check out the documentation <https://python-binance.readthedocs.io/en/latest/>`_.
