import logging
import streamlit as st
from bot.orders import create_order
from bot.logging_config import setup_logger


logger = setup_logger()

st.title("Binance Futures Testnet Trading Bot")
    
symbol = st.text_input("Symbol", "BTCUSDT")

side = st.selectbox("Side", ["BUY", "SELL"])
order_type = st.selectbox("Order Type", ["MARKET", "LIMIT", "STOP_LIMIT"])
quantity = st.number_input("Quantity", min_value=0.0, step=0.001)

price = None
stop_price = None

if order_type in ["LIMIT", "STOP_LIMIT"]:
    price = st.number_input("Limit Price", min_value=0.0)

if order_type == "STOP_LIMIT":
    stop_price = st.number_input("Stop Price", min_value=0.0)

if st.button("Place Order"):
    try:
        response = create_order(
            symbol, side, order_type, quantity, price, stop_price
        )

        st.success("Order Placed Successfully!")
        st.write("Order ID:", response.get("orderId"))
        st.write("Status:", response.get("status"))
        st.write("Executed Qty:", response.get("executedQty"))

    except Exception as e:
        logging.error(f"Error placing order: {str(e)}")
        st.error(str(e))

