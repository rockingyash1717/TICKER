import os
import json
import pandas as pd
import yfinance as yf
import httpx
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from cachetools import TTLCache
import google.generativeai as genai
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def get_price_momentum(ticker, alpha_key):
    url_price = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={alpha_key}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url_price)
        data = resp.json()
    df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index', dtype=float)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df['return'] = df['4. close'].pct_change()
    last_5_returns = df['return'].tail(5)
    momentum_score = round(last_5_returns.sum(), 4)
    return last_5_returns.tolist(), momentum_score

async def get_recent_news(company_name, mediastack_key):
    url_news = (
        f"http://api.mediastack.com/v1/news?"
        f"access_key={mediastack_key}"
        f"&keywords={company_name}"
        f"&limit=5"
        f"&sort=published_desc"
    )
    async with httpx.AsyncClient() as client:
        resp = await client.get(url_news)
        news_data = resp.json()
    headlines = []
    for article in news_data.get('data', []):
        title = article.get('title', 'No title')
        description = article.get('description', 'No description')
        url = article.get('url', '')
        headlines.append({'title': title, 'description': description, 'url': url})
    return headlines


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
ALPHA_KEY = os.getenv("ALPHA_KEY")
MEDIASTACK_KEY = os.getenv("MEDIASTACK_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

cache = TTLCache(maxsize=100, ttl=600)

def format_news(raw_news):
    return [
        {
            "title": n.get("title", ""),
            "description": n.get("description", ""),
            "url": n.get("url", "")
        }
        for n in raw_news
    ]

def extract_sentiment(llm_text):
    pulse = ""
    explanation = llm_text
    for sentiment in ["bullish", "neutral", "bearish"]:
        if sentiment in llm_text.lower():
            pulse = sentiment
            idx = llm_text.lower().find(sentiment)
            after = llm_text[idx+len(sentiment):].lstrip(". :,-\n")
            explanation = after if after else llm_text
            break
    for phrase in ["\n\nReasoning:", "Reasoning:", "Reason:", "Explanation:"]:
        if phrase in explanation:
            explanation = explanation.split(phrase, 1)[-1].lstrip(". :,-\n")
    return pulse, explanation

@app.get("/api/v1/market-pulse")
async def market_pulse(ticker: str = Query(...)):
    cache_key = f"sentiment:{ticker}"
    if cache_key in cache:
        return cache[cache_key]

    ticker_id = yf.Ticker(ticker)
    company_name = ticker_id.info.get("longName", "Unknown").split(" ")[0]

    price_returns, momentum_score = await get_price_momentum(ticker, ALPHA_KEY)
    raw_news = await get_recent_news(company_name, MEDIASTACK_KEY)
    formatted_news = format_news(raw_news)

    news_str = "\n".join([
        f"{i+1}. {n['title']} - {n['description']}" for i, n in enumerate(formatted_news)
    ])
    prompt = f"""your Role: financial sentiment analysis model\nGiven the price momentum score: {momentum_score} and the following recent news headlines:\n{news_str}\n\nClassify the overall sentiment as bullish, neutral, or bearish. Short explain in 20 to 50 words your reasoning referencing both the momentum and news context.\n"""

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = await asyncio.to_thread(model.generate_content, prompt)
    llm_text = response.text.strip()
    pulse, explanation = extract_sentiment(llm_text)

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
    cache[cache_key] = output
    return output
