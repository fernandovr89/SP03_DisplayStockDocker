from django.shortcuts import render
from django.http import HttpResponse
from . import stock_tools as st
import csv
import locale


def display(request) -> HttpResponse:
    return render(request, "template.tmpl", {"stocks": st.download_stocks()})


def get_csv(request) -> HttpResponse:
    locale.setlocale(locale.LC_ALL, "fr_FR.utf8")
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=get_values.csv"
    writer = csv.writer(response, dialect="excel", delimiter="\t")
    writer.writerow(["sep=\t"])
    stocks = st.get_all_stocks()
    for stock in stocks:
        writer.writerow([stock.name, locale.format("%.4f", stock.price)])
    return response
