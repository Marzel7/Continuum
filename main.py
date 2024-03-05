import time
import schedule
from config import load_api_credentials, load_trading_params
from request import initialize_phemex
from bots.bot1 import bot # Import your bots

# Load API credentials from config
api_key, secret = load_api_credentials()


# Initialize Phemex exchange
phemex = initialize_phemex(api_key, secret)



# Load trading parameters from config
trading_params, order_params = load_trading_params()

# Extract values from trading_params
symbol = trading_params.get('symbol')
size = trading_params.get('size')
bid = trading_params.get('bid')
params = {'timeInForce': order_params.get('timeInForce'), 'type': 'spot'}

bot(symbol, size, bid)

# Schedule the bot function to run once after 28 seconds with arguments
#schedule.every(28).seconds.do(lambda: bot(phemex, symbol, size, bid, params))

# Run all pending tasks immediately
#schedule.run_all()
while True:
    schedule.run_pending()
    time.sleep(1)
