import pandas as pd
import datetime
import yfinance as yf

from display.models import Stocks

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


def get_all_stocks():
    return Stocks.objects.all()


def download_stocks():
    # dotCode is used in Yahoo Finance (e.g ACCOR SA code is AC.PA)
    stocks = [
        {"name": "ACCOR", "dotCode": "AC.PA"},
        {"name": "AIR LIQUIDE", "dotCode": "AI.PA"},
        {"name": "AXA", "dotCode": "CS.PA"},
        {"name": "BNP PARIBAS", "dotCode": "BNP.PA"},
        {"name": "BOUYGUES", "dotCode": "EN.PA"},
        {"name": "CRCAM BRIE PICARDIE", "dotCode": "CRBP2.PA"},
        {"name": "CRCAM NORD France", "dotCode": "CNF.PA"},
        {"name": "DANONE", "dotCode": "BN.PA"},
        {"name": "EDENRED", "dotCode": "EDEN.PA"},
        {"name": "ENGIE", "dotCode": "ENGI.PA"},
        {"name": "ESSILOR LUXOTTICA", "dotCode": "EL.PA"},
        {"name": "HERMES INTL", "dotCode": "RMS.PA"},
        {"name": "ICADE", "dotCode": "ICAD.PA"},
        {"name": "IDI", "dotCode": "IDIP.PA"},
        {"name": "IPSEN", "dotCode": "IPN.PA"},
        {"name": "LAGARDERE", "dotCode": "MMB.PA"},
        {"name": "L'OREAL", "dotCode": "OR.PA"},
        {"name": "METROPOLE TELEVISION", "dotCode": "MMT.PA"},
        {"name": "MICHELIN", "dotCode": "ML.PA"},
        {"name": "ORANGE", "dotCode": "ORA.PA"},
        {"name": "PERNOD RICARD", "dotCode": "RI.PA"},
        {"name": "ROTHSCHILD", "dotCode": "ROTH.PA"},
        {"name": "RUBIS", "dotCode": "RUI.PA"},
        {"name": "SANOFI", "dotCode": "SAN.PA"},
        {"name": "SCHNEIDER ELECTRIC", "dotCode": "SU.PA"},
        {"name": "SCOR", "dotCode": "SCR.PA"},
        {"name": "THERMADOR GROUPE", "dotCode": "THEP.PA"},
        {"name": "TOTAL ENERGIES", "dotCode": "TTE.PA"},
        {"name": "UNIVERSAL MUSIC GROUP N.V.", "dotCode": "UMG.AS"},
        {"name": "VEOLIA ENVIRONNEMENT", "dotCode": "VIE.PA"},
        {"name": "VERALLIA", "dotCode": "VRLA.PA"},
        {"name": "VIVENDI", "dotCode": "VIV.PA"},
    ]
    price_fl = None
    Stocks.objects.all().delete()
    current_time_tmp = datetime.datetime.now() + datetime.timedelta(days=1)
    current_time = current_time_tmp.strftime("%Y-%m-%d")
    diff_time_tmp = datetime.datetime.now() - datetime.timedelta(days=6)
    diff_time = diff_time_tmp.strftime("%Y-%m-%d")
    print(current_time)
    print(diff_time)
    for stock in stocks:
        price_fl = get_fixstock_quote(stock["dotCode"], diff_time, current_time)
        if price_fl is None or type(price_fl) == str:
            price_fl = 0.0
        stock_model = Stocks(name=stock["name"], symbol=stock["dotCode"], price=price_fl)
        stock_model.save()
        price_fl = None

    return Stocks.objects.all()
