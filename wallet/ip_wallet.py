import os

from pybit import inverse_perpetual
import logging

import config


class InversePerpetualWallet:

    ENDPOINT = 'https://api-testnet.bybit.com'

    def __init__(self, sub_acct: int = None):
        """Constructor"""

        if sub_acct:
            self.BYBIT_API_KEY = os.environ[f'SUB_{sub_acct}_BYBIT_API_KEY']
            self.BYBIT_API_SECRET = os.environ[f'SUB_{sub_acct}_BYBIT_API_SECRET']
        else:
            self.BYBIT_API_KEY = os.environ['BYBIT_API_KEY']
            self.BYBIT_API_SECRET = os.environ['BYBIT_API_SECRET']

        self.session = inverse_perpetual.HTTP(
            endpoint=self.ENDPOINT,
            api_key=self.BYBIT_API_KEY,
            api_secret=self.BYBIT_API_SECRET,
        )

    def submit_order(self, order):
        # try:
        o = {k: v for k, v in order.items() if k in config.BYBIT_SPOT_ORDER_FIELDS}

        logging.info('Submitting Following Order to ByBit: ')
        logging.info()
        response = self.session.place_active_order(o)
        logging.info(response)
        logging.info('  * ORDER PLACED *')
        logging.info('')
        return response
        # except Exception as e:
        #     logging.error(e)

    def get_available_balance(self, symbol):
        response = self.session.get_wallet_balance()
        available_bal = response['result'][symbol]['available_balance']
        logging.info(f"{symbol} Balance: {available_bal}")
        return available_bal
