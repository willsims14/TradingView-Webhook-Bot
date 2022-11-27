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
from order.order import Order
from wallet.wallet import Wallet

logging.basicConfig(filename="main.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

app = Flask(__name__)

RISK_LEVEL = 0.20


WALLETS = {
    0: Wallet(risk_level=RISK_LEVEL),
    1: Wallet(risk_level=RISK_LEVEL, sub_acct=1),
    2: Wallet(risk_level=RISK_LEVEL, sub_acct=2),
    3: Wallet(risk_level=RISK_LEVEL, sub_acct=3),
}


def get_timestamp():
    timestamp = time.strftime("%Y-%m-%d %X")
    return str(timestamp)


@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    logging.info(f'------------ New Webhook Alert ------------\n{request.data}')
    # try:
    if request.method == "POST":
        data = request.get_json()
        if data is None:
            logging.info('[DEBUGGING]  !!  BAD JSON  !! ')
            return "Bad JSON", 400

        key = data["key"]
        if key != config.sec_key:
            logging.info("[X] Alert Received & Refused! (Wrong Key)")
            return "Refused alert", 400

        wallet = WALLETS[int(data["account"])]
        if data['side'].lower() == 'buy' and data['order_type'].lower() == 'market':
            available_bal = wallet.get_available_balance('USDT')
            data['qty'] = (available_bal * RISK_LEVEL)
        else:
            data['qty'] = wallet.calculate_buy_order_qty(data['side'], data['symbol'], data['price'])

        # TODO: Refactor - remove class. Simply return a dict with the values I want
        o = Order(**data)
        wallet.submit_order(o.as_dict())
        logging.info(o)
        logging.info('')
        logging.info('\n\n')
        alert_handler.send_alert(data)
        return "Sent alert", 200

    # except Exception as e:
    #     logging.error(e)
    #     return "Error", 400


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
