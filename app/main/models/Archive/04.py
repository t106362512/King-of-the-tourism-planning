import yfinance as yf
from pprint import pprint
from datetime import datetime
data = yf.download("SPY AAPL", start="2017-01-01", end="2017-01-04")
pprint(data.to_json(date_unit='s'))