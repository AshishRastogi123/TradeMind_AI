import json
import config
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any
import yfinance as yf
import talib
import numpy as np
from langchain_groq import ChatGroq

@dataclass
class StockSignal:
    symbol: str
    opportunity_score: float  # 0-1
    tech_score: float  # 0-1
    sentiment_score: float  # -1 to 1
    risk_score: float  # 0-1 (lower better)

@dataclass
class Recommendation:
    stock: str
    action: str  # STRONG BUY, BUY, HOLD, SELL
    confidence: int  # 0-100
    risk_level: str  # Low/Medium/High
    entry: float
    target: float
    stop_loss: float
    reason: List[str]

def compute_rsi(data: np.ndarray, period: int = 14) -> float:
    return talib.RSI(data, timeperiod=period)[-1] if len(data) >= period else 50

def compute_macd(data: np.ndarray) -> Dict[str, float]:
    macd, signal, hist = talib.MACD(data)
    return {"macd": macd[-1], "signal": signal[-1], "hist": hist[-1]}

def get_stock_data(symbol: str, period: str = "1mo") -> Dict[str, Any]:
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period)
    return {"hist": hist, "info": ticker.info}

def translate_to_hindi(llm: ChatGroq, text: str) -> str:
    prompt = config.HINDI_PROMPT.format(text=text)
    return llm.invoke(prompt).content

# JSON Schema for validation (simplified)
RECOMMENDATION_SCHEMA = {
    "type": "object",
    "properties": {
        "stock": {"type": "string"},
        # etc.
    }
}
