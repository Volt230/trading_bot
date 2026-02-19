import os
from binance.client import Client
from dotenv import load_dotenv
import logging

load_dotenv()

class BinanceFuturesClient:
    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")

        if not self.api_key or not self.api_secret:
            raise ValueError("API credentials not found in environment variables.")

        self.client = Client(self.api_key, self.api_secret)
        self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

    def place_order(self, **kwargs):
        try:
            logging.info(f"Placing order with params: {kwargs}")
            response = self.client.futures_create_order(**kwargs)
            logging.info(f"Order response: {response}")
            return response
        except Exception as e:
            logging.error(f"Error placing order: {str(e)}")
            raise
    def get_balance(self):
        try:
            logging.info("Fetching account balance")
            balance = self.client.futures_account_balance()
            logging.info(f"Account balance: {balance}")
            return balance
        except Exception as e:
            logging.error(f"Error fetching balance: {str(e)}")
            raise