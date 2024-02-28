import time
import schedule
from config import load_api_credentials, load_trading_params
from request import initialize_mexc, create_limit_buy_order, cancel_all_orders

# Load API credentials from config
api_key, secret = load_api_credentials()

# Initialize MXC exchange
mexc = initialize_mexc(api_key, secret)

# Load trading parameters from config
trading_params, order_params = load_trading_params()

# Extract values from trading_params
symbol = trading_params.get('symbol')
size = trading_params.get('size')
bid = trading_params.get('bid')
params = {'timeInForce': order_params.get('timeInForce')}

def bot():
    create_limit_buy_order(mexc, symbol, size, bid, params)
    time.sleep(10)
    cancel_all_orders(mexc, symbol)

schedule.every(28).seconds.do(bot)

while True:
    schedule.run_pending()
    time.sleep(1)
