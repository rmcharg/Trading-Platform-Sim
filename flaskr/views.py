from flask import Blueprint, render_template, request, session, jsonify
from flaskr.helpers import login_required
import yfinance as yf
import pandas as pd
import time

views = Blueprint('views', __name__)

TICKERS = ['AAPL', 'NFLX']

@views.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@views.route("/")
@login_required
def index():
    return render_template("index.html")

@views.route("/portfolio")
@login_required
def portfolio():
    
    return render_template("portfolio.html")

@views.route("/transactions")
@login_required
def transactions():
    return render_template("transactions.html")

@views.route('/get_data')
def get_data():
    data = []
    for ticker_symbol in TICKERS:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        data.append({'ticker': ticker_symbol, 'currentPrice': round(info['currentPrice'],2)})

    return jsonify(data)
        
