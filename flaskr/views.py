from flask import Blueprint, render_template, request, session, jsonify, flash, redirect
from flaskr.helpers import login_required, get_stock, get_user_portfolio, get_user_cash, add_transaction
from flaskr.helpers import update_user_cash, get_user_transactions, add_user_holdings, get_indexes, remove_user_holdings
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
    """Dashboard, display summary of users portfolio as well
        as some key market indexes and their stock positions.
    """
    portfolio = get_user_portfolio(session['user_id'])
    indexes = get_indexes()
    return render_template("index.html", portfolio = portfolio, indexes=indexes)


@views.route("/portfolio")
@login_required
def portfolio():
    """Display users portfolio"""
    return render_template("portfolio.html", portfolio=get_user_portfolio(session['user_id']))


@views.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol").upper()

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

        # Check user can afford transaction
        user_id = session["user_id"]
        cash = get_user_cash(user_id)
        price = stock['current_price']
        transaction_cost = price * shares

        if cash - transaction_cost < 0:
            flash('You do not have the cash for this purchase')
            return redirect("/buy")
        
        # Get date and time (ISO 8601 format) and insert transaction record into db
        time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        add_transaction(user_id, symbol, shares, transaction_cost, time, 'Buy')

        # Add stocks to the users holdings table
        add_user_holdings(user_id, symbol, shares, price)

        # Update cash in users table
        update_user_cash(user_id, transaction_cost, action="remove")
        flash('Stocks Purchased!')
        return redirect("/portfolio")


@views.route('/sell', methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        return render_template("sell.html")
    else:
        symbol = request.form.get("symbol").upper()

        if symbol is None:
            flash('Must enter a symbol for the stock you wish to buy!')
            return redirect("/sell")
        
        try:
            shares = int(request.form.get("shares"))
        except:
            flash('Invalid number of shares')
            return redirect("/sell")
        
        # check that the shares is positive
        if shares <= 0 :
            flash('Invalid number of shares')
            return redirect("/sell")
        
        # try to get the stock value
        stock = get_stock(symbol)
        print(stock)
        if stock is None:
            flash('Invalid Symbol')
            return redirect("/sell")

        # Check user can afford transaction
        user_id = session["user_id"]
        cash = get_user_cash(user_id)
        price = stock['current_price']
        value_shares = price * shares
        
        # Get date and time (ISO 8601 format) and insert transaction record into db
        time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        user_id = session["user_id"]
        add_transaction(user_id, symbol, shares, value_shares, time, 'Sell')

        # Remove shares from users holdings table
        remove_user_holdings(user_id, symbol, shares, price)

        # Update users cash balance
        update_user_cash(user_id, value_shares, action="add")

        flash('Stocks Sold !')
        return redirect("/portfolio")


@views.route("/transactions")
@login_required
def transactions():
    transactions = get_user_transactions(session['user_id'])
    return render_template("transactions.html", transactions=transactions)

@views.route('/get_dashboard_data')
@login_required
def get_dashboard_data():
    data = {'portfolio': get_user_portfolio(session['user_id']), 
            'indexes': get_indexes()}

    return jsonify(data)



        
