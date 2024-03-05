import time
from request import open_positions, create_limit_buy_order, cancel_all_orders

# Implementation - create and cancel buy orders
def bot(phemex, symbol, size, bid):
  
