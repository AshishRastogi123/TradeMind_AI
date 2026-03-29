from langchain_groq import ChatGroq
from utils import get_stock_data

class SentimentAgent:
    def __init__(self, groq_api_key: str):
        self.llm = ChatGroq(groq_api_key=groq_api_key, model="llama-3.3-70b-versatile")

    def analyze_sentiment(self, symbol: str) -> float:
        prompt = f"""Analyze sentiment for {symbol} from recent Indian financial news. Return only a number between -1.0 and 1.0"""
        response = self.llm.invoke(prompt)
        try:
            # Extract number safely, no bullets
            score_str = ''.join(c for c in response.content if c in '-0123456789. ')
            score = float(score_str.strip())
            return max(-1.0, min(1.0, score))
        except:
            return 0.0
