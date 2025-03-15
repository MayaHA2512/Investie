from django.db import models
import csv


class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    security_name = models.CharField(max_length=255)


# def publish_tickers():
#     with open('/Users/mayahettiarachchige/PycharmProjects/Investie/mysite/investie/nasdaq-listed.csv'
# ) as csv_file:
#         reader = csv.reader(csv_file)
#         for row in reader:
#             print('added an object')
#             Stock.objects.create(ticker=row[0], security_name=row[1])