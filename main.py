
from flask import Flask, request

import logging
import time

from wallet.wallet import Wallet
import alert_handler
import config

logging.basicConfig(filename="main.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

app = Flask(__name__)


WALLETS = {
    0: Wallet(),
    1: Wallet(sub_acct=1),
    2: Wallet(sub_acct=2),
    3: Wallet(sub_acct=3),
}


@app.route("/webhook", methods=["POST"])
def validate_request():
    """Entrypoint"""

    logging.info(f'------------ New Request ------------\n{request.data}')
    data = request.get_json()
    wallet = WALLETS[int(data["account"])]

    if data['side'].lower() == 'buy':
        result = buy(wallet, data)
    elif data['side'].lower() == 'sell':
        result = sell(wallet, data)
    else:
        return 'Key "side" not in request', 400

    alert_handler.send_alert(data)
    logging.info('')
    logging.info('\n\n')
    return result


def buy(wallet, data):
    """Execute ByBit BUY Order"""

    available_bal = wallet.get_available_balance(config.BYBIT_SYMBOL_STABLE_COIN)
    if available_bal < 25.0:
        logging.info('Balance < 25 USDT - Ignoring')
        return "Insufficient Balance", 400

    # if data['type'].lower() == 'market':
    data['type'] = 'Market'
    logging.info('TYPE = MARKET')
    data['qty'] = round(available_bal * config.BYBIT_RISK_LEVEL, 5)
    # else:
    #     logging.info('TYPE = LIMIT')
    #     data['qty'] = round((available_bal * config.BYBIT_RISK_LEVEL) / data['price'], 6)

    o = add_constants(data)
    logging.info(o)
    response = wallet.submit_order(o)
    logging.info(response)
    return "Sent alert", 200


def sell(wallet, data):
    """Execute ByBit SELL Order"""

    available_bal = wallet.get_available_balance(config.BYBIT_SYMBOL_TO_TRADE)
    data['qty'] = round(available_bal - (available_bal * 0.02), 5)
    o = add_constants(data)
    logging.info(o)
    response = wallet.submit_order(o)
    logging.info(response)
    return "Sent alert", 200


# Helper Methods
def get_timestamp():
    timestamp = time.strftime("%Y-%m-%d %X")
    return str(timestamp)


def add_constants(data):
    """Add constants to ByBit API Call"""

    # data['reduce_only'] = config.BYBIT_REDUCE_ONLY
    # data['close_on_trigger'] = config.BYBIT_CLOSE_ON_TRIGGER
    data['timeInForce'] = config.BYBIT_TIME_IN_FORCE
    # data['take_profit'] = config.BYBIT_TAKE_PROFIT
    # data['stop_loss'] = config.BYBIT_STOP_LOSS
    # data['category'] = config.BYBIT_CATEGORY
    data['symbol'] = config.BYBIT_SYMBOL

    return {k: v for k, v in data.items() if k in config.BYBIT_SUBMIT_ORDER_FIELDS}


if __name__ == "__main__":
    app.run(debug=True)
