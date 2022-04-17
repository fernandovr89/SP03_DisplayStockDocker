from django.shortcuts import render
from display.models import Stocks
from django.http import HttpResponse
from . import stock_tools as st
import csv
import locale
import datetime


def display(request):
    # fmt: off
    st_name = ['ACCOR','AIR LIQUIDE','AXA','BNP PARIBAS','BOUYGUES',\
    'CRCAM BRIE PICARDIE','CRCAM NORD France',\
    'DANONE','EDENRED','ENGIE','ESSILOR LUXOTTICA','HERMES INTL',\
    'ICADE','IDI','IPSEN','LAGARDERE','L OREAL',\
    'METROPOLE TELEVISION','MICHELIN','ORANGE','PERNOD RICARD',\
    'ROTHSCHILD','RUBIS','SANOFI','SCHNEIDER ELECTRIC','SCOR',\
    'SUEZ ENVIRONNEMENT','THERMADOR GROUPE','TOTAL ENERGIES', \
    'UNIVERSAL MUSIC GROUP N.V.','VEOLIA ENVIRONNEMENT','VERALLIA', 'VIVENDI']
    st_toget = ['AC.PA','AI.PA','CS.PA','BNP.PA','EN.PA',\
    'CRBP2.PA','CNF.PA',\
    'BN.PA','EDEN.PA','ENGI.PA','EL.PA','RMS.PA',\
    'ICAD.PA','IDIP.PA','IPN.PA','MMB.PA','OR.PA',\
    'MMT.PA','ML.PA','ORA.PA','RI.PA',\
    'ROTH.PA','RUI.PA','SAN.PA','SU.PA','SCR.PA',\
    'SEV.PA','THEP.PA','TTE.PA',\
    'UMG.AS','VIE.PA','VRLA.PA', 'VIV.PA']
    # fmt: on
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
    for st_toget_i in range(len(st_toget)):
        price_fl = st.get_fixstock_quote(st_toget[st_toget_i], diff_time, current_time)
        if price_fl is None or type(price_fl) == str:
            price_fl = 0.0
        stock_model = Stocks(name=st_name[st_toget_i], symbol=st_toget[st_toget_i], price=price_fl)
        stock_model.save()
        price_fl = None
    return render(request, "template.tmpl", {"obj": Stocks.objects.all()})


def get_csv(request):
    locale.setlocale(locale.LC_ALL, "fr_FR.utf8")
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=get_values.csv"
    writer = csv.writer(response, dialect="excel", delimiter="\t")
    writer.writerow(["sep=\t"])
    obj = Stocks.objects.all()
    for obj_i in obj:
        writer.writerow([obj_i.name, locale.format("%.4f", obj_i.price)])
    return response
