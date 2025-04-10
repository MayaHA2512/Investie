import datetime
from . import models
from django.http import HttpResponse
from django.shortcuts import render
import yfinance as yf
import json
import os
from django.conf import settings
import csv
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from alpha_vantage.timeseries import TimeSeries

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
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'watchlists.html', {'user': user.username})
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')  # Redirect to login page after successful registration
        else:
            form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def create_watchlist(request):
    if request.method == 'POST':
        print('YOOO A WATCHLIST HAS BEEN Created!')
        print('These are the deetes we have' + str(request.POST))
    csv_path = os.path.join(settings.BASE_DIR, 'investie/nasdaq-listed.csv')
    tickers = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tickers.append({'symbol': row['AACBU'], 'name': row['Artius II Acquisition Inc. - Units']})
    return render(request, 'create_watchlist.html', {'tickers': tickers})
