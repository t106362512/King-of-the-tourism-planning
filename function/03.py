from pandas_datareader import data as pdr
from pprint import pprint

import yfinance as yf
# yf.pdr_override() # <== that's all it takes :-)

# download dataframe
# data = pdr.get_data_yahoo("SPY", start="2019-01-01", end="2019-01-02")

data = yf.download("SPY", start="2017-01-01", end="2017-01-09",
                   group_by="ticker")

pprint(data.to_json(date_unit="s", date_format='iso'))
# pprint(data['Date'].dt.strftime('%Y-%m-%d').to_dict())
# pprint(data)
