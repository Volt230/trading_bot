from bot.client import BinanceFuturesClient


class FuturesValidator:
    def __init__(self, symbol: str):
        self.symbol = symbol.upper()
        self.client_wrapper = BinanceFuturesClient()
        self.client = self.client_wrapper.client

        self.mark_price = float(
            self.client.futures_mark_price(symbol=self.symbol)["markPrice"]
        )

        self.exchange_info = self.client.futures_exchange_info()
        self.symbol_info = next(
            s for s in self.exchange_info["symbols"] if s["symbol"] == self.symbol
        )


    def validate_quantity(self, quantity: float):
        lot_filter = next(
            f for f in self.symbol_info["filters"] if f["filterType"] == "LOT_SIZE"
        )

        min_qty = float(lot_filter["minQty"])

        if quantity < min_qty:
            raise ValueError(f"Quantity must be >= {min_qty}")

        return quantity

    def validate_min_notional(self, quantity: float):
        notional = quantity * self.mark_price

        if notional < 100:
            raise ValueError(
                f"Order notional {notional:.2f} USDT < 100 USDT minimum required."
            )

        return notional

    def validate_margin(self, quantity: float, leverage: int = 1):
        balance = self._get_balance()

        notional = quantity * self.mark_price
        required_margin = notional / leverage

        if required_margin > balance:
            raise ValueError(
                f"Insufficient margin. Required: {required_margin:.2f}, "
                f"Available: {balance:.2f}"
            )

        return required_margin

    def _get_balance(self):
        balances = self.client.futures_account_balance()
        for b in balances:
            if b["asset"] == "USDT":
                return float(b["balance"])

        return 0.0

    def validate_stop_order(self, side: str, stop_price: float):
        if side == "BUY":
            if stop_price <= self.mark_price:
                raise ValueError(
                    f"BUY stop must be above current price {self.mark_price}"
                )

        if side == "SELL":
            if stop_price >= self.mark_price:
                raise ValueError(
                    f"SELL stop must be below current price {self.mark_price}"
                )
        return stop_price

    def validate_side(self,side: str):
        side = side.upper()
        if side not in ["BUY", "SELL"]:
            raise ValueError("Side must be BUY or SELL")
        return side

    def validate_order_type(self,order_type: str):
        order_type = order_type.upper()
        if order_type not in ["MARKET", "LIMIT", "STOP_LIMIT"]:
            raise ValueError("Order type must be MARKET, LIMIT, or STOP_LIMIT")
        return order_type

    def validate_price(self,price):
        if price is not None and price <= 0:
            raise ValueError("Price must be greater than 0")
        return price

    def validate_stop_price(self,stop_price):
        if stop_price is not None and stop_price <= 0:
            raise ValueError("Stop price must be greater than 0")
        return stop_price