
from pybit import spot

import logging
import pprint
import os

import alert_handler
import config


class SpotWallet:

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

        order['reduce_only'] = config.BYBIT_REDUCE_ONLY
        order['close_on_trigger'] = config.BYBIT_CLOSE_ON_TRIGGER
        order['timeInForce'] = config.BYBIT_TIME_IN_FORCE
        order['take_profit'] = config.BYBIT_TAKE_PROFIT
        order['stop_loss'] = config.BYBIT_STOP_LOSS
        order['category'] = config.BYBIT_CATEGORY
        order['symbol'] = config.BYBIT_SYMBOL

        o = {k: v for k, v in order.items() if k in config.BYBIT_SPOT_ORDER_FIELDS}
        logging.info('Submitting Following Order to ByBit: ')
        logging.info(o)
        response = self.session.place_active_order(**o)
        # alert_handler.send_alert(order)
        order['response'] = response['result']
        alert_handler.send_alert(order)
        logging.info(response)
        logging.info('  * ORDER PLACED *')
        logging.info
        return response
        # except Exception as e:
        #     logging.error(e)

    def get_active_orders(self, symbol):
        return [o for o in self.session.get_active_order(symbol=symbol)['result'] if o['status'] not in ('CANCELED', 'FILLED')]

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

    def cancel_order(self, order_id=None, order_link_id=None):
        if not order_id:
            return self.session.cancel_active_order(orderLinkId=order_link_id)
        else:
            if order_link_id:
                return self.session.cancel_active_order(orderId=order_id, orderLinkId=order_link_id)
            return self.session.cancel_active_order(orderId=order_id)

    def fast_cancel_order(self, symbol, order_id):
        return self.session.cancel_active_order(symbolId=symbol, orderId=order_id)

    def query_active_orders(self, symbol):
        return self.session.query_active_order(symbol=symbol)
