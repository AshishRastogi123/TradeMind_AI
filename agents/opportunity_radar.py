from typing import List
from utils import get_stock_data
from config import NSE_SYMBOLS
import pandas as pd

class OpportunityRadarAgent:
    def __init__(self):
        self.symbols = NSE_SYMBOLS

    def scan_opportunities(self) -> List[str]:
        # Loosen criteria to always return some symbols for demo
        opportunities = self.symbols[:3]  # First 3 for demo
        print(f"Debug OpportunityRadar: Scanning {len(self.symbols)} symbols, returning {len(opportunities)}")
        return opportunities

    def score_opportunity(self, symbol: str) -> float:
        data = get_stock_data(symbol)
        hist = data["hist"]
        change_5d = (hist["Close"].iloc[-1] / hist["Close"].iloc[-5] - 1)
        vol_spike = hist["Volume"].iloc[-1] / hist["Volume"].rolling(5).mean().iloc[-1]
        score = min(1.0, (change_5d + 0.5 * vol_spike) / 2)
        return score
