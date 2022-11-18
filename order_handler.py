import logging
import json
import pandas as pd
from order.order import Order
from wallet.wallet import Wallet

logging.basicConfig(filename="main.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

w = Wallet(wallet_type='inverse_perpetual')




def handle_order(data):
    """Submit order to ByBit"""


    logging.info('ORDER HANDLER')

    for key,val in data.items():
        logging.info(f"{key}: {val}")

    if 'side' not in data:
        raise KeyError('Key, `side`, not in TradingView alert.')

    if 'BAR_close' not in data:
        raise KeyError('Key, `BAR_close`, not in TradingView alert.')

    if 'ticker' not in data:
        raise KeyError('Key, `ticker`, not in TradingView alert.')

    order_type = data.get('order_type', 'Market')
    price = data['BAR_close']
    # ticker = data['ticker'] . # TODO:
    ticker = 'BTCUSDT'

    qty = data.get('qty', None)
    if qty is None:
        qty = calculate_order_qty(ticker)

    o = Order(
        side=data['side'],
        symbol=ticker,
        order_type=order_type,
        qty=qty,
        price=price,
    )

    logging.info(o)
