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


def update_user_cash(id, amount, action):
        """Update the users cash balance in the database.
        
        inputs:
            - id: the users unique account id in the database
            - amount: the amount to be added/removed from user accounts cash balance
            - action: specify whether amount should be added or removed
        
        returns: None
        """
        # get users current cash balance
        current_cash_balance = get_user_cash(id)

        # Determine new cash balance, if not valid type is entered return none
        if action.lower() == "add":
             new_cash_balance = current_cash_balance + amount
        elif action.lower() == "remove":
             new_cash_balance = current_cash_balance - amount
        else:
             return False
        
        # Connect to database
        conn = sqlite3.connect(DATABASE_NAME)
        cur = conn.cursor()
        cur.execute(             
             "UPDATE users SET cash = ? WHERE id = ?", 
             (new_cash_balance, session['user_id']))
        conn.commit()
        cur.close()


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
        "SELECT symbol, shares, total_value FROM holdings WHERE user_id = ?", 
        (id,)).fetchall()
    
    stocks = []
    for row in rows:
        stock = {}
    
        # Add number of shares of the stock and the value of the shares
        stock['symbol'] = row['symbol']
        stock['shares'] = row['shares']
        stock['total'] = row['total_value']
        stock['price'] = 10
        stocks.append(stock)
    
    portfolio_value = 0
    cash = get_user_cash(id)

    return {'stocks': stocks, 'cash': cash, 'value': portfolio_value}


def add_transaction(id, symbol, shares, value, time, transaction_type):
        """Add record of transaction to database.
        
        inputs:
            - id: user unique id
            - symbol: stock being bought/sold
            - shares: number of shares bought/sold
            - value: value of shares being sold
            - time: date and time of transaction
            - type: the type of transaction (buy or sell)
        
        returns: None
        """
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO transactions (user_id, symbol, shares, value, datetime, type) VALUES (?, ?, ?, ?, ?, ?)",
            (id, symbol.upper(), shares, value, time, transaction_type))

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
         "SELECT symbol, shares, value, datetime FROM transactions WHERE user_id = ?",
        (id,)).fetchall()
    
    return transactions


def add_user_holdings(id, symbol, shares, price):
    # Connect to database
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Check to see if the user already has holdings in these shares
    rows = cur.execute(
         "SELECT shares, total_value FROM holdings WHERE user_id = ? AND symbol = ?",
         (id, symbol)).fetchall()
    
    
    if len(rows) == 0:
         cur.execute(
              "INSERT INTO holdings (user_id, symbol, shares, total_value) VALUES (?, ?, ?, ?)",
              (session['user_id'], symbol, shares, shares * price))

    else:
        new_shares = rows[0]['shares'] + shares
        new_total_value = rows[0]['total_value'] + shares * price
        cur.execute("UPDATE holdings SET shares = ?, total_value = ? WHERE user_id = ? AND symbol = ?",
                    (new_shares, new_total_value, session['user_id'], symbol))

    conn.commit()