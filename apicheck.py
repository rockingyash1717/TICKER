import requests
import pandas as pd
import yfinance as yf

# ===== API KEYS =====
ALPHA_KEY = "GNC3M0GIO2BF6HHU"
GNEWS_KEY = "6e7a12111d17708ed89b621957e1e093"
ticker = "AAPL"  # Example: Apple

# ===== 1. PRICE MOMENTUM =====
url_price = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={ALPHA_KEY}"
data = requests.get(url_price).json()

# Convert price data to DataFrame
df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index', dtype=float)
df.index = pd.to_datetime(df.index)
df = df.sort_index()

# Calculate daily returns
df['return'] = df['4. close'].pct_change()
last_5_returns = df['return'].tail(5)
momentum_score = round(last_5_returns.sum(), 4)

print("=== Price Momentum ===")
print("Last 5 Daily Returns:")
print(last_5_returns)
print("Momentum Score:", momentum_score)


ticker_id = yf.Ticker(ticker)

company_name = ticker_id.info.get("longName", "Unknown")
company_name = company_name.split(" ")[0]  # Get the first part of the company name
print(company_name)

# ===== 2. NEWS FEED (Mediastack) =====
MEDIASTACK_KEY = "582cb1dafa0c318f2d826be541da7b03"
url_news = (
    f"http://api.mediastack.com/v1/news?"
    f"access_key={MEDIASTACK_KEY}"
    f"&keywords={company_name}"
    f"&limit=5"
    f"&sort=published_desc"
)
news_data = requests.get(url_news).json()

print("\n=== Latest News Headlines (Mediastack) ===")
for i, article in enumerate(news_data.get('data', []), start=1):
    title = article.get('title', 'No title')
    description = article.get('description', 'No description')
    print(f"{i}. {title} - {description}")
