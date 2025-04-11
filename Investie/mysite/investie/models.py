from django.db import models
from django.contrib.auth.models import User


class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    security_name = models.CharField(max_length=255)

    def __str__(self):
        return self.ticker

class Watchlist(models.Model):
    watchlist_name = models.CharField(max_length=255)
    tickers = models.JSONField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

