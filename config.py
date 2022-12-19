# Spot Config
BYBIT_SYMBOL_TO_TRADE = 'BTC'
BYBIT_SYMBOL_STABLE_COIN = 'USDT'
BYBIT_SYMBOL = BYBIT_SYMBOL_TO_TRADE + BYBIT_SYMBOL_STABLE_COIN
BYBIT_SPOT_RISK_LEVEL = 0.45  # order_qty = available_bal * risk_level
BYBIT_SPOT_ORDER_FIELDS = (
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


# Derivatives Config
BYBIT_USDT_PERP_RISK_LEVEL = 0.30
BYBIT_USDT_PERP_ORDER_FIELDS = (
    'symbol',
    'side',
    'order_type',
    'qty',
    'price',
    'time_in_force',
    'reduce_only',
    'take_profit',
    'close_on_trigger',
)
BYBIT_USDT_PERP_REDUCE_ONLY = 'false'
BYBIT_USDT_PERP_CLOSE_ON_TRIGGER = False
BYBIT_USDT_PERP_TIME_IN_FORCE = 'GoodTillCancel'
BYBIT_USDT_PERP_TAKE_PROFIT_PERCENTAGE = 0.001
BYBIT_USDT_PERP_STOP_LOSS = None
BYBIT_USDT_PERP_CATEGORY = 'linear'

# Alerting Config
send_discord_alerts = True
send_email_alerts = False
