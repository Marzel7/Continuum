import time
from request import ask_bid, kill_switch, create_limit_order, open_positions

# Your implementation - create and cancel buy orders
def bot(symbol, size, bid):
    create_limit_order('buy', symbol, size, bid)
    time.sleep(10)
    open_positions(symbol)
    #cancel_all_orders(phemex, symbol)
    ask_bid(symbol)
    kill_switch(symbol)


