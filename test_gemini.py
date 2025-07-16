import os
import google.generativeai as genai

# Example test data
momentum_score = 0.045
news_headlines = [
    {'title': 'Apple launches new product', 'description': 'Positive reception from analysts.'},
    {'title': 'Apple faces supply chain delays', 'description': 'Minor impact expected.'},
    {'title': 'Apple stock hits new high', 'description': 'Investors optimistic.'},
    {'title': 'Apple expands into new markets', 'description': 'Growth prospects strong.'},
    {'title': 'Apple sued over patents', 'description': 'Legal risks remain.'}
]

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

news_str = "\n".join([
    f"{i+1}. {n['title']} - {n['description']}" for i, n in enumerate(news_headlines)
])
prompt = f"""your Role: financial sentiment analysis model\nGiven the price momentum score: {momentum_score} and the following recent news headlines:\n{news_str}\n\nClassify the overall sentiment as bullish, neutral, or bearish. Briefly explain your reasoning referencing both the momentum and news context.\n"""

model = genai.GenerativeModel("gemini-2.0-flash")
response = model.generate_content(prompt)
print("\nGemini Sentiment Analysis Result:")
print(response.text)
