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

RISK_LEVEL = 0.50


WALLETS = {
    0: Wallet(risk_level=RISK_LEVEL),
    1: Wallet(risk_level=RISK_LEVEL, sub_acct=1),
    2: Wallet(risk_level=RISK_LEVEL, sub_acct=2),
    3: Wallet(risk_level=RISK_LEVEL, sub_acct=3),
}


def get_timestamp():
    timestamp = time.strftime("%Y-%m-%d %X")
    return str(timestamp)


@app.route("/webhook", methods=["POST"])
def validate_request():
    logging.info(f'------------ New Request ------------\n{request.data}')
    if request.method != "POST":
        return f"Method {request.method} not allowed at this endpoint", 400

    data = request.get_json()
    if not data:
        logging.info('[DEBUGGING]  !!  BAD JSON  !! ')
        return "Bad JSON", 400

    wallet = WALLETS[int(data["account"])]

    if data['side'].lower() == 'buy':
        return buy(wallet, data)
    elif data['side'].lower() == 'sell':
        return sell(wallet, data)


# @app.route("/webhook-buy", methods=["POST"])
def buy(wallet, data):
    """ BUY """

    if data['order_type'].lower() == 'market':
        available_bal = wallet.get_available_balance('USDT')
        data['qty'] = round(available_bal * RISK_LEVEL, 6)
    else:
        data['qty'] = wallet.calculate_buy_order_qty(data['side'], data['symbol'], data['price'])

    if not data['qty']:
        logging.info("Insufficient Balance")
        logging.info(data)
        return "Insufficient Balance", 400

    # TODO: Refactor - remove class. Simply return a dict with the values I want
    o = Order(**data)
    wallet.submit_order(o.as_dict())
    logging.info(o)
    logging.info('')
    logging.info('\n\n')
    alert_handler.send_alert(data)
    return "Sent alert", 200


def sell(wallet, data):
    logging.info(f'------------ SELL ------------\n{request.data}')

    data['qty'] = wallet.calculate_sell_order_qty(data['side'], data['symbol'], data['price'])

    if not data['qty']:
        logging.info("Insufficient Balance")
        logging.info(data)
        return "Insufficient Balance", 400

    # TODO: Refactor - remove class. Simply return a dict with the values I want
    o = Order(**data)
    wallet.submit_order(o.as_dict())
    logging.info(o)
    logging.info('')
    logging.info('\n\n')
    alert_handler.send_alert(data)
    return "Sent alert", 200


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
