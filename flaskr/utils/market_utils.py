# Functions used for retrieving live market data
import yfinance as yf

def get_stock_data(symbol):
    """Get the current price of the stock.
    
    inputs:
        - symbol: the stocks ticker symbol
    
    returns:
        - dict containing the following information about the stock:
            - symbol
            - current market price
            - todays opening price
            - % change from yesterdays closing price
    """
    try:
        ticker = yf.Ticker(symbol)
        stock_data = ticker.history(period="1d", interval="1m")
        current_price = stock_data.iloc[-1].Close
        open_price = stock_data.iloc[0].Open
        yesterday_close = ticker.history(period="5d", interval="1d").iloc[-2].Close
        change = ((current_price - yesterday_close) / yesterday_close) * 100
        return {"symbol": symbol, "current_price": current_price, "open_price": open_price, "change": change}
    
    except:
         return None
    

def get_indexes():
    """Get the current pricing data for a list of predefined stocks
    
    returns:
    - list of dictionaries, where each dictionary contains the pricing 
        data for one stock.
    """
    index_symbols = ['^GSPC', '^IXIC', '^DJI','^FTSE', '^HSI']
    indexes = []
    for symbol in index_symbols:
         index = get_stock_data(symbol)
         indexes.append(index)

    return indexes