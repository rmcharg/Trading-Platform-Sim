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
        # Get ticker from API
        ticker = yf.Ticker(symbol)

        # Extract relevant stock information from ticker
        stock_history = ticker.history(period="1d", interval="1m", prepost=True)
        stock_info = ticker.info

        # Calculate change in price today
        current_price = stock_history.iloc[-1].Close
        open_price = stock_history.iloc[0].Open
        yesterday_close = stock_info['previousClose']
        change = ((current_price - yesterday_close) / yesterday_close) * 100

        stock_data = {
            "symbol": symbol,
            "current_price": current_price,
            "open_price": open_price,
            "change": change,
            "previous_close": yesterday_close,
            "Name": stock_info["shortName"],
            "market_cap": stock_info["marketCap"],
            "volume": stock_info["volume"],
            "average_volume": stock_info["averageVolume"],
            "day_low": stock_info["dayLow"],
            "day_high": stock_info["dayHigh"],
            "year_low": stock_info["fiftyTwoWeekLow"],
            "year_high": stock_info["fiftyTwoWeekHigh"]
        }
        return stock_data
    
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