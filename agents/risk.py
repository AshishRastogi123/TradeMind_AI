from utils import get_stock_data
import numpy as np
from typing import Dict

class RiskAgent:
    def assess_risk(self, symbol: str) -> Dict:
        data = get_stock_data(symbol)
        hist = data["hist"]
        returns = hist["Close"].pct_change().dropna()
        vol = returns.std()
        drawdown = (hist["Close"] / hist["Close"].cummax() - 1).min()

        risk_score = min(1.0, vol * 10 + abs(drawdown) * 5)
        risk_level = "Low" if risk_score < 0.3 else "Medium" if risk_score < 0.6 else "High"

        return {"risk_score": risk_score, "risk_level": risk_level, "vol": vol}
