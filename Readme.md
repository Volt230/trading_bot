# Binance Futures Testnet Trading Bot

A simplified trading bot built in Python for Binance USDT-M Futures Testnet.

This project demonstrates:

- Market, Limit, and Stop-Limit order placement
- Structured architecture (client / validators / order logic separation)
- Risk validation before sending orders
- Logging of requests and responses
- Enhanced CLI using Typer
- Lightweight UI using Streamlit

---

## 📌 Features

### Core
- Place MARKET orders
- Place LIMIT orders
- Place STOP-LIMIT orders
- BUY and SELL supported
- Pre-trade validation 
- Structured logging to file

### Bonus
- Interactive CLI
- Streamlit web interface
- Risk-aware validation engine

### RUN
- Through cli : python cli.py
- Tjrough Streamlit UI : streamlit run ui.py