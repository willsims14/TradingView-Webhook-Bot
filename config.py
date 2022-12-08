# ByBit Config
BYBIT_SYMBOL_TO_TRADE = 'BTC'
BYBIT_SYMBOL_STABLE_COIN = 'USDT'
BYBIT_SYMBOL = BYBIT_SYMBOL_TO_TRADE + BYBIT_SYMBOL_STABLE_COIN
BYBIT_RISK_LEVEL = 0.45  # order_qty = available_bal * risk_level
BYBIT_SUBMIT_ORDER_FIELDS = (
    'symbol',
    'qty',
    'side',
    'type',
    'timeInForce',
    'price',
    'orderLinkId',
)

BYBIT_REDUCE_ONLY = 'false'
BYBIT_CLOSE_ON_TRIGGER = False
BYBIT_TIME_IN_FORCE = 'GTC'   # 'GTC', 'FOK'
BYBIT_TAKE_PROFIT = None
BYBIT_STOP_LOSS = None
BYBIT_CATEGORY = 'linear'

# Alerting Config
send_discord_alerts = True
send_email_alerts = False
