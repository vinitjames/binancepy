import sys
from binance.client import AuthenticatedClient
from secret import API_KEY, API_SECRET

if __name__ == '__main__':
    # creating a public client with default request params
    client = AuthenticatedClient(API_KEY, API_SECRET)
    print(client.get_server_time())
    
    #querying margin asset info 
    print(client.query_margin_asset('ETH'))

    
