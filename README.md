# TICKER - Market Sentiment Analysis API

A FastAPI-based market sentiment analysis tool that provides real-time stock momentum analysis and news sentiment evaluation using AI.

## 🚀 Features

- **Real-time Stock Analysis**: Get price momentum scores based on recent trading data
- **News Sentiment Analysis**: AI-powered sentiment classification (bullish, neutral, bearish)
- **Caching System**: Efficient TTL-based caching for improved performance
- **RESTful API**: Clean and well-documented API endpoints
- **CORS Support**: Ready for frontend integration

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- API Keys for:
  - Alpha Vantage (stock data)
  - MediaStack (news data)
  - Google Gemini AI (sentiment analysis)

## 🛠️ Installation

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/rockingyash1717/TICKER.git
   cd TICKER
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```env
   ALPHA_KEY=your_alpha_vantage_api_key
   MEDIASTACK_KEY=your_mediastack_api_key
   GEMINI_API_KEY=your_gemini_api_key
   ```

5. **Run the backend server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000` and will automatically proxy API requests to the backend at `http://localhost:8000`.

## 📦 Dependencies

### Backend
```txt
fastapi
uvicorn
pandas
yfinance
httpx
cachetools
google-generativeai
python-dotenv
```

### Frontend
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.4.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.0.3",
    "vite": "^4.4.5"
  }
}
```

## 🔧 API Endpoints

### GET `/api/v1/market-pulse`

Get market sentiment analysis for a stock ticker.

**Parameters:**
- `ticker` (required): Stock ticker symbol (e.g., "AAPL", "GOOGL")

**Response:**
```json
{
  "ticker": "AAPL",
  "as_of": "2024-01-15",
  "momentum": {
    "returns": [0.0123, -0.0045, 0.0067, 0.0089, -0.0012],
    "score": 0.0222
  },
  "news": [
    {
      "title": "Apple Reports Strong Q4 Earnings",
      "description": "Apple Inc. reported better-than-expected earnings...",
      "url": "https://example.com/news/apple-earnings"
    }
  ],
  "pulse": "bullish",
  "llm_explanation": "Strong momentum score of 0.0222 combined with positive earnings news suggests bullish sentiment."
}
```

## 🚀 Usage Examples

### Using curl
```bash
curl "http://localhost:8000/api/v1/market-pulse?ticker=AAPL"
```

### Using Python requests
```python
import requests

response = requests.get("http://localhost:8000/api/v1/market-pulse?ticker=AAPL")
data = response.json()
print(f"Sentiment: {data['pulse']}")
```

### Frontend Integration
```javascript
import axios from 'axios';

const fetchMarketPulse = async (ticker) => {
  try {
    const response = await axios.get(`/api/v1/market-pulse?ticker=${ticker}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching market pulse:', error);
  }
};
```

## 🔍 How It Works

1. **Price Momentum**: Calculates 5-day return momentum using Alpha Vantage daily price data
2. **News Collection**: Fetches recent news headlines using MediaStack API
3. **Sentiment Analysis**: Uses Google Gemini AI to analyze combined momentum and news data
4. **Caching**: Results are cached for 10 minutes to reduce API calls and improve performance

## 🎯 Frontend Features

- **Responsive Design**: Mobile-friendly interface built with modern React
- **Real-time Updates**: Live market sentiment tracking
- **Interactive Charts**: Visual representation of momentum and sentiment
- **Search Functionality**: Easy ticker symbol lookup
- **Dark/Light Mode**: User preference theme switching

## 📁 Project Structure

```
TICKER/
├── main.py              # FastAPI backend application
├── getname.py           # Company name extraction utility
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
├── README.md           # This file
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── utils/
    │   └── App.jsx
    ├── package.json
    ├── vite.config.js
    └── index.html
```

## 🔐 API Keys Setup

### Alpha Vantage
1. Visit [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. Sign up for a free API key
3. Add to `.env` file as `ALPHA_KEY`

### MediaStack
1. Visit [MediaStack](https://mediastack.com/)
2. Create account and get API key
3. Add to `.env` file as `MEDIASTACK_KEY`

### Google Gemini AI
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Generate API key
3. Add to `.env` file as `GEMINI_API_KEY`

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Known Issues

- API rate limits may apply based on your subscription tier
- News data availability depends on MediaStack coverage
- Sentiment analysis accuracy may vary based on news quality

## 🆘 Support

For support, please open an issue on GitHub or contact the maintainers.

## 🔄 Changelog

### v1.0.0
- Initial release with basic sentiment analysis
- FastAPI backend with caching
- Vite React frontend integration
- Support for major stock tickers

---

**Made with ❤️ by [rockingyash1717](https://github.com/rockingyash1717)**
