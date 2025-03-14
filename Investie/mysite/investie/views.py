import datetime

from django.http import HttpResponse
from django.shortcuts import render
import yfinance as yf
import json
from django.http import JsonResponse
from alpha_vantage.timeseries import TimeSeries

def index(request):
    stock_data = yf.Ticker("AAPL").history(period="6mo", auto_adjust=True)

    labels = stock_data.index.strftime('%Y-%m-%d').tolist()
    data = stock_data['Close'].tolist()
    chart_data = {
        'labels': labels,
        'data': data
    }

    return render(request, 'chart_template.html', {'data': json.dumps(chart_data)})

def get_live_price(request):
    # api_key = 'M7WMH9UKWLS88BMX'
    # ts = TimeSeries(key=api_key, output_format='pandas')
    # data, meta_data = ts.get_quote_endpoint(symbol='AAPL')
    # current_price = data['05. price'][0]
    return JsonResponse({'current_price': 3, 'last_updated': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
