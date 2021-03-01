==============

Installation
------------

``binancepy`` is available on `PYPI <https://pypi.python.org/pypi/binacepy/>`_.
Install with ``pip``:

.. code:: bash

   pip install python-binance



Generating an API KEY
-------------------
Authenticated client should be used for trading(spot/margin/futures) and wallet endpoints. A binance API key is required for this.
For this firstly `register an account with Binance <https://www.binance.com/register.html?ref=10099792>`_.

Then `create an API Key  <https://www.binance.com/userCenter/createApi.html>`_.

Initialising the client
-----------------------

Market data can be accessed using market data endpoints even without an API key. For this use a PublicClient

.. code:: python

   from binance.client import PublicClient
   client = PublicClient()
   
All endpoints/funtionalities are accessible using an AuthenticatedClient. For this use api_key and api_secret which can be generated using the info in the previous section 

.. code:: python

   from binance.client import AuthenticatedClient
   client = AuthenticatedClient(api_key, api_secret)

Making API Calls
----------------

Every method supports the parameters as specified in the`Binance API documentation <https://github.com/binance-exchange/binance-official-api-docs>`_.
These arguments will be sent directly to the relevant endpoint. The Binance API documentation references a `timestamp` parameter, this is generated for you where required.

Each API method returns a dictionary of the JSON response as per the `Binance API documentation <https://github.com/binance-exchange/binance-official-api-docs>`_.
The docstring of each method in the code references the endpoint it implements.
								

Some methods have a `recvWindow` parameter for `timing security, see Binance documentation <https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#timing-security>`_.

All enums for functions parametrs are already specified and can be used directly or strings can be passed for enums as specified in the api docs.
Python bools are accepted instead of strings for arguments which require 'TRUE/True/true' and 'FALSE/False/false' as per the api documentation. 

API Endpoints are rate limited by Binance at 20 requests per second, ask them if you require more.

API Rate Limit
--------------

Check the `get_exchange_info() <binance.html#binance.client.Client.get_exchange_info>`_ call for up to date rate limits.

At the current time Binance rate limits are:

- 1200 requests per minute
- 10 orders per second
- 100,000 orders per 24hrs

Some calls have a higher weight than others especially if a call returns information about all symbols.
Read the `official Binance documentation <https://github.com/binance-exchange/binance-official-api-docs`_ for specific information.


Requests Settings
-----------------

`python-binance` uses the `requests <http://docs.python-requests.org/en/master/>`_ library.

You can set custom requests parameters for all API calls when creating the client.

.. code:: python

    # this would result in verify: False and timeout: 5 for the get_all_orders call
	
	# For Public Client
    client = PublicClient(request_params = {"verify": False, "timeout": 20})

	# For Authenticated Client
	client = AuthenticatedClient("api-key", "api-secret", request_params = {"verify": False, "timeout": 20})
   

Check out the `requests documentation <http://docs.python-requests.org/en/master/>`_ for all options.

**Proxy Settings**

You can use the Requests Settings method above

.. code:: python
		  
		  proxies = {
		  'http': 'http://10.10.1.10:3128',
		  'https': 'http://10.10.1.10:1080'
		  }

		  # in the PublicClient instantiation
		  client = PublicClient(request_params={'proxies': proxies})

		  # in the AuthenticatedClient instantiation
		  client = AuthenticatedClient(api_key, api_secret, request_params={'proxies': proxies})

		  
Or set an environment variable for your proxy if required to work across all requests.

An example for Linux environments from the `requests Proxies documentation <http://docs.python-requests.org/en/master/user/advanced/#proxies>`_ is as follows.

.. code-block:: bash

   $ export HTTP_PROXY="http://10.10.1.10:3128"
   $ export HTTPS_PROXY="http://10.10.1.10:1080"

For Windows environments

.. code-block:: bash

   C:\>set HTTP_PROXY=http://10.10.1.10:3128
   C:\>set HTTPS_PROXY=http://10.10.1.10:1080
