# ----------------------------------------------- #
# Plugin Name           : TradingView-Webhook-Bot #
# Author Name           : fabston                 #
# File Name             : main.py                 #
# ----------------------------------------------- #

# from logging.config import dictConfig
import logging
import time

from flask import Flask, request

import config
import alert_handler
# import order_handler
from order.order import Order
from wallet.wallet import Wallet

logging.basicConfig(filename="main.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

app = Flask(__name__)

w = Wallet()

def get_timestamp():
    timestamp = time.strftime("%Y-%m-%d %X")
    return str(timestamp)


@app.route("/webhook", methods=["POST"])
def webhook():
    logging.info('')
    logging.info('------------ New Webhook Alert ------------')
    try:
        logging.info(f'[DEBUGGING] Request received: {request.data}')
        if request.method == "POST":
            data = request.get_json()
            logging.info(f'[DEBUGGING] Request received: {data}')
            if data is None:
                logging.info(f'[DEBUGGING]  !!  BAD JSON  !! ')
            key = data["key"]
            if key == config.sec_key:
                alert_handler.send_alert(data)
                # order_handler.handle_order(data)

                # TODO: remove hard-coded symbol
                # data['symbol'] = 'BTCUSDT'

                data['qty'] = w.calculate_order_qty(data['symbol'], data['price'])
                o = Order(**data)

                for key,val in o.as_dict().items():
                    logging.info(f"{key}: {val}")
                w.submit_order(o.as_dict())
                logging.info('--- order ---')
                logging.info(o)
                logging.info('-------------')
                logging.info(get_timestamp() + " Alert Received & Sent!")
                return "Sent alert", 200
            else:
                logging.info("[X] Alert Received & Refused! (Wrong Key)")
                return "Refused alert", 400
    except Exception as e:
        logging.error(e)
        return "Error", 400


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
