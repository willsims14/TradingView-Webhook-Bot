"""
To see which endpoints are available, you can read the API docs at
https://bybit-exchange.github.io/docs/inverse/#t-introduction

Some methods will have required parameters, while others may be optional.
The arguments in pybit methods match those provided in the Bybit API
documentation.

The following functions are available:

exit()

Public Methods:
------------------------
orderbook()
query_kline()
latest_information_for_symbol()
public_trading_records()
query_symbol()
liquidated_orders()
query_mark_price_kline()
query_index_price_kline()
query_premium_index_kline()
open_interest()
latest_big_deal()
long_short_ratio()
get_the_last_funding_rate()

Private Methods:
(requires authentication)
------------------------
place_active_order()
get_active_order()
cancel_active_order()
cancel_all_active_orders()
replace_active_order()
query_active_order()

place_conditional_order()
get_conditional_order()
cancel_conditional_order()
cancel_all_conditional_orders()
replace_conditional_order()
query_conditional_order()

user_leverage()
change_user_leverage()
cross_isolated_margin_switch()
position_mode_switch()
full_partial_position_tp_sl_switch()

my_position()
change_margin()
set_trading_stop()

query_trading_fee_rate()

get_risk_limit()
set_risk_limit()

my_last_funding_fee()
predicted_funding_rate()

api_key_info()

get_wallet_balance()
wallet_fund_records()
withdraw_records()
user_trade_records()

server_time()
announcement()

Spot Methods:
(many of the above methods can also be used with the spot market, provided the argument spot=True is passed)
------------------------
fast_cancel_active_order()
batch_cancel_active_order()
batch_fast_cancel_active_order()
batch_cancel_active_order_by_ids()

Asset Transfer Methods:
------------------------
create_internal_transfer()
create_subaccount_transfer()
query_transfer_list()
query_subaccount_transfer_list()
query_subaccount_list()

Custom Methods:
(requires authentication)
------------------------
place_active_order_bulk()
cancel_active_order_bulk()
place_conditional_order_bulk()
cancel_conditional_order_bulk()
close_position()

Cross Margin Trading Methods:
------------------------
borrow_margin_loan()
repay_margin_loan()
query_borrowing_info()
query_account_info()
query_interest_quota()
query_repayment_history()

Leveraged Tokens Trading Methods:
------------------------
lt_asset_info()
lt_market_info()
lt_purchase()
lt_redeem()
lt_purchase_redemption_history()




"""

# Import pybit and define the HTTP object.
from pybit import HTTP  # supports inverse perp & futures, usdt perp, spot.
from pybit.spot import HTTP
from pprint import pprint
import os
"""
Some methods might need extra arguments due to the current Bybit APIs -
which are divided across market types. To ensure you're sending requests to
a specific market type, like Inverse Perpetual, you can import and define
HTTP like so:

from pybit.inverse_perpetual import HTTP   <-- exclusively supports spot.
"""
from pybit import spot  # <-- import HTTP & WSS for spot



"""
Spot & other APIs.
from pybit import HTTP  <-- supports inverse perp & futures, usdt perp, spot.
from pybit.spot import HTTP   <-- exclusively supports spot.
"""

# Reassign session_auth to exclusively use spot.
session_auth = spot.HTTP(
    endpoint="https://api.bybit.com",
    api_key=os.environ['BYBIT_API_KEY'],
    api_secret=os.environ['BYBIT_API_SECRET']
)

# Require spot endpoint (`spot` arg unnecessary)
session_auth.get_wallet_balance(coin="BTC")