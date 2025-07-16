# Finance Sentiment API

This project provides a FastAPI-based REST API for financial sentiment analysis using price momentum and recent news headlines. It integrates with Alpha Vantage, MediaStack, Yahoo Finance, and Google Gemini for LLM-based sentiment classification.

## Features
- Fetches price momentum for a given ticker using Alpha Vantage
- Retrieves recent news headlines using MediaStack
- Uses Gemini LLM to classify sentiment (bullish, neutral, bearish) with reasoning
- Caches results for performance

## Setup
1. Clone the repository and navigate to the project folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```env
   ALPHA_KEY=your_alpha_vantage_key
   MEDIASTACK_KEY=your_mediastack_key
   GEMINI_API_KEY=your_gemini_api_key
   ```

## Usage
Run the API server:
```bash
uvicorn finance_sentiment_api:app --reload
```

Access the endpoint:
```
GET /api/v1/market-pulse?ticker=MSFT
```

## Files
- `finance_sentiment_api.py`: Main FastAPI app and logic
- `finance_utils.py`, `finance_sentiment_json.py`, `tickername.py`: Utility modules
- `test_gemini.py`: Test script for Gemini integration
- `apicheck.py`: API check script

## License
MIT
