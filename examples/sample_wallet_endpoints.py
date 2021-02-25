import sys
from binance.client import AuthenticatedClient
from secret import API_KEY, API_SECRET

if __name__ == '__main__':
    # creating a public client with default request params
    client = AuthenticatedClient(API_KEY, API_SECRET)
    print(client.get_server_time())
    
            
    #checking wallet system status 
    print(client.get_system_status())

    #checking wallet all coin info 
    print(client.get_all_coin_info())

    #checking wallet account snapshot for current day
    print(client.get_daily_account_snapshot(type = "SPOT",
                                            limit = 1))
    
    #checking wallet account disable fast withdraw switch
    #print(client.disable_fast_withdraw_switch())

    #checking wallet account disable fast withdraw switch
    #print(client.enable_fast_withdraw_switch())
    
    #get wallet withdraw history for all coins 
    print(client.get_withdraw_history(coin='ETH',
                                      status=client.DEPOSIT_HISTORY_STATUS.SUCCESS,
                                      startTime='1.1.2021' ,
                                      endTime='22.2.2021'))

    #get wallet deposit history for all coins
    print(client.get_deposit_history(coin='BTC',
                                     status=client.WITHDRAW_HISTORY_STATUS.COMPLETED,
                                     startTime='1.1.2021',
                                     endTime='1.1.2021'))

    #get account status
    print(client.get_account_status())

    #get deposit address
    print(client.get_deposit_address(coin='BTC'))

    #get account API trading status
    print(client.get_account_API_trading_status())

    #get dust log

    print(client.get_dust_log())

    #get asset details for all assets
    print(client.get_asset_detail())

    #get asset dividend record
    print(client.get_asset_dividend_record(asset = 'ETH',
                                           startTime = '1.1.2021',
                                           endTime = '2.2.2021'))

    #get trade fee
    print(client.get_trade_fee(symbol = 'ETHEUR'))
