
class Wallet(object):

    def __init__(self,
                 request_handler,

                 ):
        pass

    def _create_withdraw_api_uri(self, path: str):
        return self.WITHDRAW_API__URL + '/' + self.WITHDRAW_API_VERSION + '/' + path

    def get_system_starus(self) -> dict:
        uri = self._create_withdraw_api_uri('systemStatus.html')
        return self.request_handler.get(uri, **params)
        
    def get_all_coin_info(self,
                          recvWindow: int = None)  -> dict:

        params = locals()
        del params['self']
        uri = self._create_withdraw_api_uri('capital/config/getall')
        return self.request_handler.get(uri, **params)    

    def get_daily_account_snapshot(self,
                                   type:str,
                                   startTime: int = None,
                                   endTime: int = None,
                                   limit: int = 5,
                                   recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k : v for k, v in params.items() if v is not None}
        uri = self._create_withdraw_api_uri('accountSnapshot')
        return self.request_handler.get(uri, signed=True, **params)

    def disable_fast_withdraw_switch(self,
                                     recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k : v for k, v in params.items() if v is not None}
        uri = self._create_withdraw_api_uri('account/disableFastWithdrawSwitch')
        return self.request_handler.post(uri, signed=True, **params)

    def enable_fast_withdraw_switch(self,
                                    recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k : v for k, v in params.items() if v is not None}
        uri = self._create_withdraw_api_uri('account/enableFastWithdrawSwitch')
        return self.request_handler.post(uri, signed=True, **params)

    def widthdraw(self,
                  coin: str,
                  address: str,
                  amount: float,
                  transactionFeeFlag: bool = None,
                  withdrawOrderId: str = None,
                  network: str = None,
                  addressTag: str = None,
                  name: str = None,
                  recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k : v for k, v in params.items() if v is not None}
        uri = self._create_withdraw_api_uri('withdraw.html')
        return self.request_handler.post(uri, signed=True, **params)


    def get_deposit_history(self,
                            asset: str = None,
                            status: int = None,
                            startTime: int = None,
                            endTime: int = None,
                            recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k : v for k, v in params.items() if v is not None}
        uri = self._create_withdraw_api_uri('depositHistory.html')
        return self.request_handler.get(uri, signed=True, **params)

    def get_withdraw_history(self,
                            asset: str = None,
                            status: int = None,
                            startTime: int = None,
                            endTime: int = None,
                            recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k : v for k, v in params.items() if v is not None}
        uri = self._create_withdraw_api_uri('withdrawHistory.html')
        return self.request_handler.get(uri, signed=True, **params)

    def get_deposit_address(self,
                            asset: str = None,
                            status: bool = None,
                            recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k : v for k, v in params.items() if v is not None}
        uri = self._create_withdraw_api_uri('depositAddress.html')
        return self.request_handler.get(uri, signed=True, **params)

    def get_account_status(self,
                           recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k : v for k, v in params.items() if v is not None}
        uri = self._create_withdraw_api_uri('accountStatus.html')
        return self.request_handler.get(uri, signed=True, **params)

    def get_account_API_trading_status(self,
                                       recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k : v for k, v in params.items() if v is not None}
        uri = self._create_withdraw_api_uri('apiStatus.html')
        return self.request_handler.get(uri, signed=True, **params)


    def get_dust_log(self,
                     recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k : v for k, v in params.items() if v is not None}
        uri = self._create_withdraw_api_uri('userAssetDribbleLog.html')
        return self.request_handler.get(uri, signed=True, **params)


    def dust_transfer(self,
                      asset:str,
                      recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k : v for k, v in params.items() if v is not None}
        uri = self._create_withdraw_api_uri('asset/dust')
        return self.request_handler.post(uri, signed=True, **params)

    def get_asset_dividend_record(self,
                                  asset: str = None,
                                  status: int = None,
                                  startTime: int = None,
                                  endTime: int = None,
                                  limit: int = None,
                                  recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k : v for k, v in params.items() if v is not None}
        uri = self._create_withdraw_api_uri('asset/assetDividend')
        return self.request_handler.get(uri, signed=True, **params)

    def get_asset_detail(self,
                         recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k : v for k, v in params.items() if v is not None}
        uri = self._create_withdraw_api_uri('assetDetail.html')
        return self.request_handler.get(uri, signed=True, **params)

    def get_trade_fee(self,
                      symbol: str = None,
                      recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k : v for k, v in params.items() if v is not None}
        uri = self._create_withdraw_api_uri('tradeFee.html')
        return self.request_handler.get(uri, signed=True, **params)


    def user_universal_transfer(self,
                                type : str,
                                asset: str,
                                amount: str,
                                recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k : v for k, v in params.items() if v is not None}
        uri = self._create_withdraw_api_uri('asset/transfer')
        return self.request_handler.post(uri, signed=True, **params)


    def get_user_universal_transfer_history(self,
                                            type: str,
                                            startTime: int = None,
                                            endTime: int = None,
                                            current: int = 1,
                                            size: int = 10,
                                            recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k : v for k, v in params.items() if v is not None}
        uri = self._create_withdraw_api_uri('asset/transfer')
        return self.request_handler.get(uri, signed=True, **params)