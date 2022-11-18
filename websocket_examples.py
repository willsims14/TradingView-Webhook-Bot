

"""
To see which endpoints and topics are available, check the Bybit API
documentation: https://bybit-exchange.github.io/docs/inverse/#t-websocket
There are several WSS URLs offered by Bybit, which pybit manages for you.
However, you can set a custom `domain` as shown below.
"""

from time import sleep

# Import your desired markets from pybit
from pybit import inverse_perpetual
from pybit import spot

"""
An alternative way to import:
from pybit.inverse_perpetual import WebSocket, HTTP
"""

import logging
import os

BYBIT_API_KEY = os.environ['BYBIT_API_KEY']
BYBIT_API_SECRET = os.environ['BYBIT_API_SECRET']


logging.basicConfig(filename="pybit.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")



# Let's fetch the orderbook for BTCUSD. First, we'll define a function.
def handle_orderbook(message):
    # I will be called every time there is new orderbook data!
    print(message)
    orderbook_data = message["data"]



# Similarly, if you want to listen to the WebSockets of other markets:
ws_spot = spot.WebSocket(test=True, api_key=BYBIT_API_KEY, api_secret=BYBIT_API_SECRET)
# handle_orderbook() will now be called for both inverse and spot data.
# To keep the data separate, simply create another function and pass it below.
ws_spot.depth_v2_stream(handle_orderbook, "BTCUSDT")


while True:
    # This while loop is required for the program to run. You may execute
    # additional code for your trading logic here.
    sleep(1)