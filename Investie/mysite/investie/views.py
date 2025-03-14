from django.http import HttpResponse
from django.shortcuts import render
import yfinance as yf
import json

def index(request):
    stock_data = yf.Ticker("AAPL").history(period="6mo", auto_adjust=True)

    labels = stock_data.index.strftime('%Y-%m-%d').tolist()
    data = stock_data['Close'].tolist()
    chart_data = {
        'labels': labels,
        'data': data
    }

    return render(request, 'chart_template.html', {'data': json.dumps(chart_data)})