from bot.client import BinanceFuturesClient
from bot.validators import FuturesValidator

def create_order(symbol, side, order_type, quantity, price=None, stop_price=None):
    client = BinanceFuturesClient()
    validator = FuturesValidator(symbol)

    validator.validate_quantity(quantity)
    validator.validate_min_notional(quantity)
    validator.validate_margin(quantity, leverage=10)

    if order_type == "STOP_LIMIT":
        validator.validate_stop_order(side, stop_price)
    
    print(order_type, side, quantity, price, stop_price)

        
    validator.validate_side(side)
    validator.validate_order_type(order_type)
    validator.validate_price(price)
    validator.validate_stop_price(stop_price)
    
    

    order_params = {
        "symbol": symbol.upper(),
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }

    if order_type == "LIMIT":
        order_params["price"] = price
        order_params["timeInForce"] = "GTC"

    if order_type == "STOP_LIMIT":
        order_params["type"] = "STOP"
        order_params["price"] = price
        order_params["stopPrice"] = stop_price
        order_params["timeInForce"] = "GTC"

    response = client.place_order(**order_params)
    return response
