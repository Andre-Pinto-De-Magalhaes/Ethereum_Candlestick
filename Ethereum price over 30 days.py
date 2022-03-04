'''Program will retrive data on ethereum from Coin Gecko to create a candlestick
chart that tracks the prices of ethereum over a period of 30 days'''

import pandas as pd
from pycoingecko import CoinGeckoAPI 
import plotly.graph_objects as go


#initialize class/object
cg = CoinGeckoAPI()


######## Get data from Coin Gecko#######
#retrieves data on ethereum in 30 day time period
ethereum_data = cg.get_coin_market_chart_by_id(id='ethereum', vs_currency = 'usd', days = 30)

eth_price_data = ethereum_data['prices']

#######organize data and convert values to readable data#####

data = pd.DataFrame(eth_price_data, columns = ['TimeStamp', 'Price'])

data['Date'] = pd.to_datetime(data['TimeStamp'], unit=('ms'))





#########Create candlestick chart with data############

#Groups data by date to get daily min, max, open price and closing price
candlestick_data = data.groupby(data.Date.dt.date).agg({'Price':['min','max','first','last' ]})





fig = go.Figure(data = [go.Candlestick(x = candlestick_data.index,
               open = candlestick_data['Price']['first'],
               high = candlestick_data['Price']["max"],
               low = candlestick_data['Price']['min'],
               close = candlestick_data['Price']['last'])
                        ])

fig.update_layout(xaxis_rangeslider_visible = False, xaxis_title = 'Date',
                  yaxis_title = 'Price(USD$)', title = 'Ethereum Prices over 30 days')
               


fig.write_html('Ethereum price over 30 days.html', auto_open = True)