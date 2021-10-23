from django.db import models

class Stocks(models.Model):
    name = models.CharField(max_length=48)
    symbol = models.CharField(max_length=24)
    price = models.DecimalField(max_digits=11,decimal_places=4)
