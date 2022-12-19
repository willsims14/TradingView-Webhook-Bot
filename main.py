
from flask import Flask, request

import logging
import time

from wallet.spot_wallet import SpotWallet
# from wallet.ip_wallet import InversePerpetualWallet
from wallet.usdt_perpetual_wallet import USDTPerpetualWallet


# import alert_handler
import config

logging.basicConfig(filename="main.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

app = Flask(__name__)


SPOT_WALLETS = {
    1: SpotWallet(sub_acct=1),
    2: SpotWallet(sub_acct=2),
    3: SpotWallet(sub_acct=3),
}
USDT_PERPETUAL_WALLETS = {
    0: USDTPerpetualWallet(),
    4: USDTPerpetualWallet(sub_acct=4),
}


@app.route("/webhook", methods=["POST"])
def validate_spot_request():
    """Spot Trading Entrypoint"""

    logging.info(f'------------ New Spot Trade ------------\n{request.data}')
    data = request.get_json()
    account_id = int(data["account"])
    wallet = SPOT_WALLETS[account_id]

    logging.info(f'Account #{account_id}')
    logging.info(f"Side: {data['side'].upper()}")
    if data['side'].lower() == 'buy':
        result = spot_buy(wallet, data)
    elif data['side'].lower() == 'sell':
        result = spot_sell(wallet, data)
    else:
        return 'Key "side" not in request', 400

    # alert_handler.send_alert(data)
    logging.info('')
    logging.info('\n\n')
    return result


def spot_buy(wallet, data):
    """Execute ByBit BUY Order"""

    available_bal = wallet.get_available_balance(config.BYBIT_SYMBOL_STABLE_COIN)
    if available_bal < 25.0:
        logging.info('Balance < 25 USDT - Ignoring')
        return "Insufficient Balance", 400

    data['qty'] = round(available_bal * config.BYBIT_SPOT_RISK_LEVEL, 5)
    response = wallet.submit_order(data)
    logging.info(response)
    return "Executed Trade: BUY ", 200


def spot_sell(wallet, data):
    """Execute ByBit SELL Order"""

    available_bal = wallet.get_available_balance(config.BYBIT_SYMBOL_TO_TRADE)
    data['qty'] = round(available_bal - (available_bal * 0.02), 5)
    response = wallet.submit_order(data)
    logging.info(response)
    return "Executed Trade: SELL", 200


@app.route("/usdtperpetual", methods=["POST"])
def validate_inverse_request():
    """Inverse Perp Trading Entrypoint"""

    logging.info(f'------------ New USDT Perpetual Trade ------------\n{request.data}')
    data = request.get_json()
    account_id = int(data["account"])
    wallet = USDT_PERPETUAL_WALLETS[account_id]

    logging.info(f'Account #{account_id}')
    logging.info(f"Side: {data['side'].upper()}")
    if data['side'].lower() == 'buy':
        result = usdt_perpetual_buy(wallet, data)
    elif data['side'].lower() == 'sell':
        result = usdt_perpetual_sell(wallet, data)
    else:
        return 'Key "side" not in request', 400

    # alert_handler.send_alert(data)
    logging.info('')
    logging.info('\n\n')
    return result


def usdt_perpetual_buy(wallet, data):
    available_bal = wallet.get_available_balance(config.BYBIT_SYMBOL_STABLE_COIN)
    if available_bal < 25.0:
        logging.info('Balance < 25 USDT - Ignoring')
        return "Insufficient Balance", 400

    data['qty'] = round((available_bal * config.BYBIT_USDT_PERP_RISK_LEVEL) / float(data['price']), 5)
    response = wallet.submit_order(data)
    logging.info(response)
    return "Executed Inverse Trade: BUY ", 200


def usdt_perpetual_sell(wallet, data):
    """Execute ByBit SELL Order"""

    available_bal = wallet.get_available_balance(config.BYBIT_SYMBOL_TO_TRADE)
    data['qty'] = round(available_bal - (available_bal * config.BYBIT_USDT_PERP_RISK_LEVEL), 5)
    # data['qty'] = round((available_bal * config.BYBIT_USDT_PERP_RISK_LEVEL) / float(data['price']), 5)
    response = wallet.submit_order(data)
    logging.info(response)
    return "Executed Inverse Trade: SELL", 200


# Helper Methods
def get_timestamp():
    timestamp = time.strftime("%Y-%m-%d %X")
    return str(timestamp)


if __name__ == "__main__":
    app.run(debug=True)
