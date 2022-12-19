import os

from pybit import usdt_perpetual
import logging

import config

import alert_handler


class USDTPerpetualWallet:

    ENDPOINT = 'https://api-testnet.bybit.com'

    def __init__(self, sub_acct: int = None):
        """Constructor"""

        if sub_acct:
            self.BYBIT_API_KEY = os.environ[f'SUB_{sub_acct}_BYBIT_API_KEY']
            self.BYBIT_API_SECRET = os.environ[f'SUB_{sub_acct}_BYBIT_API_SECRET']
        else:
            self.BYBIT_API_KEY = os.environ['BYBIT_API_KEY']
            self.BYBIT_API_SECRET = os.environ['BYBIT_API_SECRET']

        self.session = usdt_perpetual.HTTP(
            endpoint=self.ENDPOINT,
            api_key=self.BYBIT_API_KEY,
            api_secret=self.BYBIT_API_SECRET,
        )

    def submit_order(self, order):
        # try:

        order['price'] = float(order['price'])
        order['reduce_only'] = config.BYBIT_USDT_PERP_REDUCE_ONLY
        order['close_on_trigger'] = config.BYBIT_USDT_PERP_CLOSE_ON_TRIGGER
        order['time_in_force'] = config.BYBIT_USDT_PERP_TIME_IN_FORCE
        order['take_profit'] = round(order['price'] + (order['price'] * config.BYBIT_USDT_PERP_TAKE_PROFIT_PERCENTAGE), 5)
        order['stop_loss'] = config.BYBIT_USDT_PERP_STOP_LOSS
        order['category'] = config.BYBIT_USDT_PERP_CATEGORY
        order['symbol'] = config.BYBIT_SYMBOL
        order['side'] = order['side'].title()

        o = {k: v for k, v in order.items() if k in config.BYBIT_USDT_PERP_ORDER_FIELDS}

        logging.info('Submitting Following Order to ByBit: ')
        logging.info(o)
        response = self.session.place_active_order(**o)
        order['response'] = response['result']
        alert_handler.send_alert(order)
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
