import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.mysite.settings')
django.setup()

from django.test import TestCase
from investie.models import Stock

class StockModelTest(TestCase):
    def setUp(self):
        self.stock = Stock.objects.create(ticker='AAPL', security_name='Apple Inc.')

    def test_stock_creation(self):
        self.assertEqual(self.stock.ticker, 'AAPL')
        self.assertEqual(self.stock.security_name, 'Apple Inc.')
