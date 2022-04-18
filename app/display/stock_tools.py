import pandas as pd
import datetime
import yfinance as yf


from display.models import Stocks

from schedule import Scheduler
import threading
import time


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


def download_stocks(isJob=False):
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
    price_float = None
    Stocks.objects.all().delete()
    current_time_tmp = datetime.datetime.now() + datetime.timedelta(days=1)
    current_time = current_time_tmp.strftime("%Y-%m-%d")
    diff_time_tmp = datetime.datetime.now() - datetime.timedelta(days=6)
    diff_time = diff_time_tmp.strftime("%Y-%m-%d")
    stock_objects = []
    for index, stock in enumerate(stocks):
        price_float = get_fixstock_quote(stock["dotCode"], diff_time, current_time)
        if price_float is None or type(price_float) == str:
            price_float = 0.0
        stock_model = Stocks(name=stock["name"], symbol=stock["dotCode"], price=price_float)
        stock_model.save()
        if index == 0 and isJob:
            price_float = float(Stocks.objects.filter(symbol=stock["dotCode"])[0].price) + 0.1
        stock_model = Stocks(name=stock["name"], symbol=stock["dotCode"], price=price_float)
        stock_objects.append(stock_model)
        stock_model.save()
        price_float = None

    return stock_objects


def start_scheduler():
    scheduler = Scheduler()
    scheduler.every().minute.do(download_stocks, isJob=True)
    scheduler.run_continuously()


def run_continuously(self, interval=1):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run


Scheduler.run_continuously = run_continuously
