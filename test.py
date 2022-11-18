from wallet.wallet import Wallet
from pybit import usdt_perpetual
from pybit import spot

from pprint import pprint
import json
import bybit
import os

ENDPOINT = 'https://api-testnet.bybit.com'
BYBIT_API_KEY = os.environ['BYBIT_API_KEY']
BYBIT_API_SECRET = os.environ['BYBIT_API_SECRET']


ws_spot = spot.WebSocket(test=True)
session = spot.HTTP(
    endpoint=ENDPOINT,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET,
)

def handle_orderbook(message):
    # I will be called every time there is new orderbook data!
    print(message)
    orderbook_data = message["data"]

order = {
    'symbol': 'BTCUSDT',
    'qty': '0.5',
    'side': 'Buy',
    'type': 'Limit',
    'timeInForce': "GTC",
    'price': '16480.00'
}

session.place_active_order(**order)
# handle_orderbook() will now be called for both inverse and spot data.
# To keep the data separate, simply create another function and pass it below.

usdt_bal = session.get_wallet_balance()['result']['balances'][0]
print(f"USDT Balance: {usdt_bal['free']} (Total: {usdt_bal['total']})")
while True:
    active_order = session.get_active_order()
    pprint(active_order['result'])

ws_spot.depth_v2_stream(handle_orderbook, "BTCUSDT")
pprint(wb)
