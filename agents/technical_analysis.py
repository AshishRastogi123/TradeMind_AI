from utils import get_stock_data, compute_rsi, compute_macd
import numpy as np
from typing import Dict

class TechnicalAnalysisAgent:
    def analyze(self, symbol: str) -> Dict:
        data = get_stock_data(symbol)
        hist = data["hist"]
        closes = hist["Close"].values

        rsi = compute_rsi(closes)
        macd_data = compute_macd(closes)
        sma20 = np.mean(closes[-20:])
        sma50 = np.mean(closes[-50:]) if len(closes) >= 50 else sma20

        rsi_score = 1 if rsi < 30 else -1 if rsi > 70 else 0
        ma_score = 1 if closes[-1] > sma20 > sma50 else -1
        macd_score = 1 if macd_data["hist"] > 0 else -1
        tech_score = (rsi_score + ma_score + macd_score) / 3

        return {
            "symbol": symbol,
            "rsi": rsi,
            "macd": macd_data,
            "sma20": sma20,
            "tech_score": max(0, min(1, tech_score + 1))
        }
