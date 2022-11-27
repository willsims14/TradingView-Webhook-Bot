import logging


class Order:
    """ByBit Order Model"""

    time_in_force = 'GoodTillCancel'
    close_on_trigger = False
    reduce_only = False
    take_profit = None
    stop_loss = None

    def __init__(self, side, symbol, order_type, qty, **kwargs):
        self.side = side.title()
        self.symbol = symbol
        self.order_type = order_type
        self.qty = qty
        self.reduce_only = 'false'
        self.close_on_trigger = 'false'
        self.time_in_force = 'GTC'
        self.take_profit = None
        self.stop_loss = None
        self.category = 'linear'
        self.price = kwargs.get('price')
        self.account = kwargs.get('account', None)

        for key, val in kwargs.items():
            setattr(self, key, val)

    def __str__(self):
        return f"[{self.side.upper()}] {self.order_type} Order:  {self.qty} {self.symbol} @ {self.price}"

    def as_dict(self):
        d = {
            "side": self.side,
            "symbol": self.symbol,
            # "orderType": self.order_type,
            "type": self.order_type.upper(),
            "qty": str(round(self.qty, 7)),
            "price": self.price,
            "reduceOnly": self.reduce_only,
            "closeOnTrigger": self.close_on_trigger,
            "timeInForce": self.time_in_force,
            "category": self.category,
            # "takeProfit":  self.take_profit,
            # "stopLoss":  self.stop_loss,
        }
        for key, val in d.items():
            logging.info(f"{key}: {val}")
        return d
