from flask import redirect, session
from functools import wraps
import yfinance as yf
import sqlite3

DATABASE_NAME = 'flaskr/trade.db'


# Decorator for routes so that is login is required
def login_required(orig_func):

    # use wraps so that the decorated function still has the route name
    @wraps(orig_func)
    def decorated_function(*args, **kwargs):
        print(session)
        if session.get("user_id") is None:
            return redirect("/login")
        return orig_func(*args, **kwargs)
    
    return decorated_function

def get_user_cash(id):
        """Get user cash from the database"""
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        rows = cur.execute('SELECT cash FROM users WHERE id = ?',(session['user_id'],)).fetchall()
        cash = rows[0]['cash']

        return cash 

def update_user_cash(id, cash):
        conn = sqlite3.connect(DATABASE_NAME)
        cur = conn.cursor()
        cur.execute("UPDATE users SET cash = ? WHERE id = ?", (cash, id))
        conn.commit()

def get_stock(symbol):
    try:
        ticker = yf.Ticker(symbol)
    except:
        return None
    
    stock_data = ticker.history(period="1d", interval="1m")
    current_price = stock_data.iloc[-1].Close
    return {"price": current_price, "symbol": symbol}

def get_user_portfolio(id):
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT symbol, SUM(shares) FROM transactions WHERE user_id = ? GROUP BY symbol"
        , (id,)).fetchall()
    
    stocks = []
    portfolio_value = 0
    for row in rows:
        stock = get_stock(row['symbol'])

        # Add number of shares of the stock and the value of the shares
        stock['shares'] = row['SUM(shares)']
        stock['total'] = round(stock['price'] * stock['shares'], 2)
        stock['price'] = round(stock['price'], 2)

        portfolio_value += stock['total']

        stocks.append(stock)
    
    cash = round(get_user_cash(id),2)
    portfolio_value = round(portfolio_value, 2)

    return {'stocks': stocks, 'cash': cash, 'value': portfolio_value}

def add_transaction(id, symbol, shares, price, time, type):
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, type, datetime) VALUES (?, ?, ?, ?, ?, ?)",
            (id, symbol.upper(), shares, price,type,time))

        conn.commit()
    

    