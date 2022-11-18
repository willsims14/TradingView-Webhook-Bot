import os

from pybit import inverse_perpetual
from pybit import usdt_perpetual
from pybit import spot
import logging
import pprint

class Wallet:

    ENDPOINT = 'https://api-testnet.bybit.com'
    BYBIT_API_KEY = os.environ['BYBIT_API_KEY']
    BYBIT_API_SECRET = os.environ['BYBIT_API_SECRET']

    def __init__(self):
        """Constructor"""

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
        # for x in dir(self.session):
        #     print(x)


    def get_available_balance(self, symbol):
        response = self.session.get_wallet_balance()
        for coin in response['result']['balances']:
            if coin['coin'] == symbol:
                return float(coin['free'])
        return response['result']['balances']

    def calculate_order_qty(self, symbol, symbol_price):
        if symbol == 'BTCUSDT':
            balance = self.get_available_balance('USDT')
            logging.info(f'USDT Balance: {balance}')
            amount_to_spend = balance * 0.01
            qty = round(amount_to_spend / symbol_price, 6)
            logging.info(f'1% of USDT Balance: {qty}')
            return qty

    def submit_order(self, order):
        try:
            response = self.session.place_active_order(**order)
            logging.info(response)
            logging.info('  * ORDER PLACED *')
            return response
        except Exception as e:
            logging.error(e)

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

    def get_position(self):
        return self.session.my_position(category='linear', symbol='BTCUSDT')


    def stream_orderbook(self,):
        self.ws_session.orderbook_25_stream(self.handle_orderbook, 'BTCUSDT')
        # return x

    def handle_orderbook(self, message):

        print(message)
        orderbook_data = message["data"]
