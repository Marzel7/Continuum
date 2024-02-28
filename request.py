import ccxt

def initialize_mexc(api_key, secret):
    return ccxt.mexc({
        'apiKey': api_key,
        'secret': secret,
    })

def create_limit_buy_order(exchange, symbol, size, bid, params):
    try:
        order = exchange.create_limit_buy_order(symbol, size, bid, params)
        print(f"Order created: {order}")
    except ccxt.BaseError as e:
        print(f"Error creating order: {e}")

def cancel_all_orders(exchange, symbol):
    try:
        exchange.cancel_all_orders(symbol)
        print("All orders canceled.")
    except ccxt.BaseError as e:
        print(f"Error canceling orders: {e}")
