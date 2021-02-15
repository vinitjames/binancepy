import sys
from binance.client import AuthenticatedClient
from secret import API_KEY, API_SECRET

if __name__ == '__main__':
    # creating a public client with default request params
    client = AuthenticatedClient(API_KEY, API_SECRET)
    print(client.get_server_time())
    print(client.get_account_info())
    print(client.get_open_orders())
    print(client.get_all_orders('ETHEUR'))
    print(client.get_trade_list('ETHEUR'))
    
    #print(client.query_trade_list('BTCEUR'))
    #print(client.market_buy_order('BTCEUR',quoteOrderQty = 100))
    
