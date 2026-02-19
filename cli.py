import typer
from bot.orders import create_order
# from bot.validators import validate_side, validate_order_type
from bot.logging_config import setup_logger

app = typer.Typer()

@app.command()
def trade():
    setup_logger()

    symbol = typer.prompt("Enter Symbol (e.g., BTCUSDT)")
    side = typer.prompt("Side (BUY/SELL)")
    order_type = typer.prompt("Order Type (MARKET/LIMIT/STOP_LIMIT)")
    quantity = float(typer.prompt("Quantity"))

    price = None
    stop_price = None

    if order_type in ["LIMIT", "STOP_LIMIT"]:
        price = float(typer.prompt("Limit Price"))

    if order_type == "STOP_LIMIT":
        stop_price = float(typer.prompt("Stop Price (Trigger Price)"))

    typer.echo("\n--- Order Summary ---")
    typer.echo(f"Symbol: {symbol}")
    typer.echo(f"Side: {side}")
    typer.echo(f"Type: {order_type}")
    typer.echo(f"Quantity: {quantity}")

    try:
        response = create_order(
            symbol, side, order_type, quantity, price, stop_price
        )

        typer.echo("\n✅ Order Placed Successfully!")
        typer.echo(f"Order ID: {response.get('orderId')}")
        typer.echo(f"Status: {response.get('status')}")
        typer.echo(f"Executed Qty: {response.get('executedQty')}")

    except Exception as e:
        typer.echo(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    app()
