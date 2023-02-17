from django.shortcuts import render
from display.models import Stocks
from django.http import HttpResponse
from . import stock_tools as st
import csv
import locale
import datetime


def display(request) -> HttpResponse:
    # dotCode is used in Yahoo Finance (e.g ACCOR SA code is AC.PA)
    stocks = [
        {"name": "ACCOR", "dotCode": "AC.PA"},
        {"name": "AIR LIQUIDE", "dotCode": "AI.PA"},
        {"name": "ALD SA", "dotCode": "ALD.PA"},
        {"name": "AXA", "dotCode": "CS.PA"},
        {"name": "BNP PARIBAS", "dotCode": "BNP.PA"},
        {"name": "BOUYGUES", "dotCode": "EN.PA"},
        {"name": "CRCAM BRIE PICARDIE", "dotCode": "CRBP2.PA"},
        {"name": "CRCAM NORD France", "dotCode": "CNF.PA"},
        {"name": "DANONE", "dotCode": "BN.PA"},
        {"name": "EDENRED", "dotCode": "EDEN.PA"},
        {"name": "ENGIE", "dotCode": "ENGI.PA"},
        {"name": "ESSILOR LUXOTTICA", "dotCode": "EL.PA"},
        {"name": "EUROAPI SA", "dotCode": "EAPI.PA"},
        {"name": "HERMES INTL", "dotCode": "RMS.PA"},
        {"name": "ICADE", "dotCode": "ICAD.PA"},
        {"name": "IDI", "dotCode": "IDIP.PA"},
        {"name": "IPSEN", "dotCode": "IPN.PA"},
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
        {"name": "STELLANTIS NV", "dotCode": "STLA.PA"},
        {"name": "THERMADOR GROUPE", "dotCode": "THEP.PA"},
        {"name": "TOTAL ENERGIES", "dotCode": "TTE.PA"},
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
        price_fl = st.get_fixstock_quote(stock["dotCode"], diff_time, current_time)
        stock_model = Stocks(name=stock["name"], symbol=stock["dotCode"], price=price_fl)
        stock_model.save()
        price_fl = None
    return render(request, "template.tmpl", {"stocks": Stocks.objects.all()})


def get_csv(request) -> HttpResponse:
    locale.setlocale(locale.LC_ALL, "fr_FR.utf8")
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=get_values.csv"
    writer = csv.writer(response, dialect="excel", delimiter="\t")
    writer.writerow(["sep=\t"])
    obj = Stocks.objects.all()
    for obj_i in obj:
        writer.writerow([obj_i.name, locale.format("%.4f", obj_i.price)])
    return response
