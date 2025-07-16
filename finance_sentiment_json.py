import requests
import pandas as pd
import yfinance as yf
import os
import google.generativeai as genai
import json

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
        url = article.get('url', '')
        headlines.append({'title': title, 'description': description, 'url': url})
    return headlines

if __name__ == "__main__":
    ALPHA_KEY = "GNC3M0GIO2BF6HHU"
    MEDIASTACK_KEY = "582cb1dafa0c318f2d826be541da7b03"
    ticker = "MSFT"
    ticker_id = yf.Ticker(ticker)
    company_name = ticker_id.info.get("longName", "Unknown").split(" ")[0]

    price_returns, momentum_score = get_price_momentum(ticker, ALPHA_KEY)
    raw_news = get_recent_news(company_name, MEDIASTACK_KEY)

    # Format news: ensure only title, description, url
    formatted_news = [
        {
            "title": n.get("title", ""),
            "description": n.get("description", ""),
            "url": n.get("url", "")
        }
        for n in raw_news
    ]

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBPVh_YR0IrLhlXFaabKr8fdTiLzJ6ELe8")
    genai.configure(api_key=GEMINI_API_KEY)

    news_str = "\n".join([
        f"{i+1}. {n['title']} - {n['description']}" for i, n in enumerate(formatted_news)
    ])
    prompt = f"""your Role: financial sentiment analysis model\nGiven the price momentum score: {momentum_score} and the following recent news headlines:\n{news_str}\n\nClassify the overall sentiment as bullish, neutral, or bearish. Short explain in 20 to 50 words your reasoning referencing both the momentum and news context.\n"""

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    llm_text = response.text.strip()
    pulse = ""
    explanation = llm_text
    # Remove overall sentiment phrase if present
    for sentiment in ["bullish", "neutral", "bearish"]:
        if sentiment in llm_text.lower():
            pulse = sentiment
            idx = llm_text.lower().find(sentiment)
            after = llm_text[idx+len(sentiment):].lstrip(". :,-\n")
            explanation = after if after else llm_text
            break

    # Remove '\n\nReasoning:' or similar phrases from explanation
    for phrase in ["\n\nReasoning:", "Reasoning:", "Reason:", "Explanation:"]:
        if phrase in explanation:
            explanation = explanation.split(phrase, 1)[-1].lstrip(". :,-\n")

    output = {
        "ticker": ticker,
        "as_of": pd.Timestamp.now().strftime("%Y-%m-%d"),
        "momentum": {
            "returns": [round(r, 4) for r in price_returns],
            "score": momentum_score
        },
        "news": formatted_news,
        "pulse": pulse,
        "llm_explanation": explanation
    }

    print(json.dumps(output, indent=2))
