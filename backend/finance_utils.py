import requests
import pandas as pd
import yfinance as yf

import os
import google.generativeai as genai

# ===== 1. PRICE MOMENTUM FUNCTION =====
def get_price_momentum(ticker, alpha_key):
    url_price = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={alpha_key}"
    data = requests.get(url_price).json()
    df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index', dtype=float)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df['return'] = df['4. close'].pct_change()
    last_5_returns = df['return'].tail(5)
    momentum_score = round(last_5_returns.sum(), 4)
    return last_5_returns.tolist(), momentum_score

# ===== 2. RECENT NEWS FUNCTION =====
def get_recent_news(company_name, mediastack_key):
    url_news = (
        f"http://api.mediastack.com/v1/news?"
        f"access_key={mediastack_key}"
        f"&keywords={company_name}"
        f"&limit=5"
        f"&sort=published_desc"
    )
    news_data = requests.get(url_news).json()
    headlines = []
    for article in news_data.get('data', []):
        title = article.get('title', 'No title')
        description = article.get('description', 'No description')
        headlines.append({'title': title, 'description': description})
    return headlines

# ===== EXAMPLE USAGE =====
if __name__ == "__main__":
    ALPHA_KEY = "GNC3M0GIO2BF6HHU"
    MEDIASTACK_KEY = "582cb1dafa0c318f2d826be541da7b03"
    ticker = "AAPL"
    ticker_id = yf.Ticker(ticker)
    company_name = ticker_id.info.get("longName", "Unknown").split(" ")[0]

    price_returns, momentum_score = get_price_momentum(ticker, ALPHA_KEY)
    news_headlines = get_recent_news(company_name, MEDIASTACK_KEY)

    print("Last 5 Daily Returns:", price_returns)
    print("Momentum Score:", momentum_score)
    print("Latest News Headlines:")
    for i, article in enumerate(news_headlines, start=1):
        print(f"{i}. {article['title']} - {article['description']}")

    

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBPVh_YR0IrLhlXFaabKr8fdTiLzJ6ELe8")
    genai.configure(api_key=GEMINI_API_KEY)

    # Prepare shorter prompt
    news_str = "\n".join([
        f"{i+1}. {n['title']} - {n['description']}" for i, n in enumerate(news_headlines)
    ])
    prompt = f"""your Role: financial sentiment analysis model
Given the price momentum score: {momentum_score} and the following recent news headlines:\n{news_str}\n\nClassify the overall sentiment as bullish, neutral, or bearish. Short explain in 20 to 50 words your reasoning referencing both the momentum and news context.
"""

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    print("\nGemini Sentiment Analysis Result:")
    print(response.text)
