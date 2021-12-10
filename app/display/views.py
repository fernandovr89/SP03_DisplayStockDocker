from django.shortcuts import render
from display.models import Stocks
from django.http import HttpResponse
from . import stocks
import csv
import locale
import time
import datetime

def display(request):
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
    price_fl = None
    Stocks.objects.all().delete()
    current_time_tmp = datetime.datetime.now()+datetime.timedelta(days=1)
    current_time = current_time_tmp.strftime("%Y-%m-%d")
    diff_time_tmp = datetime.datetime.now()-datetime.timedelta(days=6)
    diff_time = diff_time_tmp.strftime("%Y-%m-%d")
    print(current_time)
    print(diff_time)
    for st_toget_i in range(len(st_toget)):
      price_fl=stocks.get_fixstock_quote(st_toget[st_toget_i],diff_time,current_time)
      if price_fl is None or type(price_fl) == str:
          price_fl = 0.0 
      st = Stocks(name=st_name[st_toget_i],symbol=st_toget[st_toget_i],price=price_fl)
      st.save()
      price_fl = None
    return render(request,'template.tmpl',{'obj':Stocks.objects.all()})


def get_csv(request):
    locale.setlocale(locale.LC_ALL,'fr_FR.utf8')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=get_values.csv'
    writer = csv.writer(response,dialect="excel",delimiter="\t")
    writer.writerow(['sep=\t'])
    obj = Stocks.objects.all()
    for obj_i in obj:
      writer.writerow([obj_i.name,locale.format('%.4f',obj_i.price)])
    return response

