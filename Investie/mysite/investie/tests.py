import os
import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from investie.models import Stock, Watchlist

class StockModelTest(TestCase):
    def setUp(self):
        self.stock = Stock.objects.create(ticker='AAPL', security_name='Apple Inc.')

    def test_stock_creation(self):
        self.assertEqual(self.stock.ticker, 'AAPL')
        self.assertEqual(self.stock.security_name, 'Apple Inc.')

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.watchlist = Watchlist.objects.create(user=self.user, watchlist_name='Test Watchlist', tickers=["AAPL", "GOOG"])

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chart_template.html')

    def test_get_live_price_view(self):
        response = self.client.get(reverse('get_live_price'), {'ticker': 'AAPL'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('current_price', response.json())

    def test_watchlists_view_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('watchlists'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Watchlist')

    def test_watchlists_view_unauthenticated(self):
        response = self.client.get(reverse('watchlists'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_view_watchlist_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('view_watchlist', args=[self.watchlist.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_watchlist.html')

    def test_create_watchlist_get(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('create_watchlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_watchlist.html')

    def test_create_watchlist_post(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'watchlist_name': 'New Watchlist',
            'watchlist': json.dumps(["AAPL", "MSFT"])
        }
        response = self.client.post(reverse('create_watchlist'), data)
        self.assertEqual(response.status_code, 302)  # redirect after success
        self.assertTrue(Watchlist.objects.filter(watchlist_name='New Watchlist').exists())
