import yfinance as yf


def get_stock_data(symbol: str):
    stock = yf.Ticker(symbol)

    # Retrieve the most recent 5 trading days
    history = stock.history(period="5d")

    if len(history) < 2:
        return None

    # Extract the two most recent closing prices
    current = float(history["Close"].iloc[-1])
    previous = float(history["Close"].iloc[-2])

    return current, previous