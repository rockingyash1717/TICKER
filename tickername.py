import yfinance as yf

ticker_symbol = "AAPL"  # Example ticker
ticker = yf.Ticker(ticker_symbol)

company_name = ticker.info.get("longName", "Unknown")
print(company_name)