import configparser
from dotenv import load_dotenv
import os

def load_trading_params():
    config = configparser.ConfigParser()
    config.read('config.ini')

    trading_params = dict(config['TradingParams'])
    order_params = dict(config['OrderParams'])
    return trading_params, order_params

def load_api_credentials():
    load_dotenv()
    api_key = os.getenv('apiKey')
    api_secret = os.getenv('secret')
    return api_key, api_secret









