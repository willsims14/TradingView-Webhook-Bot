import os

# from pybit import inverse_perpetual
# from pybit import usdt_perpetual
from pybit import spot
import logging
import pprint


class Wallet:

    ENDPOINT = 'https://api-testnet.bybit.com'

    def __init__(self, sub_acct: int = None):
        """Constructor"""

        if sub_acct:
            self.BYBIT_API_KEY = os.environ[f'SUB_{sub_acct}_BYBIT_API_KEY']
            self.BYBIT_API_SECRET = os.environ[f'SUB_{sub_acct}_BYBIT_API_SECRET']
        else:
            self.BYBIT_API_KEY = os.environ['BYBIT_API_KEY']
            self.BYBIT_API_SECRET = os.environ['BYBIT_API_SECRET']

        self.session = spot.HTTP(
            endpoint=self.ENDPOINT,
            api_key=self.BYBIT_API_KEY,
            api_secret=self.BYBIT_API_SECRET,
        )
        self.ws_session = spot.WebSocket(
            test=True,
            api_key=self.BYBIT_API_KEY,
            api_secret=self.BYBIT_API_SECRET,
            ping_interval=10,  # the default is 30
            ping_timeout=5,  # the default is 10
        )

    def get_available_balance(self, symbol):
        response = self.session.get_wallet_balance()
        logging.info(f"Balance Response: {response}")
        for coin in response['result']['balances']:
            if coin['coin'] == symbol:
                logging.info(f"{symbol} Balance: {coin['free']}")
                return float(coin['free'])
        return 0.0

    def submit_order(self, order):
        # try:
        response = self.session.place_active_order(**order)
        logging.info(response)
        logging.info('  * ORDER PLACED *')
        logging.info
        return response
        # except Exception as e:
        #     logging.error(e)

    def get_active_orders(self, symbol):
        return self.session.get_active_order(symbol=symbol)

    def log_active_orders(self, symbol):
        orders = self.session.get_active_order(symbol=symbol)
        logging.info(orders)
        pprint.pprint(orders)
        for order in orders['result']['data']:
            string = f"{order['side']} {order['qty']} {order['symbol']} @ ${order['price']} ({order['order_status']})"
            print(string)
            logging.info(string)

    def get_position(self, symbol, category="linear"):
        return self.session.my_position(category=category, symbol=symbol)
