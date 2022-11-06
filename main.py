# ----------------------------------------------- #
# Plugin Name           : TradingView-Webhook-Bot #
# Author Name           : fabston                 #
# File Name             : main.py                 #
# ----------------------------------------------- #

import logging
import time

from flask import Flask, request

import config
import alert_handler
import order_handler


logging.basicConfig(filename="main.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

app = Flask(__name__)


def get_timestamp():
    timestamp = time.strftime("%Y-%m-%d %X")
    return timestamp


@app.route("/webhook", methods=["POST"])
def webhook():
    # try:
    dir(request)
    # logging.info(f'\n(log) Request received: {request.data}')
    if request.method == "POST":
        data = request.get_json()
        key = data["key"]
        if key == config.sec_key:
            # logging.info(get_timestamp(), "Alert Received & Sent!")
            alert_handler.send_alert(data)
            order_handler.submit_order(data)
            return "Sent alert", 200

        else:
            logging.info("[X]", get_timestamp(), "Alert Received & Refused! (Wrong Key)")
            return "Refused alert", 400
    # except Exception as e:
    #     logging.error("[X]", get_timestamp(), "Error:\n>", e)
    #     return "Error", 400


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
