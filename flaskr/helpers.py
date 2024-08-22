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
        """Get user cash from the database.
        
        inputs: 
            - id: the users id in the database
        returns:
            - the current cash balance of the users account
        """
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        rows = cur.execute('SELECT cash FROM users WHERE id = ?',(session['user_id'],)).fetchall()
        cash = rows[0]['cash']

        return cash 


def update_user_cash(id, cash):
        """Update the users cash balance in the database.
        
        inputs:
            - id: the users unique account id in the database
            - cash: the users new cash balance
        
        returns: None
        """
        conn = sqlite3.connect(DATABASE_NAME)
        cur = conn.cursor()
        cur.execute("UPDATE users SET cash = ? WHERE id = ?", (cash, id))
        conn.commit()


def get_stock(symbol):
    """Get the current price of the stock.
    
    inputs:
        - symbol: the stocks ticker symbol
    
    returns:
        - dict containing the price and the symbol
    """
    try:
        ticker = yf.Ticker(symbol)
    except:
        return None
    
    stock_data = ticker.history(period="1d", interval="1m")
    current_price = stock_data.iloc[-1].Close
    return {"price": current_price, "symbol": symbol}


def get_user_portfolio(id):
    """Get a summary of users portfolio data.
    
        This function will return the users stock holdings and their current
        value as well as the total portfolio value and cash balance
        
        inputs:
            - id: user unique id in database
        
        returns:
            - dict containing the stock holdings stored in a dict themselves,
                the cash balance and the total portfolio value
    """
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
    portfolio_value = round(portfolio_value, 2) + cash

    return {'stocks': stocks, 'cash': cash, 'value': portfolio_value}


def add_transaction(id, symbol, shares, price, time, type):
        """Add record of transaction to database.
        
        inputs:
            - id: user unique id
            - symbol: stock being bought/sold
            - shares: number of shares bought/sold
            - time: date and time of transaction
            - type: the type of transaction (buy or sell)
        
        returns: None
        """
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, type, datetime) VALUES (?, ?, ?, ?, ?, ?)",
            (id, symbol.upper(), shares, price,type,time))

        conn.commit()
    
def get_user_transactions(id):
    """Get all of the transactions of the user.
        
        inputs:
            - id: users unique id
        
        returns:
            - list of dicts where each dict contains an individual transactions
                info."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    transactions =cur.execute(
         "SELECT symbol, shares, price, datetime FROM transactions WHERE user_id = ?",
        (id,)).fetchall()
    
    return transactions


    