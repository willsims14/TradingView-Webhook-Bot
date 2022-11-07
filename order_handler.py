from order.order import Order
import logging
import json


logging.basicConfig(filename="main.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

def handle_order(data):
    """Submit order to ByBit"""


    # TODO: Write orders to a log or DB
    # for key, val in data.items():
    #     print(f"{key}: {val}")
