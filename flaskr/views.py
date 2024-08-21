from flask import Blueprint, render_template, request, session, jsonify, flash, redirect
from flaskr.helpers import login_required, get_stock, get_user_portfolio, get_user_cash, add_transaction
from flaskr.helpers import update_user_cash
from datetime import datetime
import yfinance as yf
import pandas as pd
import time
import sqlite3 

views = Blueprint('views', __name__)

TICKERS = ['AAPL', 'NFLX']
DATABASE_NAME = 'flaskr/trade.db'

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
    return render_template("portfolio.html", portfolio=get_user_portfolio(session['user_id']))


@views.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol")

        if symbol is None:
            flash('Must enter a symbol for the stock you wish to buy!')
            return redirect("/buy")
        
        try:
            shares = int(request.form.get("shares"))
        except:
            flash('Invalid number of shares')
            return redirect("/buy")
        
        # check that the shares is not empty and it is positive
        if shares <= 0 or shares is None:
            flash('Invalid number of shares')
            return redirect("/buy")
        
        # try to get the stock value
        stock = get_stock(symbol)
        print(stock)
        if stock is None:
            flash('Invalid Symbol')
            return redirect("/buy")

        # connect to database to get user budget
        cash = get_user_cash(id)
        price = stock['price']
        transaction_cost = price * shares

        if cash - transaction_cost < 0:
            flash('You do not have the cash for this purchase')
            return redirect("/buy")
        
        # Get date and time (ISO 8601 format) and insert transaction record into db
        time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        user_id = session["user_id"]
        add_transaction(user_id, symbol, shares, price, time, 'Buy')

        # Update cash in users table
        new_cash = cash - transaction_cost
        update_user_cash(session['user_id'],new_cash)

        return redirect("/portfolio")


@views.route('/sell')
@login_required
def sell():
    return render_template("sell.html")


@views.route("/transactions")
@login_required
def transactions():
    return render_template("transactions.html")

@views.route('/get_dashboard_data')
@login_required
def get_dashboard_data():
    data = []
    for ticker_symbol in TICKERS:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        data.append({'ticker': ticker_symbol, 'currentPrice': round(info['currentPrice'],2)})

    return jsonify(data)



        
