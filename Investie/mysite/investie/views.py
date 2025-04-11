import datetime
from . import models
from django.http import HttpResponse
from django.shortcuts import render
import yfinance as yf
import json
import os
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
import json
from django.conf import settings
import csv
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from alpha_vantage.timeseries import TimeSeries
from investie.models import Watchlist
from django.shortcuts import render, get_object_or_404


def get_price_for_day(stock_symbol, days=7):
    try:
        print('Stock symbol is ' + str(stock_symbol))
        stock = yf.Ticker(stock_symbol)
        if stock:
            history_data = stock.history(period=f"{days}d")
            prices = history_data['Close'].tolist()
            print('These are the prices' + str(prices))
            dates = history_data.index.strftime('%Y-%m-%d').tolist()
            return dates, prices
    except Exception as e:
        print('e')

def index(request):
    ticker = request.GET.get('ticker', 'AAPL')
    stock_data = yf.Ticker(ticker).history(period="6mo", auto_adjust=True)
    labels = stock_data.index.strftime('%Y-%m-%d').tolist()
    data = stock_data['Close'].tolist()
    chart_data = {
        'labels': labels,
        'data': data
    }

    csv_path = os.path.join(settings.BASE_DIR, 'investie/nasdaq-listed.csv')
    tickers = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tickers.append({'symbol': row['AACBU'], 'name': row['Artius II Acquisition Inc. - Units']})

    return render(request, 'chart_template.html', {'data': json.dumps(chart_data), 'tickers': tickers})

from django.shortcuts import render
from .forms import EntryForm

def entry_view(request):
    form = EntryForm()
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            selected_entry = form.cleaned_data['entry']
            print(selected_entry)
    return render(request, 'entry_template.html', {'form': form})


def get_live_price(request):
    ticker = request.GET.get('ticker', 'AAPL')
    print(f'getting ticker for {ticker}')

    stock = yf.Ticker(ticker)

    today_data = stock.history(period="1d")
    current_price = today_data['Close'].iloc[-1] if not today_data.empty else None

    history_data = stock.history(period="1mo")
    labels = history_data.index.strftime('%Y-%m-%d').tolist()
    chart_data = history_data['Close'].tolist()

    return JsonResponse({
        'current_price': round(current_price) if current_price else "N/A",
        'last_updated': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'chart_labels': labels,
        'chart_data': chart_data
    })

def home(request):
    return render(request, 'home.html')

def watchlists(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        user = request.user
        watchlists_for_user = Watchlist.objects.filter(user=request.user)
        print(f'These are the watchlists for {user}: {watchlists_for_user}')
        return render(request, 'watchlists.html', {'user': user.username, 'watchlists': watchlists_for_user})
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def create_watchlist(request):
    user = request.user
    if request.method == 'POST':
        print('YOOO A WATCHLIST HAS BEEN Created!')
        print(json.loads(request.POST.get('watchlist'))[0])
        print('These are the deetes we have' + str(request.POST))
        Watchlist.objects.create(watchlist_name=request.POST.get('watchlist_name'), tickers=json.loads(request.POST.get('watchlist')), user=user)
        return redirect('watchlists')
    csv_path = os.path.join(settings.BASE_DIR, 'investie/nasdaq-listed.csv')
    tickers = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tickers.append({'symbol': row['AACBU'], 'name': row['Artius II Acquisition Inc. - Units']})
    return render(request, 'create_watchlist.html', {'tickers': tickers})


def view_watchlist(request, id):
    watchlist = get_object_or_404(Watchlist, id=id)
    stocks = watchlist.tickers
    print('These are the stocks' + str(stocks))
    labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    data = {}
    for stock in stocks:
        stock_prices = [
            get_price_for_day(stock, day) for day in range(1, 7)
        ]
        data[stock] = stock_prices
    chart_data = {
        'labels': labels,
        'datasets': []
    }
    for stock_symbol, prices in data.items():
        chart_data['datasets'].append({
            'label': stock_symbol,
            'data': prices,
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1
        })
    chart_data_json = json.dumps(chart_data)
    return render(request, 'view_watchlist.html', {'watchlist': watchlist, 'chart_data': chart_data_json})

def home(request):
    return render(request, 'home.html')