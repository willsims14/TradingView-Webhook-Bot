from order.order import Order
import logging
import json


logging.basicConfig(filename="main.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

def submit_order(data):
    """Submit order to ByBit"""


    for key, val in data.items():
        print(f"{key}: {val}")