import ccxt
from config import load_api_credentials
import time
import pandas as pd

phemex = None

def initialize_phemex(api_key, api_secret):
    global phemex
    phemex = ccxt.phemex({
        'enableRateLimit': True,
        'apiKey': api_key,
        'secret': api_secret,
        'options': {
            'defaultType': 'swap',  # set the default spot/swap
        }
    })
    return phemex

def create_limit_order(action, symbol, size, price):
    params = {'type': 'swap', 'code': 'USD'}
    try:
        if action == 'buy':
            order = phemex.create_limit_buy_order(symbol, size, price, params)
        elif action == 'sell':
            order = phemex.create_limit_sell_order(symbol, size, price, params)
        print(f"Order created: {order}")
    except ccxt.BaseError as e:
        print(f"Error creating order: {e}")

def cancel_all_orders(symbol):
    try:
        phemex.cancel_all_orders(symbol)
        print("All orders canceled.")
    except ccxt.BaseError as e:
        print(f"Error canceling orders: {e}")

def open_positions(symbol):
    position_mapping = {'uBTCUSD': 2, 'ETHUSD': 1, 'DOGEUSDT': 0}
    index_pos = position_mapping.get(symbol, None)

    if index_pos is not None:
        phe_bal = phemex.fetch_balance()
        open_positions = phe_bal['info']['data']['positions']

        openpos_side = open_positions[index_pos]['side']
        openpos_size = open_positions[index_pos]['size']

        openpos_bool = openpos_side in ['Buy', 'Sell']
        long = True if openpos_side == 'Buy' else (False if openpos_side == 'Sell' else None)

        print(f'open_positions... | openpos_bool {openpos_bool} | openpos_size {openpos_size} | long {long} | index_pos {index_pos}')
        return open_positions, openpos_bool, openpos_size, long, index_pos
    else:
        print(f'Invalid symbol: {symbol}')
        return None

def ask_bid(symbol):
    ob = phemex.fetch_order_book(symbol)
    bid = ob['bids'][0][0]
    ask = ob['asks'][0][0]

    print(f'this is the ask for {symbol} {ask}')
    return ask, bid

def kill_switch(symbol):
    print(f'starting the kill switch for {symbol}')
    openposi = open_positions(symbol)[1]
    long = open_positions(symbol)[3]
    kill_size = open_positions(symbol)[2]

    print(f'openposi {openposi}, long {long}, size {kill_size}')

    while openposi:
        print('starting kill switch loop til limit fil..')
        temp_df = pd.DataFrame()
        print('just made a temp df')

        cancel_all_orders(symbol)
        openposi = open_positions(symbol)[1]
        long = open_positions(symbol)[3]
        kill_size = int(kill_size)

        ask = ask_bid(symbol)[0]
        bid = ask_bid(symbol)[1]

        if long is not None:
            action = 'buy' if long else 'sell'
            create_limit_order(action, symbol, kill_size, bid if long else ask)
            print(f'Just made a {action.upper()} to Close of {kill_size} {symbol} at ${bid if long else ask}')
            print('sleeping for 30 seconds to see if it fills..')
            time.sleep(30)
        else:
            print('Positions closed')

# # Example usage:
# api_key = 'your_api_key'
# api_secret = 'your_api_secret'
# initialize_phemex(api_key, api_secret)

# # Now you can use the functions in a cleaner way
# create_limit_order('buy', 'BTC/USD', 1, 50000)
# cancel_all_orders('BTC/USD')
# open_positions('BTC/USD')
# ask_bid('BTC/USD')
# kill_switch('BTC/USD')
