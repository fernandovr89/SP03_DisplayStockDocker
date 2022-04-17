import pandas as pd
import yfinance as yf

# Retrieves the stock quote for the given symbol
# from Yahoo Finance as a float.
# Input:  symbol - stock symbol as a string
# Output: price  - latest trade price from yahoo finance
def get_fixstock_quote(symbol, diff_time, current_time):
    try:
        data = yf.download(f"{symbol}", threads=False, start=diff_time, end=current_time)
    except Exception as e:
        print(e)
        data = pd.DataFrame()

    price_fl = None
    if not data.empty:
        price_fl = float(str("%5.3f" % data["Close"].values[-1]))
    return price_fl
